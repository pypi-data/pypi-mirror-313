
from collections import defaultdict, deque
import hashlib
from typing import Dict, Generator, List, Tuple

import numpy as np
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer import BatchPacker
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk


class CpmFlashAttnBatchPacker(BatchPacker):
    def __init__(self, batch_size: int, max_len: int, dataset_cnt: int, **kwargs):
        super().__init__(batch_size, max_len, dataset_cnt)
        self.buffer = deque()
        self.current_length = 0
        self.max_total_length = batch_size * max_len
        self.batch_size = 1
        self.dataset_cnt = dataset_cnt

    def put(self, data: DetailedDoc):
        self.buffer.append(data)
        self.current_length += len(data.base_doc.token_ids)
        
    def pop(self) -> DetailedDoc:
        lengths = []
        indexes: List[Tuple[int, Dict[Chunk, List[int]]]] = []
        inputs = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        targets = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-100)
        dataset_ids = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-1)
        position_ids = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        tags = torch.full((self.batch_size, self.max_total_length), dtype=torch.int64, fill_value=-1)

        span_begin = 0
        while self.buffer:
            data: DetailedDoc = self.buffer.pop()
            dataset_idx = data.dataset_idx
            doc = data.base_doc
            token_ids = doc.token_ids
            mask = doc.mask
            tag = doc.tag[0] # TODO: support multiple tags
            target_ids = np.where(mask[1:], -100, token_ids[1:]).tolist() + [-100]
            span_end = span_begin + len(token_ids)
            # TODO: what if the inputs is longer than max_total_length?
            # RuntimeError: The expanded size of the tensor (16) must match the existing size (385) at non-singleton dimension 0.  Target sizes: [16].  Tensor sizes: [385]
            inputs[0, span_begin:span_end] = torch.tensor(token_ids, dtype=torch.int32)
            targets[0, span_begin:span_end] = torch.tensor(target_ids, dtype=torch.int32)
            dataset_ids[0, span_begin:span_end] = torch.tensor(dataset_idx, dtype=torch.int32)
            position_ids[0, span_begin:span_end] = torch.from_numpy(np.arange(len(token_ids), dtype=np.int32))
            lengths.append(len(token_ids))
            indexes.append((dataset_idx, data.indexes_dict))
            tags[0, span_begin:span_end] = self.encode_tags(len(token_ids), tag)
            span_begin = span_end
        cu_seqlens = torch.cat(
            [torch.tensor([0] + lengths).cumsum(dim=-1), torch.tensor([self.max_total_length], dtype=torch.int32)],
            dim=0,
        ).int()
        batch = {
            "input_ids": inputs,
            "target_ids": targets,
            "dataset_ids": dataset_ids,
            "indexes": indexes,
            "cu_seqlens": cu_seqlens,
            "max_seqlen": int(torch.max(cu_seqlens[1:] - cu_seqlens[:-1])),
            "lengths": torch.tensor(sum(lengths)).int(),
            "position_ids": position_ids,
            "tags": tags,
            "hash_to_tag": self.hash_to_tag
        }
        self.current_length = 0
        return batch
    
    
    def will_exceed(self, data: DetailedDoc):
        if data is None:
            return False
        return self.current_length + len(data.base_doc.token_ids) > self.max_total_length

    @staticmethod
    def collate_fn(batch):
        return batch[0]

    def __call__(self, detailed_doc: DetailedDoc=None, pop_last=False) -> Generator[DetailedDoc, None, None]:
        if (pop_last and self.buffer):
            yield self.pop()
        if detailed_doc is not None:
            if self.will_exceed(detailed_doc):
                yield self.pop()
            self.put(detailed_doc)
