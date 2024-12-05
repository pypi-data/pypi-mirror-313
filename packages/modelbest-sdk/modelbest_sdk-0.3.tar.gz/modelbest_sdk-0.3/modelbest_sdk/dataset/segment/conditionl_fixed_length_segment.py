from collections import deque
import logging
from typing import Generator
from modelbest_sdk.dataset.segment.segment import Segment
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import LastSample

logger = logging.getLogger(__name__)
class ConditionalFixedLengthSegment(Segment):
    def __init__(self, max_len: int, drop_last=False, **kwargs):
        self.max_len = max_len
        self.drop_last = drop_last
        
        self.buffer = deque()
        self.current_length = 0
    
    def is_instruction(self, data: DetailedDoc) -> bool:
        return data.mask is not None and data.mask[0] == True
    
    def put(self, data: DetailedDoc):
        if self.is_instruction(data):
            if len(data.base_doc) > self.max_len + 1:
                logger.warning(f"Data from : {data.base_doc.tag} {data.position}, type: instruction, length: {len(data.base_doc)}, which is longer than max_len + 1 ({self.max_len + 1}).")
                return
        self.buffer.append(data)
        self.current_length += len(data)
    
    def pop(self) -> DetailedDoc:
        remaining_seq_length = self.max_len + 1
        begin = 0
        concat_data = None
        last_sample = None
        while self.buffer and remaining_seq_length > 0:
            data: DetailedDoc = self.buffer.popleft()
            self.current_length -= len(data)
            
            if remaining_seq_length >= len(data):
                end = begin + len(data)
                data_to_fill = data
            else:
                end = begin + remaining_seq_length
                if self.is_instruction(data):
                    self.buffer.appendleft(data)
                    self.current_length += len(data)
                    break
                else:
                    data_to_fill, data_to_buffer = data.split(remaining_seq_length)
                    self.buffer.appendleft(data_to_buffer)
                    self.current_length += len(data_to_buffer)
                    # useful when resume
                    lask_chunk = data_to_fill.position.chunk
                    last_index = data_to_fill.position.index
                    last_offset = data_to_fill.prev_len + remaining_seq_length
                    last_sample = LastSample(lask_chunk, last_index, last_offset)
            concat_data = data_to_fill if concat_data is None else concat_data.concat(data_to_fill)
            remaining_seq_length -= len(data_to_fill)
            begin = end
        concat_data.last_sample = last_sample
        return concat_data
            
            
    def __call__(self, detailed_doc: DetailedDoc) -> Generator[DetailedDoc, None, None]:
        self.put(detailed_doc)
        while self.current_length > self.max_len:
            yield self.pop()

