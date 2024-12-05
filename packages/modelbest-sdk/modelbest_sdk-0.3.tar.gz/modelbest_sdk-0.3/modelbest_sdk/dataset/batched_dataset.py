from collections import defaultdict
import hashlib
import numpy as np
import torch

# from modelbest_sdk.dataset.collater.collater import Collater
from modelbest_sdk.dataset.batch_packer.batch_packer_factory import CPM_FLASH_ATTN_BATCH_PACKER, BatchPackerFactory
from modelbest_sdk.dataset.batch_packer.cpm_flash_attn_batch_packer import CpmFlashAttnBatchPacker
from modelbest_sdk.dataset.batch_packer.megatron_batch_packer import MegatronBatchPacker
from modelbest_sdk.dataset.sampler.sampler_factory import WEIGHTED_MEGATRON_SAMPLER, WEIGHTED_SAMPLER
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc, DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext


class BatchedDataset(torch.utils.data.IterableDataset):
    def __init__(self, context, weighted_dataset: WeightedDataset, batch_size, max_len, batch_packer_type=CPM_FLASH_ATTN_BATCH_PACKER, drop_last=False, **kwargs):
        self.context = context
        self.weighted_dataset = weighted_dataset
        self.drop_last = drop_last
        self.dataset_cnt = len(self.weighted_dataset.dataset_info_list)
        self.batch_packer_type = batch_packer_type
        self.batch_size = batch_size
        self.max_len = max_len
        self.kwargs = kwargs
        

    def __iter__(self):
        self.batch_packer = BatchPackerFactory.create_batch_packer(self.batch_packer_type, self.batch_size, self.max_len, self.dataset_cnt, **self.kwargs)
        for data in self.weighted_dataset:
            data: DetailedDoc
            for batch in self.batch_packer(data):
                yield batch
                
        if not self.drop_last:
            for batch in self.batch_packer():
                yield batch
    
    def collate_fn(self, batch):
        return BatchPackerFactory.collate_fn(self.batch_packer_type)(batch)


if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)

    dataset_info_list = [
        DatasetInfo(
            path="human.BaseDoc.sstable",
            weight=1,
            max_epoch=1
        ),
        DatasetInfo(
            path="hot_chars.BaseDoc.sstable",
            weight=2,
            max_epoch=2
        )
    ]
    
    dataset_info_list = DatasetInfoList(dataset_info_list)
    
    w_dataset = WeightedDataset(
        context=context,
        dataset_info_list=dataset_info_list,
        segment_type=FIXED_LENGTH_SEGMENT,
        sampler_type=WEIGHTED_MEGATRON_SAMPLER,
        max_len=8192
    )
    
    dataset = BatchedDataset(
        context=context,
        weighted_dataset=w_dataset,
        batch_size=1,
        max_len=8192
    )
    
    for data in dataset:
        print(data)
        # print(data['indexes'].keys())
        # print(data['indexes'].values())
    