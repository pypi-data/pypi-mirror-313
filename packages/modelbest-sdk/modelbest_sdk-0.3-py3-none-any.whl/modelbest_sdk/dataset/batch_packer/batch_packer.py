from collections import defaultdict
import hashlib
import torch


class BatchPacker:
    def __init__(self, batch_size: int, max_len: int, dataset_cnt: int, **kwargs):
        self.hash_to_tag = defaultdict()
    
    def encode_tags(self, token_ids_len, tag):
        tag_hash = self._get_tag_hash(tag)
        self.hash_to_tag[tag_hash] = tag
        return torch.full((token_ids_len,), tag_hash, dtype=torch.int64)
    
    def _get_tag_hash(self, tag: str) -> int:
        hash_obj = hashlib.sha256(tag.encode('utf-8'))
        return int(hash_obj.hexdigest(), 16) & ((1 << 63) - 1)        
            