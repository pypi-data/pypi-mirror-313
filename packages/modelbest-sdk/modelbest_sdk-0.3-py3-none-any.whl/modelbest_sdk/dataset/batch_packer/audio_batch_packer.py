from collections import defaultdict, deque
import io
import logging
from typing import Dict, Generator, List, Tuple
import librosa
import numpy as np
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer import BatchPacker
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk
from modelbest_sdk.dataset.thrift_wrapper.messages import Messages, Msg

logger = logging.getLogger(__name__)
class AudioBatchPacker(BatchPacker):
    def __init__(self, batch_size, max_len, dataset_cnt, **kwargs):
        super().__init__(batch_size, max_len, dataset_cnt, **kwargs)
        self.buffer = deque()
        self.current_length = 0
        self.max_total_length = batch_size * max_len
        self.batch_size = 1
        self.dataset_cnt = dataset_cnt

        
    def put(self, data: DetailedDoc):
        print(data.usage)
        self.buffer.append(data)
        self.current_length += data.mm_doc_seq.doc_seq[0].shape[1]
        
    def pop(self):
        lengths = []
        indexes: List[Tuple[int, Dict[Chunk, List[int]]]] = []
        tokens = torch.zeros((self.batch_size, 16, self.max_total_length), dtype=torch.int32)
        mask = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.float)
        position_ids = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        doc_ids = []
        # tags = torch.full((self.batch_size, self.max_total_length), dtype=torch.int64, fill_value=-1)

        span_begin = 0
        while self.buffer:
            data: DetailedDoc = self.buffer.popleft()
            position = data.position
            dataset_idx = data.dataset_idx
            mm_doc = data.mm_doc_seq.doc_seq[0]

            messages: Messages = data.messages
            for message in messages.messages:
                message.role: str
                audio = message.content[0].value
                audio.text: str
                audio.wav : bytes
                
                audio_data =np.frombuffer(io.BytesIO(audio.wav).read(), dtype=np.int16)
                if audio_data.size == 0:
                    continue
                # 将音频数据转换为浮点数格式，因为 librosa 处理的音频数据通常是浮点数
                audio_data = librosa.util.normalize(audio_data.astype(np.float32))
                # 原始采样率
                original_sr = 22050
                # 目标采样率
                target_sr = 16000
                # 使用 librosa 进行重采样
                audio_data = librosa.resample(audio_data, orig_sr=original_sr, target_sr=target_sr)
                

            shape = mm_doc.shape
            token_info = torch.tensor(mm_doc.token_info).reshape(shape)
            # tag = mm_doc.tag[0]  # TODO: support multiple tags
            length = shape[1]
            span_end = span_begin + length
            
            tokens[0, :, span_begin:span_end] = token_info
            indexes.append((dataset_idx, data.indexes_dict))
            # tags[0, span_begin:span_end] = self.encode_tags(length, tag)
            position_ids[0, span_begin:span_end] = torch.from_numpy(np.arange(1, length + 1, dtype=np.int32))
            lengths.append(length)
            doc_ids.append(mm_doc.docid)
            span_begin = span_end
        
        mask[:, :] = 1.0
        
        cu_seqlens = torch.cat(
            [torch.tensor([0] + lengths).cumsum(dim=-1), torch.tensor([self.max_total_length], dtype=torch.int32)],
            dim=0,
        ).int()
        batch = {
            'tokens': tokens[:,:,:-1],
            'labels': tokens[:,:,1:],
            'loss_mask': mask[:, :-1],
            'position_ids': position_ids[:, :-1],
            'indexes': indexes,
            "cu_seqlens": cu_seqlens,
            "lengths": torch.tensor(sum(lengths)).int(),
            "max_seqlen": int(torch.max(cu_seqlens[1:] - cu_seqlens[:-1])),
            "doc_ids": doc_ids,
            # "tags": tags,
            # "hash_to_tag": self.hash_to_tag
        }
        self.current_length = 0
        return batch
        
    def will_exceed(self, data: DetailedDoc):
        if data is None:
            return False
        return self.current_length + data.mm_doc_seq.doc_seq[0].shape[1] > self.max_total_length

    def too_long(self, data: DetailedDoc):
        if data.mm_doc_seq.doc_seq[0].shape[1] > self.max_total_length:
            logger.warning(f"Document {data.mm_doc_seq.doc_seq[0].docid} is too long, length {data.mm_doc_seq.doc_seq[0].shape[1]} > {self.max_total_length}, truncate it.")
            return True
        return False
    
    def __call__(self, detailed_doc: DetailedDoc=None, pop_last=False) -> Generator[DetailedDoc, None, None]:
        if (pop_last and self.buffer):
            yield self.pop()
        if detailed_doc is not None:
            if self.too_long(detailed_doc):
                truncate_token_info = detailed_doc.mm_doc_seq.doc_seq[0].token_info[:self.max_total_length*16]
                detailed_doc.mm_doc_seq.doc_seq[0].token_info = truncate_token_info
                detailed_doc.mm_doc_seq.doc_seq[0].shape = [16, self.max_total_length]
            if self.will_exceed(detailed_doc):
                yield self.pop()
            self.put(detailed_doc)
        
    @staticmethod
    def collate_fn(batch):
        return batch[0]