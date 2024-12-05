import torch
from modelbest_sdk.dataset.batch_packer.batch_packer_factory import CPM_FLASH_ATTN_BATCH_PACKER, MEGATRON_BATCH_PACKER
from modelbest_sdk.dataset.batched_dataset import BatchedDataset
from modelbest_sdk.dataset.modelbest_dataloader import ModelbestDataloader
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetInfo, DatasetInfoList
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset
from test.test_base import TestBase
import unittest


class TestBatchPacker(TestBase):
    def test_megatron_batch_packer(self):
        token_count = 10
        max_len = 16
        context = DatasetContext()
        TestBase.generate_data(dataset_path='/tmp/megatron_batch_packer', file_count=1, doc_count_per_file=10, token_count=token_count, token_offset=1000, mask_pattern='text')
        dataset_info_list = DatasetInfoList([DatasetInfo(path='/tmp/megatron_batch_packer', weight=1, max_epoch=1)])
        
        w_dataset = WeightedDataset(context, dataset_info_list, max_len=max_len, segment_type=FIXED_LENGTH_SEGMENT)
        dataset = BatchedDataset(context, weighted_dataset=w_dataset, batch_size=1, max_len=max_len, batch_packer_type=MEGATRON_BATCH_PACKER)
        start_idx = 0   
        expected_token_ids = list(range(1000, 1000+token_count))
        expected_mask = [False] * (token_count - 1) + [True]
        concatenated_token_ids = expected_token_ids * max_len
        concatenated_mask = expected_mask * max_len
        
        for batch in dataset:
            tokens = batch['tokens']
            labels = batch['labels']
            loss_mask = batch['loss_mask']
            position_ids = batch['position_ids']
            assert len(tokens) == max_len
            assert len(loss_mask) == max_len
            assert len(position_ids) == max_len
            assert len(labels) == max_len
            assert tokens.tolist() == concatenated_token_ids[start_idx:start_idx + max_len], f"Tokens do not match. Expected: {concatenated_token_ids[start_idx:start_idx + max_len]}, Got: {tokens}"
            assert labels.tolist() == concatenated_token_ids[start_idx + 1:start_idx + max_len + 1], f"Labels do not match. Expected: {concatenated_token_ids[start_idx + 1:start_idx + max_len + 1]}, Got: {labels}"
            assert (~(loss_mask.bool())).tolist() == concatenated_mask[start_idx:start_idx + max_len], f"Loss mask does not match. Expected: {concatenated_mask[start_idx:start_idx + max_len]}, Got: {loss_mask}"
            start_idx += max_len
            
            
if __name__ == '__main__':
    unittest.main()