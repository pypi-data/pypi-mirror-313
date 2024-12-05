import os
import sys
import unittest

from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetInfo

cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.abspath(os.path.join(cur_path, '../')))

from modelbest_sdk.dataset.prefetch_chunk_dataset import PrefetchChunkDataset
from modelbest_sdk.dataset.segment.segment_factory import CONDITIONAL_FIXED_LENGTH_SEGMENT, NO_SEGMENT, FIXED_LENGTH_SEGMENT
from modelbest_sdk.dataset.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder
from test.test_base import TestBase


class TestSegment(TestBase):
    def test_no_segment(self):
        TestBase.generate_data(dataset_path='/tmp/no_segment', file_count=1, doc_count_per_file=10, token_count=10, token_offset=1000, mask_pattern='text')
        context = DatasetContext()
        dataset_info = DatasetInfo('/tmp/no_segment', max_epoch=1)
        p_dataset = PrefetchChunkDataset(context, dataset_info)
        dataset = SegmentDataset(
            p_dataset,
            segment_type=NO_SEGMENT,
            max_len=16
        )
        for data in dataset:
            base_doc = data.base_doc
            expected_token_ids = list(range(1000, 1010))
            assert base_doc.token_ids == expected_token_ids, f"Token IDs do not match. Expected: {expected_token_ids}, Got: {base_doc.token_ids}"
            expected_mask = [False] * 9 + [True]
            assert base_doc.mask == expected_mask, f"Mask does not match. Expected: {expected_mask}, Got: {base_doc.mask}"
    
    def test_fixed_length_segment(self):
        max_len = 16
        token_count = 10
        TestBase.generate_data(dataset_path='/tmp/fixed_length_segment', file_count=1, doc_count_per_file=10, token_count=token_count, token_offset=1000, mask_pattern='text')
        context = DatasetContext()
        dataset_info = DatasetInfo('/tmp/fixed_length_segment', max_epoch=1)
        p_dataset = PrefetchChunkDataset(context, dataset_info)
        dataset = SegmentDataset(
            p_dataset,
            segment_type=FIXED_LENGTH_SEGMENT,
            max_len=16
        )
        start_idx = 0
        expected_token_ids = list(range(1000, 1000+token_count))
        expected_mask = [False] * (token_count - 1) + [True]
        concatenated_token_ids = expected_token_ids * 10
        concatenated_mask = expected_mask * 10
        for data in dataset:
            token_ids = data.base_doc.token_ids
            mask = data.base_doc.mask
            assert len(token_ids) == max_len + 1, f"Token IDs length does not match. Expected: {max_len + 1}, Got: {len(token_ids)}"
            assert len(mask) == max_len + 1, f"Mask length does not match. Expected: {max_len + 1}, Got: {len(mask)}"
            assert token_ids == concatenated_token_ids[start_idx:start_idx + max_len + 1], f"Token IDs do not match. Expected: {concatenated_token_ids[start_idx:start_idx + max_len + 1]}, Got: {token_ids}"
            assert mask == concatenated_mask[start_idx:start_idx + max_len + 1], f"Mask does not match. Expected: {concatenated_mask[start_idx:start_idx + max_len + 1]}, Got: {mask}"
            start_idx += max_len
            
    def test_conditional_fixed_length_segment(self):
        max_len = 16
        token_count = 5 
        # 5, 10, 15, and the last token could not fit into the fixed length segment
        TestBase.generate_data(dataset_path='/tmp/conditional_fixed_length_segment', file_count=1, doc_count_per_file=10, token_count=token_count, token_offset=1000, mask_pattern='instruction')
        context = DatasetContext()
        dataset_info = DatasetInfo('/tmp/conditional_fixed_length_segment', max_epoch=1)
        p_dataset = PrefetchChunkDataset(context, dataset_info)
        dataset = SegmentDataset(
            p_dataset,
            segment_type=CONDITIONAL_FIXED_LENGTH_SEGMENT,
            max_len=16
        )
        expected_token_ids = list(range(1000, 1005)) * 3
        expected_mask = ([True] * 2 + [False] * 2 + [True]) * 3
        for data in dataset:
            token_ids = data.base_doc.token_ids
            mask = data.base_doc.mask
            assert len(token_ids) == token_count * 3, f"Token IDs length does not match. Expected: {token_count * 3}, Got: {len(token_ids)}"
            assert len(mask) == token_count * 3, f"Mask length does not match. Expected: {token_count * 3}, Got: {len(mask)}"
            assert token_ids == expected_token_ids, f"Token IDs do not match. Expected: {expected_token_ids}, Got: {token_ids}"
            assert mask == expected_mask, f"Mask does not match. Expected: {expected_mask}, Got: {mask}"


if __name__ == '__main__':
    unittest.main()
