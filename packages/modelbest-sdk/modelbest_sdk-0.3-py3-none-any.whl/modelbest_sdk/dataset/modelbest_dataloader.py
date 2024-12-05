import logging
import os
from typing import Dict, List
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer_factory import CPM_FLASH_ATTN_BATCH_PACKER
from modelbest_sdk.dataset.batched_dataset import BatchedDataset
from modelbest_sdk.dataset.sampler.sampler_factory import *
from modelbest_sdk.dataset.segment.segment_factory import *
from modelbest_sdk.dataset.constant import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetCheckpointList, DatasetInfoList, Used
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset

logger = logging.getLogger(__name__)
class ModelbestDataloader():
    def __init__(
        self,
        context: DatasetContext,
        dataset_info_list: DatasetInfoList,
        batch_size=1,
        max_len=4096,
        prefetch_chunk_cnt=2,
        chunk_size=1024,
        num_workers=1,
        prefetch_factor=4,
        cuda_prefetch=False, # @deprecated
        segment_type=NO_SEGMENT,
        sampler_type=WEIGHTED_SAMPLER,
        batch_packer_type=CPM_FLASH_ATTN_BATCH_PACKER,
        dp_group=None,
        **kwargs
    ):
        self.context = context
        self.context.num_workers = num_workers
        
        self.weighted_dataset = WeightedDataset(
            context=context, 
            dataset_info_list=dataset_info_list,
            segment_type=segment_type,
            sampler_type=sampler_type,
            max_len=max_len,
            prefetch_chunk_cnt=prefetch_chunk_cnt,
            chunk_size=chunk_size,
            dp_group=dp_group,
            **kwargs
        )
        
        self.batched_dataset = BatchedDataset(
            context=context, 
            weighted_dataset=self.weighted_dataset, 
            batch_size=batch_size, 
            max_len=max_len,
            batch_packer_type=batch_packer_type,
            drop_last=False,
            **kwargs
        )
        
        self.batch_size = 1 if batch_packer_type == CPM_FLASH_ATTN_BATCH_PACKER else batch_size
        self.dataloader = torch.utils.data.DataLoader(
            dataset=self.batched_dataset, 
            batch_size=self.batch_size,
            num_workers=num_workers,
            prefetch_factor=prefetch_factor,
            pin_memory=True,
            collate_fn=self.batched_dataset.collate_fn,
            # worker_init_fn=self.weighted_dataset.worker_init,
        )
        
        self.iterator = None

    def __iter__(self):
        self.iterator = iter(self.dataloader)
        return self
    
    def __next__(self):
        if self.iterator is None:
            self.__iter__()
        return next(self.iterator)
    
    def checkpoint(self):
        return self.weighted_dataset.checkpoint()
    
    def load_checkpoint(self, checkpoint):
        self.weighted_dataset.load_checkpoint(checkpoint)
        
    def update(self, dataset_entries, last_samples={}):
        self.weighted_dataset.update(dataset_entries, last_samples)
    
    def save(self, sub_dir=''):
        if self.context.tp_rank != 0 or self.context.pp_rank != 0:
            logger.warning("Only tp/pp rank 0 can save dataloader")
            return
        path = os.path.join(self.context.dataset_checkpoint_path, sub_dir, "dataset_ckpt", f"rank_{self.context.rank}.mbt")
        self.checkpoint().save_to_file(path)
        
    def resume(self, dir):
        # if dir empty, return
        resume_dir = os.path.join(dir, "dataset_ckpt")
        if not os.path.exists(resume_dir):
            logger.warning(f'{resume_dir} not exists, skip resume')
            return
        if os.listdir(resume_dir) == []:
            logger.warning(f'{resume_dir} is empty, skip resume')
            return
        logger.info(f'Resuming dataloader from {dir}')
        all_dataset_ckpt_dict: Dict[str, DatasetCheckpointList] = {}
        for path in os.listdir(resume_dir):
            abs_path = os.path.join(resume_dir, path)
            all_dataset_ckpt_dict[path] = DatasetCheckpointList.load_from_file(abs_path)
        
        final_ckpt = None
        first_rank_ckpt_path = f"rank_0.mbt"
        cur_rank_ckpt_name = f"rank_{self.context.rank}.mbt"
        
        # 1. check if world size change
        new_world_size = self.context.world_size
        old_world_size = all_dataset_ckpt_dict[first_rank_ckpt_path].world_size
        if new_world_size == old_world_size:
            final_ckpt = all_dataset_ckpt_dict[cur_rank_ckpt_name]
        else:
            logger.warning(f"World size changed from {old_world_size} to {new_world_size}, resuming from scratch")
            chunk_size_map = self.weighted_dataset.get_chunk_size_map()
            all_dataset_ckpt_list = [dataset_ckpt_list for dataset_ckpt_list in all_dataset_ckpt_dict.values()]
            final_ckpt = all_dataset_ckpt_list[0]
            for ckpt in final_ckpt.checkpoint_list:
                ckpt.used = Used()
            for other_dataset_ckpt in all_dataset_ckpt_list:
                final_ckpt.merge_my_chunk(other_dataset_ckpt, self.context.rank, new_world_size, chunk_size_map)
                
        # 2. check if dataset change
        new_dataset_cnt = len(self.weighted_dataset.datasets)
        old_dataset_cnt = len(all_dataset_ckpt_dict[first_rank_ckpt_path].checkpoint_list)
        if new_dataset_cnt == old_dataset_cnt and new_world_size == old_world_size:
            global_sample_index = 0
            global_current_samples_list = []
            for dataset_ckpt_list in all_dataset_ckpt_dict.values():
                global_sample_index += dataset_ckpt_list.sample_idx
                global_current_samples_list.append(dataset_ckpt_list.current_samples)
            global_current_samples = [sum(x) for x in zip(*global_current_samples_list)]
            final_ckpt.global_sample_idx = global_sample_index
            final_ckpt.global_current_samples = global_current_samples
        else:
            logger.warning("Dataset or world size change detected, reset sampler state")
            final_ckpt.global_sample_idx = 0
            final_ckpt.global_current_samples = [0] * new_dataset_cnt
            final_ckpt.sample_idx = 0
            final_ckpt.current_samples = [0] * new_dataset_cnt
            
        self.weighted_dataset.load_checkpoint(final_ckpt)
        logger.info(f'Successfully resume dataloader from {dir}')

    
    def progress(self, global_checkpoint: List[DatasetCheckpointList]):
        # This is a approximate progress calculation
        # This is used after:
        #   global_ckpt_list = [_ for _ in range(world_size)]
        #   dist.all_gather_object(global_ckpt_list, dataloader.checkpoint())
        #   dataloader.progress(global_ckpt_list)
        # or other all gather functions

        merged_ckpt = None
        for ckpt in global_checkpoint:
            if merged_ckpt is None:
                merged_ckpt = ckpt
            else:
                merged_ckpt.merge(ckpt)
        
        path_len_map = self.weighted_dataset.get_path_len_map()
        progress_dict = {}

        for checkpoint in merged_ckpt.checkpoint_list:
            dataset_info = checkpoint.dataset_info
            used = checkpoint.used
            total_samples_per_epoch = path_len_map[dataset_info.path]
            consumed_samples = 0
            
            for chunk, index_set in used.active.items():
                consumed_samples += len(index_set)
            min_epoch = 2048 if used.done else 0
            for epoch, chunk_set in used.done.items():
                min_epoch = min(min_epoch, epoch)
                for chunk in chunk_set:
                    consumed_samples += (chunk.stop - chunk.start)
            if min_epoch > 0:
                consumed_samples += total_samples_per_epoch * min_epoch

            progress_percentage = consumed_samples / total_samples_per_epoch
            
            progress_dict[dataset_info.path] = {
                "samples_per_epoch": total_samples_per_epoch,
                "samples_consumed": consumed_samples,
                "progress": progress_percentage
            }
        return progress_dict