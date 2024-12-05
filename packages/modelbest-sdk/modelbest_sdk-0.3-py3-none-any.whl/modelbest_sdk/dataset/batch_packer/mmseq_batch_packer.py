from collections import defaultdict
import io
from PIL import Image
from typing import Dict, Generator, List, Tuple
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer import BatchPacker
from modelbest_sdk.dataset.constant import *
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc, DocType, Position
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk


class MmSeqBatchPacker(BatchPacker):
    def __init__(self, batch_size, max_len, dataset_cnt, **kwargs):
        self.max_len = max_len
        self.dataset_cnt = dataset_cnt
        for k, v in kwargs.items():
            setattr(self, k, v)
            print(f"{k}={v}")


    def __call__(self, detailed_doc: DetailedDoc=None) -> Generator[DetailedDoc, None, None]:
        if detailed_doc is None:
            return
        print(f"usage: {detailed_doc.usage}")
        if detailed_doc.proto_type == BASE_DOC:
            print('we could pack base doc as well')
            print(detailed_doc.base_doc)
            return
        tokens = torch.zeros(self.max_len + 1, dtype=torch.long)
        mask = torch.ones(self.max_len + 1, dtype=torch.bool)
        position_ids = torch.zeros(self.max_len + 1, dtype=torch.long)
        img_idx = 0
        img_list = []
        img_bounds = []
        span_begin, span_end = 0, 0
        for mmdoc in detailed_doc.mm_doc_seq.doc_seq:
            if mmdoc.dtype == DocType.TXT:
                print(mmdoc.text)
                # txt_token = mmdoc.token_info
                # span_end = span_begin + len(txt_token)
                # tokens[span_begin:span_end] = torch.tensor(txt_token)
                mask[span_begin:span_end] = 0 # calculate loss 
                # print(mmdoc)
                # print(txt_token)
            elif mmdoc.dtype == DocType.IMG:
                image_size = mmdoc.image.size
                place_holder = get_placeholder(image_size=image_size, image_index=img_idx)
                img_idx += 1
                span_end = span_begin + len(place_holder)
                tokens[span_begin:span_end] = torch.tensor(place_holder)
                mask[span_begin:span_end] = 1 # not calculate loss 
                img_list.append(mmdoc.image)
                img_bounds.append((span_begin, span_end))
                # print(f"image_size={image_size}")
                # print(f"place_holder={place_holder}")
                # print(f"image={mmdoc.image}")
            span_begin = span_end

            
        position_ids[:span_end] = torch.arange(span_end)
        indexes: Tuple[int, Dict[Chunk, List[int]]] = (detailed_doc.dataset_idx, detailed_doc.indexes_dict)
        yield {
            'tokens': tokens[:-1],
            'labels': tokens[1:],
            'loss_mask': (~mask[:-1]).float(),
            'position_ids': position_ids[:-1],
            'image_list': img_list,
            'image_bounds': img_bounds,
            'indexes': indexes,
            'dataset_id': torch.tensor(detailed_doc.dataset_idx),
        }
        
    @staticmethod
    def collate_fn(batch):
        batched_data = {k: [] for k in batch[0]}
        
        for item in batch:
            for key in item:
                batched_data[key].append(item[key])

        # 对于可以直接转换为张量的数据，使用 torch.stack
        for key in ['tokens', 'labels', 'loss_mask', 'position_ids', 'dataset_id']:
            batched_data[key] = torch.stack(batched_data[key])
        return batched_data

import math

scale_resolution = 448
max_slice_nums = 9
query_len = 64
im_start_token_id = 128010
im_end_token_id = 128011
unk_token_id = 128002
slice_start_token_id = 128020
slice_end_token_id = 128021
im_id_start_token_id = 128022
im_id_end_token_id = 128023
new_schema = True
use_image_id = True


def get_image_placeholder(use_im_start_end=False):
    if use_im_start_end:
        return [im_start_token_id] + [unk_token_id] * query_len + [im_end_token_id]
    else:
        return [unk_token_id] * query_len


def get_slice_image_placeholder(use_im_start_end=False):
    if use_im_start_end:
        return [slice_start_token_id] + [unk_token_id] * query_len + [slice_end_token_id]
    else:
        return [unk_token_id] * query_len


_image_placeholder = get_image_placeholder(True)
_slice_placeholder = get_slice_image_placeholder(True)


def get_sliced_grid(image_size):
    original_width, original_height = image_size
    log_ratio = math.log(original_width / original_height)
    ratio = original_width * original_height / (scale_resolution * scale_resolution)
    multiple = min(math.ceil(ratio), max_slice_nums)
    if multiple <= 1:
        return None
    candidate_split_grids_nums = []
    for i in [multiple - 1, multiple, multiple + 1]:
        if i == 1 or i > max_slice_nums:
            continue
        candidate_split_grids_nums.append(i)
    
    candidate_grids = []
    for split_grids_nums in candidate_split_grids_nums:
        m = 1
        while m <= split_grids_nums:
            if split_grids_nums % m == 0:
                candidate_grids.append([m, split_grids_nums // m])
            m += 1

    best_grid = [1, 1]
    min_error = float("inf")
    for grid in candidate_grids:
        error = abs(log_ratio - math.log(grid[0] / grid[1]))
        if error < min_error:
            best_grid = grid
            min_error = error
    
    return best_grid


def get_grid_placeholder(grid):
    if grid is None:
        return []

    cols = grid[0]
    rows = grid[1]
    slices = []
    for i in range(rows):
        lines = []
        for j in range(cols):
            lines.append(_image_placeholder if not new_schema else _slice_placeholder)
        slices.append(sum(lines, []))
    
    if not new_schema:
        slice_placeholder = [slice_start_token_id] + sum(slices, []) + [slice_end_token_id]
    else:
        slice_placeholder = sum(slices, [])
    return slice_placeholder


def get_image_id_placeholder(idx):
    if use_image_id:
        return [im_id_start_token_id, idx, im_id_end_token_id]
    else:
        return []


def get_placeholder(image_size, image_index):
    grid = get_sliced_grid(image_size=image_size)
    return get_image_id_placeholder(image_index) \
        + _image_placeholder \
        + get_grid_placeholder(grid=grid)