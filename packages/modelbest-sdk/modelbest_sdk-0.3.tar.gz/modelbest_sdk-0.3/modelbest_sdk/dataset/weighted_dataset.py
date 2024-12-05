from typing import Tuple
import numpy as np
import concurrent.futures
import torch
from modelbest_sdk.dataset.prefetch_chunk_dataset import PrefetchChunkDataset
from modelbest_sdk.dataset.sampler.sampler_factory import WEIGHTED_SAMPLER, WEIGHTED_MEGATRON_SAMPLER,SamplerFactory
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT, NO_SEGMENT
from modelbest_sdk.dataset.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.constant import *
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class WeightedDataset(torch.utils.data.IterableDataset):
    def __init__(
        self, 
        context: DatasetContext, 
        dataset_info_list: DatasetInfoList,
        segment_type=NO_SEGMENT,
        sampler_type=WEIGHTED_SAMPLER,
        max_len=1024,
        prefetch_chunk_cnt=2,
        chunk_size=1024,
        dp_group=None,
        **kwargs
        ):
        
        self.context = context
        self.dataset_info_list = dataset_info_list.dataset_info_list

        self.dataset_weights = []
        self.datasets: List[SegmentDataset] = []
        self.prefetch_chunk_datasets: List[PrefetchChunkDataset] = []
        self.datasets_iter = []
        self.name_to_datasets: Dict[str, SegmentDataset] = {}
        weights = []
        def process_dataset_info(dataset_info: DatasetInfo):
            if dataset_info.weight == 0:
                # 如果设置 weight = 0，我们认为只是暂时不参与采样，但是之后可能会继续使用，所以我们要保留其 checkpoint 信息
                # 如果直接删掉了某条数据集，那么之前的 checkpoint 信息也会丢失
                logger.warning(f"Dataset {dataset_info.path} has weight 0, won't sample, but will initialize it")
                # continue
            prefetch_chunk_dataset = PrefetchChunkDataset(
                context=context,
                dataset_info=dataset_info,
                prefetch_chunk_cnt=prefetch_chunk_cnt,
                chunk_size=chunk_size,
                dp_group=dp_group,
                **kwargs
            )
            dataset = SegmentDataset(
                prefetch_chunk_dataset=prefetch_chunk_dataset,
                segment_type=segment_type,
                max_len=max_len,
                **kwargs
            )
            return dataset, prefetch_chunk_dataset, dataset_info.weight

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_dataset_info, self.dataset_info_list))

        for dataset, prefetch_chunk_dataset, weight in results:
            self.datasets.append(dataset)
            self.prefetch_chunk_datasets.append(prefetch_chunk_dataset)
            weights.append(weight)
            self.name_to_datasets[prefetch_chunk_dataset.dataset_info.name] = dataset
        
        weights = np.array(weights)
        self.dataset_weights = weights / weights.sum()
        self.sampler_type = sampler_type

        
        self.current_samples = np.zeros(len(self.dataset_weights), dtype=np.int64)
        self.sample_idx = 0
        self.global_current_samples = np.zeros(len(self.dataset_weights), dtype=np.int64)
        self.global_sample_idx = 0
        
        self.kwargs = kwargs

        if dp_group is not None:
            self.init_broadcast(dp_group)

    def init_broadcast(self, dp_group):
        def get_broadcast_data(prefetch_chunk_dataset: PrefetchChunkDataset):
            prefetch_chunk_dataset.init_from_local()
            return prefetch_chunk_dataset.mbtable_partition.to_broadcast_data()
        
        broadcast_list = [0]*len(self.datasets)
        if self.context.rank == 0:
            start_time = time.time()
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(get_broadcast_data, dataset): i for i, dataset in enumerate(self.prefetch_chunk_datasets)}
                for future in as_completed(futures):
                    idx = futures[future]
                    try:
                        broadcast_list[idx] = future.result()
                    except Exception as e:
                        logger.error(f"Dataset initialization failed at path {self.prefetch_chunk_datasets[idx].dataset_info.path} with error: {e}")
            elapsed_time = time.time() - start_time
            logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initialized mbtable partitions. Time taken: {elapsed_time:.2f} seconds")
            logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Broadcasting mbtable partitions to other ranks: {broadcast_list}")
        broadcast_start_time = time.time()
        try:
            import bmtrain
            bmt_init = bmtrain.init.is_initialized()
        except:
            bmt_init = False
        if bmt_init:
            for idx in range(len(broadcast_list)):
                broadcast_list[idx] = bmtrain.store.broadcast_object(broadcast_list[idx], bmtrain.config['comm'], src=0) 
        else:
            torch.distributed.broadcast_object_list(broadcast_list, src=0)
        broadcast_elapsed_time = time.time() - broadcast_start_time
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Broadcast completed. Time taken: {broadcast_elapsed_time:.2f} seconds")
        
        reconstruction_start_time = time.time()
        for i, dataset in enumerate(self.prefetch_chunk_datasets):
            dataset.init_from_broadcast(broadcast_list[i])
        reconstruction_elapsed_time = time.time() - reconstruction_start_time
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Reconstructed datasets from broadcast. Time taken: {reconstruction_elapsed_time:.2f} seconds")

        
    def __iter__(self):
        self.sampler = SamplerFactory.create_sampler(self.sampler_type, weights=self.dataset_weights, rank=self.context.rank, world_size=self.context.world_size, seed=self.context.seed, **self.kwargs)
        if self.sampler_type == WEIGHTED_MEGATRON_SAMPLER:
            self.sampler.resume(self.global_sample_idx, self.global_current_samples)
        for dataset in self.datasets:
            self.datasets_iter.append(iter(dataset))
        while True:
            if all(d.exhausted for d in self.prefetch_chunk_datasets):
                logger.warning(f"All dataset exhaust on rank {self.context.rank}")
                break
            idx = self.sampler()
            if self.prefetch_chunk_datasets[idx].exhausted:
                logger.warning(f"Dataset {idx} exhaust on rank {self.context.rank}")
                self.sampler.remove_index(idx)
                continue
            chosen_iter = self.datasets_iter[idx]
            try:
                data: DetailedDoc = next(chosen_iter)
                if data is None:
                    continue
                data.dataset_idx = idx
                yield data
            except StopIteration:
                continue

    def checkpoint(self):
        # checkpoint_list = []
        # for weight, dataset in zip(self.dataset_weights, self.datasets):
        #     if weight == 0:
        #         checkpoint_list.append(dataset.empty_checkpoint())
        #     else:
        #         checkpoint_list.append(dataset.checkpoint())
        checkpoint_list = [dataset.checkpoint() for dataset in self.datasets]
        return DatasetCheckpointList(
            checkpoint_list=checkpoint_list,
            world_size=self.context.world_size,
            tp_size=self.context.tp_size,
            sample_idx=self.sample_idx,
            current_samples=self.current_samples.tolist()
        )
    
    def load_checkpoint(self, dataset_checkpoint_list: DatasetCheckpointList):
        for i, checkpoint in enumerate(dataset_checkpoint_list.checkpoint_list):
            # checkpoint 中保留的顺序，可以和本次 dataset info list 不一致，我们通过 name_to_datasets 进行映射
            # 前提：dataset_info_list 中 name 不能重复；checkpoint 中 name 必须存在于 dataset_info_list 中
            self.name_to_datasets[checkpoint.dataset_info.name].load_checkpoint(checkpoint)
        if not self.kwargs.get('clear_sampler_state', False):
            # Megatron sampler 状态恢复的部分比较复杂，暂时不支持 dataset 顺序变换，weight = 0 也不能删
            # 要不然就直接设置 clear sampler state = True
            self.sample_idx = dataset_checkpoint_list.sample_idx
            self.current_samples = np.array(dataset_checkpoint_list.current_samples)
            self.global_sample_idx = dataset_checkpoint_list.global_sample_idx
            self.global_current_samples = np.array(dataset_checkpoint_list.global_current_samples)
        
    def update(self, consumed_sample_indexes: List[Tuple[int, Dict[Chunk, List[int]]]], last_samples: Dict[int, LastSample]={}):
        '''
        Update dataset checkpoint with consumed samples and last samples in this batch.

        Args:
            consumed_samples: [(dataset_idx, samples), ...]
                - A list where each element represents a sampling action that contributes to a batch.
                - Each element is a tuple:
                    - dataset_idx: The index of the dataset from which samples are taken.
                    - samples: A dictionary where:
                        - key: The Chunk(epoch, start, stop) within the dataset.
                        - value: A list of indexes within the chunk.
                        - EXAMPLE: {Chunk(0, 0, 16): [0, 1, 2], Chunk(0, 16, 32): [16, 17, 18]}

            last_samples: {dataset_idx: LastSample, ...}
                - A dictionary mapping each dataset index to its last partially read sample.
                - LastSample represents the last sample that was not fully consumed in the batch.

                # NOTE: last_samples are used only in scenarios where the raw data is segmented 
                # into multiple lines. This ensures that during resumption, each batch can be 
                # exactly reproduced.
        '''
        for dataset_idx, indexes in consumed_sample_indexes:
            self.datasets[dataset_idx].update(indexes, last_samples.get(dataset_idx, None))
            self.sample_idx += 1
            self.current_samples[dataset_idx] += 1
            
    def __len__(self):
        return sum(len(dataset) for dataset in self.datasets)
    
    def get_path_len_map(self):
        return {dataset.path: len(dataset) for dataset in self.prefetch_chunk_datasets}
    
    def get_chunk_size_map(self):
        return {self.prefetch_chunk_datasets[i].path: self.prefetch_chunk_datasets[i].chunk_size for i, weight in enumerate(self.dataset_weights)}

if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)

    dataset_info_list = [
        DatasetInfo(
            path="tmp.sstable",
            weight=1,
            max_epoch=1
        )
    ]
    
    dataset_info_list = DatasetInfoList(dataset_info_list=dataset_info_list)
    
    dataset = WeightedDataset(
        context=context,
        dataset_info_list=dataset_info_list,
        segment_type=NO_SEGMENT,
        sampler_type=WEIGHTED_SAMPLER,
    )

    for data in dataset:
        for mm_doc in data.mm_doc_seq.doc_seq:
            print(mm_doc.dtype)
            print(mm_doc.shape)
            print(np.array(mm_doc.token_info).shape)
