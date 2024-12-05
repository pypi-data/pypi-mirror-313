from collections import defaultdict
from contextlib import ExitStack
import itertools
import math
import random
import threading
import time
from typing import List
import torch
from modelbest_sdk.dataset.common.cache import AllCached, CacheFull, CacheNotFilled, PrefetchCache
from modelbest_sdk.dataset.common.range import Range
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc, Position
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.file_format.mbtable import MbTable, MbTableIterator, TwinMbTable, TwinMbTableListIterator, assert_path_exists
from modelbest_sdk.file_format.mbtable_partition import MbTablePartition, MbTablePartitionIterator

LARGE_RECORD_SIZE = 100 * 1024 * 1024 # 100MB

logger = logging.getLogger(__name__)
class PrefetchChunkDataset(torch.utils.data.IterableDataset):
    def __init__(
        self, 
        context: DatasetContext, 
        dataset_info: DatasetInfo,
        prefetch_chunk_cnt=2, 
        chunk_size=1024,
        dp_group=None,
        cache_size=500 * 1024 * 1024,
        **kwargs
        ):
        
        self.context = context
        self.path = dataset_info.path
        self.max_epoch = dataset_info.max_epoch
        self.proto_type = dataset_info.proto_type
        self.usage = dataset_info.usage
        self.dataset_info = dataset_info
        self.prefetch_chunk_cnt = prefetch_chunk_cnt
        self.chunk_size = chunk_size
        self.use_dp_group = True if dp_group else False
        self.num_workers = max(1, self.context.num_workers)
        self.cache_size = cache_size
        
        self.cache = None
        self.exhausted = False
        self.used = Used()

        self.is_twin_mbtable = False
        self.kwargs = kwargs

        if not self.use_dp_group:
            self.init_from_local()
        
    def init_from_local(self):
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initializing dataset {self.path}")
        self.is_dir = os.path.isdir(self.path)
        if self.is_dir:
            assert_path_exists(self.path)
            self.mbtable_partition = MbTablePartition(self.path)
            self._length = self.mbtable_partition.get_total_count()
        else:
            if self.use_dp_group:
                assert self.is_dir, "dataset must be a directory to use dp_group broadcast acceleration"
            if os.path.exists(self.path):
                self.mbtable = MbTable(self.path)
                self._length = len(self.mbtable)
            elif self.proto_type == ZIP:
                print(f'{self.path} is zip format, make sure you implement udd')
                path_list = self.path.split(",")
                self.mbtable_partition_zip = [MbTablePartition(path) for path in path_list]
                self._length = self.mbtable_partition_zip[0].get_total_count()
            else:
                print(f'{self.path} not found, trying single twin table format')
                self.twin_mbtable = TwinMbTable(self.path)
                self._length = len(self.twin_mbtable)
                self.is_twin_mbtable = True

        self.chunk_size, self.num_chunks = self.safe_chunk_size(self.chunk_size)
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initialized dataset {self.path}")
        
    def init_from_broadcast(self, broadcast_data):
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initializing dataset from broadcast {self.path}")
        self.is_dir = True
        self.mbtable_partition = MbTablePartition.from_broadcast_data(broadcast_data)
        self._length = self.mbtable_partition.get_total_count()
        self.chunk_size, self.num_chunks = self.safe_chunk_size(self.chunk_size)
        logger.debug(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initialized dataset from broadcast {self.path}")
    
    def __len__(self):
        return self._length
    
    def get_chunk_data(self, chunk, cache_size):
        assert isinstance(chunk, Chunk)
        start_index = chunk.current
        max_iter = chunk.stop - chunk.current
        ret = []
        total_size = 0
        chunk_current = None
        # print(f"start_index: {start_index}, max_iter: {max_iter}")
        if self.is_dir:
            with MbTablePartitionIterator(self.mbtable_partition, start_index, max_iter) as iter:
                for i, record in enumerate(iter):
                    if len(record) > LARGE_RECORD_SIZE:
                        print(f"RECORD TOO LARGE! {chunk}: {start_index + i} size {len(record)} Bytes is larger than {LARGE_RECORD_SIZE} Bytes, from {self.path}")
                    ret.append(record)
                    total_size += len(record)
                    if total_size > cache_size:
                        chunk_current = start_index + i + 1
                        break
                    # TODO: zhaohanqing, same logic for next two
        elif self.proto_type == ZIP:
            with ExitStack() as stack:
                iters = [stack.enter_context(MbTablePartitionIterator(mbtable_partition, start_index, max_iter)) for mbtable_partition in self.mbtable_partition_zip]
                for records in zip(*iters):
                    ret.append(records)
        elif self.is_twin_mbtable:
            with TwinMbTableListIterator(self.twin_mbtable, start_index, max_iter) as iter:
                for record in iter:
                    ret.append(record)
        else:
            with MbTableIterator(self.path, start_index, max_iter) as iter:
                for record in iter:
                    ret.append(record)
        remain_chunk = None
        if chunk_current is not None and chunk_current < chunk.stop:
            remain_chunk = Chunk(chunk.epoch, chunk.start, chunk.stop, chunk_current)
        return ret, remain_chunk
    
    def __iter__(self):
        self.init_epoch()
        prefetch_thread = threading.Thread(target=self.prefetch)
        prefetch_thread.daemon = True
        prefetch_thread.start()
        while True:
            try:
                chunk_data = self.cache.get()
                for data in chunk_data:
                    yield data
            except CacheNotFilled:
                time.sleep(0.1)
            except StopIteration:
                self.exhausted = True
                return
    
    def init_epoch(self):
        if self.max_epoch is not None and self.used.epoch >= self.max_epoch:
            self.exhausted = True
        self.cache = PrefetchCache(size=self.prefetch_chunk_cnt)
        epoch_iterator = itertools.count(start=self.used.epoch) if self.max_epoch is None else range(self.used.epoch, self.max_epoch)
        chunks = itertools.chain.from_iterable(
            (self.random_chunks(epoch) for epoch in epoch_iterator)
        )
        chunks = itertools.filterfalse(
            lambda chunk: chunk in self.used.done.get(chunk.epoch, set()), chunks
        )
        self.cache.submit(chunks)

    def safe_chunk_size(self, chunk_size):
        assert chunk_size & (chunk_size - 1) == 0, f"chunk_size must be a power of 2, but got {chunk_size}"
        total_workers = self.num_workers * self.context.world_size
        if self._length < total_workers:
            raise ValueError(
                f"more concurrent loaders ({total_workers}) than " f"data entries ({self._length}) in '{self.path}'"
            )
        num_chunks = math.ceil(self._length / chunk_size)
        if num_chunks <= total_workers:
            chunk_size = self._length // total_workers
            chunk_size = 1 << (chunk_size.bit_length() - 1)
            num_chunks = math.ceil(self._length / chunk_size)
        return chunk_size, num_chunks

    def random_chunks(self, epoch):
        random.seed(self.context.seed)
        world_size = self.context.world_size
        rank = self.context.rank
        num_workers, worker_id = get_worker_info()
        # we only iteratre through start ids as they uniquely mark each slice
        r = Range(0, len(self), self.chunk_size)
        # split index among multi-gpu workers
        r = r.subrange(split=rank, nsplits=world_size)
        # split index among multi-process dataloader workers
        r = r.subrange(split=worker_id, nsplits=num_workers)
        # obtain random chunks
        chunks = (Chunk(epoch, st, min(st + self.chunk_size, len(self))) for st in r.random_iterate())
        return chunks

    def prefetch(self):
        while True:
            try:
                chunk = self.cache.pull_task()
                chunk_data, remain_chunk = self.get_chunk_data(chunk, self.cache_size)
                if remain_chunk is not None:
                    self.cache.push_task(remain_chunk)
                unused_chunk_data = [
                    DetailedDoc(position=Position(chunk, i), raw=data, proto_type=self.proto_type, usage=self.usage, dataset_info=self.dataset_info)
                    for i, data in zip(range(chunk.current, chunk.stop), chunk_data)
                    if (data is not None) and (i not in self.used.active.get(chunk, set()))
                ]
                self.cache.put_result(unused_chunk_data)
            except CacheFull:
                time.sleep(0.1)
            except AllCached:
                break

    def checkpoint(self):
        return DatasetCheckpoint(
            dataset_info=self.dataset_info,
            used=self.used, 
            chunk_size=self.chunk_size,
            num_chunks=self.num_chunks,
            )
    
    def empty_checkpoint(self):
        return DatasetCheckpoint(
            dataset_info=self.dataset_info,
            used=Used(),
            chunk_size=self.chunk_size,
            num_chunks=self.num_chunks,
            )
    
    def load_checkpoint(self, checkpoint: DatasetCheckpoint):

        assert checkpoint.chunk_size & (checkpoint.chunk_size - 1) == 0, f"chunk_size must be a power of 2, but got {checkpoint.chunk_size}"
        
        if self.chunk_size == checkpoint.chunk_size:
            self.used = checkpoint.used
            
        elif self.chunk_size > checkpoint.chunk_size:
            assert self.chunk_size % checkpoint.chunk_size == 0
            for epoch in checkpoint.used.done.keys():
                merge_chunk_map = defaultdict(set)
                for chunk in checkpoint.used.done[epoch]:
                    merge_start = chunk.start - chunk.start % checkpoint.chunk_size
                    merge_stop = min(len(self), merge_start + checkpoint.chunk_size)
                    merge_chunk_map[Chunk(epoch, merge_start, merge_stop)].add(Chunk(epoch, chunk.start, chunk.stop))
                for merge_chunk, to_merge_chunks in merge_chunk_map.items():
                    if len(to_merge_chunks) == (merge_chunk.stop - merge_chunk.start) / checkpoint.chunk_size:
                        self.used.done.setdefault(epoch, set()).add(merge_chunk)
                    else:
                        for to_merge_chunk in to_merge_chunks:
                            self.used.active.setdefault(merge_chunk, set()).update(range(to_merge_chunk.start, to_merge_chunk.stop))
            for chunk, indexes in checkpoint.used.active.items():
                merge_start = chunk.start - chunk.start % self.chunk_size
                merge_stop = min(len(self), merge_start + self.chunk_size)
                self.used.active.setdefault(Chunk(chunk.epoch, merge_start, merge_stop), set()).update(indexes)
        elif self.chunk_size < checkpoint.chunk_size:
            
            assert checkpoint.chunk_size % self.chunk_size == 0
            for epoch in checkpoint.used.done.keys():
                for chunk in checkpoint.used.done[epoch]:
                    for split_start in range(chunk.start, chunk.stop, self.chunk_size):
                        self.used.done.setdefault(epoch, set()).add(Chunk(epoch, split_start, min(split_start + self.chunk_size, len(self))))
            for chunk, indexes in checkpoint.used.active.items():
                for split_start in range(chunk.start, chunk.stop, self.chunk_size):
                    split_stop = min(len(self), split_start + self.chunk_size)
                    split_indexes = set(filter(lambda x: x >= split_start and x < split_stop, indexes))
                    if len(split_indexes) == split_stop - split_start:
                        self.used.done.setdefault(chunk.epoch, set()).add(Chunk(chunk.epoch, split_start, split_stop))
                    else:
                        self.used.active.setdefault(Chunk(chunk.epoch, split_start, split_stop), set()).update(split_indexes)
                    
        if len(checkpoint.used.active) == 0 and len(checkpoint.used.done) == 0:
            self.used.epoch = 0
        else:
            epochs_not_exhausted = set()
            for chunk in checkpoint.used.active.keys():
                epochs_not_exhausted.add(chunk.epoch)
            epoch = 0
            for epoch in sorted(list(checkpoint.used.done.keys())):
                if len(checkpoint.used.done[epoch]) == checkpoint.num_chunks:
                    del checkpoint.used.done[epoch]
                else:
                    epochs_not_exhausted.add(epoch)
                    break
            epochs_not_exhausted.add(epoch + 1)
            self.used.epoch = min(epochs_not_exhausted, default=0)

    def update(self, consumed_sample_indexes: Dict[Chunk, List[int]]):
        for chunk, indexes in sorted(consumed_sample_indexes.items(), key=lambda x: x[0].epoch): # chunk with lower epoch comes first
            assert chunk not in self.used.done, f"chunk {chunk} has been done in dataset {self.path} on rank {self.context.rank}, cannot update"
            self.used.active.setdefault(chunk, set()).update(set(indexes))
            
            if len(self.used.active[chunk]) == chunk.stop - chunk.start:
                self.used.done.setdefault(chunk.epoch, set()).add(chunk)
                del self.used.active[chunk]
                
            for epoch in range(chunk.epoch - 1, -1, -1):
                cur_chunk = Chunk(epoch, chunk.start, chunk.stop)
                if cur_chunk in self.used.active:
                    # Note that, if data contains None, it will be filtered out in prefetch, 
                    # active chunk with lower epoch may not len(chunk) == (chunk.stop - chunk.start), but it is still done
                    del self.used.active[cur_chunk]
                    self.used.done.setdefault(epoch, set()).add(cur_chunk)
                else:
                    break

def get_worker_info():
    worker_info = torch.utils.data.get_worker_info()
    if worker_info is None:
        num_workers, worker_id = 1, 0
    else:
        num_workers, worker_id = worker_info.num_workers, worker_info.id
    return num_workers, worker_id


if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)
    dataset_info = DatasetInfo(
        path="example/mbtable_data/base_doc_simple",
        max_epoch=3
    )
    dataset = PrefetchChunkDataset(
        context=context, 
        dataset_info=dataset_info
    )
    i = 0
    for data in dataset:
        data: DetailedDoc
        consumed_sample_indexes = {data.position.chunk: set([data.position.index])}
        dataset.update(consumed_sample_indexes=consumed_sample_indexes)
        i += 1
        if i == 30:
            checkpoint = dataset.checkpoint()
            break
    
    print(checkpoint)
    dataset_next = PrefetchChunkDataset(
        context=context, 
        dataset_info=dataset_info
    )
    dataset_next.load_checkpoint(checkpoint)
    for data in dataset_next:
        consumed_sample_indexes = {data.position.chunk: set([data.position.index])}
        dataset_next.update(consumed_sample_indexes=consumed_sample_indexes)
        i += 1
        if i == 60:
            break
    checkpoint = dataset_next.checkpoint()
    print(checkpoint)