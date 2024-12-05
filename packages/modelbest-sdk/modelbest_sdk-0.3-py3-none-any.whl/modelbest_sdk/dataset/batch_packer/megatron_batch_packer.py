from collections import defaultdict
from typing import Dict, Generator, List, Tuple
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer import BatchPacker
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc, Position
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk


class MegatronBatchPacker(BatchPacker):
    def __init__(self, batch_size, max_len, dataset_cnt, **kwargs):
        self.max_len = max_len
        self.attention_mask = self._create_attention_mask(max_len)
        self.dataset_cnt = dataset_cnt

    def _create_attention_mask(self, max_len):
        mask = torch.tril(torch.ones((max_len, max_len))).unsqueeze(0) < 0.5
        return mask

    def _create_position_ids(self, max_len_plus_one: int, positions: List[Position]) -> torch.Tensor:
        total_len = 0
        tensors = []
        
        for position in positions:
            length = position.length
            tensors.append(torch.arange(length))
            total_len += length
        
        assert total_len <= max_len_plus_one, f"total_len is {total_len}, but max_len_plus_one is {max_len_plus_one}"
        
        remaining_len = max_len_plus_one - total_len
        if remaining_len > 0:
            tensors.append(torch.arange(remaining_len))
        
        return torch.cat(tensors)


    def __call__(self, detailed_doc: DetailedDoc=None) -> Generator[DetailedDoc, None, None]:
        if detailed_doc is None:
            return
        tokens = torch.zeros(self.max_len + 1, dtype=torch.long)
        mask = torch.ones(self.max_len + 1, dtype=torch.bool) # default do not calculate loss for padding token
        actual_tokens = torch.Tensor(detailed_doc.base_doc.token_ids).long()
        actual_mask = torch.Tensor(detailed_doc.base_doc.mask).bool()
        tokens[:actual_tokens.shape[0]] = actual_tokens
        mask[:actual_mask.shape[0]] = actual_mask
        
        assert tokens.shape[0] == self.max_len + 1, f"tokens.shape[0] is {tokens.shape[0]}, but self.max_len + 1 is {self.max_len + 1}"
            
        position_ids = self._create_position_ids(self.max_len + 1, detailed_doc.positions)        
        
        indexes: Tuple[int, Dict[Chunk, List[int]]] = (detailed_doc.dataset_idx, detailed_doc.indexes_dict)
        last_sample = {detailed_doc.dataset_idx: detailed_doc.last_sample}
        yield {
            'tokens': tokens[:-1],
            'labels': tokens[1:],
            'loss_mask': (~mask[:-1]).float(),
            'attention_mask': self.attention_mask,
            'position_ids': position_ids[:-1],
            'indexes': indexes,
            'last_sample': last_sample,
            'dataset_id': torch.tensor(detailed_doc.dataset_idx)
        }
        
    def collate_fn(batch):
        batched_data = {k: [] for k in batch[0]}
        
        for item in batch:
            for key in item:
                batched_data[key].append(item[key])

        # 对于可以直接转换为张量的数据，使用 torch.stack
        for key in ['tokens', 'labels', 'loss_mask', 'attention_mask', 'position_ids', 'dataset_id']:
            batched_data[key] = torch.stack(batched_data[key])

        last_sample_aggregated_dict = defaultdict()

        for last_sample_dict in batched_data['last_sample']:
            for dataset_idx, last_sample in last_sample_dict.items():
                last_sample_aggregated_dict[dataset_idx] = last_sample # 取最后一个样本

        batched_data['last_sample'] = last_sample_aggregated_dict
        return batched_data