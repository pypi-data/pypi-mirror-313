from typing import Dict, List
import torch

from modelbest_sdk.dataset.prefetch_chunk_dataset import PrefetchChunkDataset
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT, NO_SEGMENT, SegmentFactory
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.constant import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk, DatasetCheckpoint, LastSample
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext


class SegmentDataset(torch.utils.data.IterableDataset):
    def __init__(
        self, 
        prefetch_chunk_dataset: PrefetchChunkDataset, 
        segment_type=NO_SEGMENT, 
        max_len=1024,
        **kwargs
        ):
        self.name = prefetch_chunk_dataset.dataset_info.name
        self.prefetch_chunk_dataset = prefetch_chunk_dataset
        
        self.segment = SegmentFactory.create_segment(segment_type, max_len, drop_last=False, **kwargs)
        self.load_last_sample = None
        self.last_sample = None

    def __iter__(self):
        for detailed_doc in self.prefetch_chunk_dataset:
            detailed_doc: DetailedDoc
            if not detailed_doc.deserialize():
                continue
            detailed_doc.tag_or_default([self.name])
            if self.load_last_sample is not None and detailed_doc.position.chunk == self.load_last_sample.chunk and detailed_doc.position.index == self.load_last_sample.index:
                _, detailed_doc = detailed_doc.split(self.load_last_sample.offset)
                self.load_last_sample = None
            for data in self.segment(detailed_doc):
                if data is not None:
                    yield data 
    
    def checkpoint(self):
        ckpt = self.prefetch_chunk_dataset.checkpoint()
        ckpt.last_sample = self.last_sample
        return ckpt
    
    def empty_checkpoint(self):
        return self.prefetch_chunk_dataset.empty_checkpoint()
    
    def load_checkpoint(self, checkpoint: DatasetCheckpoint):
        self.prefetch_chunk_dataset.load_checkpoint(checkpoint)
        self.load_last_sample = checkpoint.last_sample
        self.last_sample = self.load_last_sample
            
    def update(self, consumed_sample_indexes: Dict[Chunk, List[int]], last_sample: LastSample):
        self.prefetch_chunk_dataset.update(consumed_sample_indexes)
        self.last_sample = last_sample
    
    def __len__(self):
        return len(self.prefetch_chunk_dataset)
    
    
                
if __name__ == '__main__':

    dataset = SegmentDataset(
        context=DatasetContext(),
        path='human.BaseDoc.sstable',
        max_epoch=1,
        segment_type=FIXED_LENGTH_SEGMENT,
        max_len=16
    )
    i = 0
    for data in dataset:
        print(data)
        i += 1
        if i == 100:
            break