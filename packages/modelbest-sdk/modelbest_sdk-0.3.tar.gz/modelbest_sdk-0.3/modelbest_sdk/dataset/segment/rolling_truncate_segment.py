from collections import deque
from typing import Generator
from modelbest_sdk.dataset.constant import MM_DOC_SEQ
from modelbest_sdk.dataset.segment.segment import Segment
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import LastSample


class RollingTruncateSegment(Segment):
    def __init__(self, max_len: int, drop_last=False, **kwargs):
        self.max_len = max_len
        self.text_only_segment_length = self.audio_only_segment_length = self.max_len + 1
        if kwargs.get('text_only_segment_length') is not None:
            self.text_only_segment_length = kwargs['text_only_segment_length']
        if kwargs.get('audio_only_segment_length') is not None:
            self.audio_only_segment_length = kwargs['audio_only_segment_length']
        self.segment_length = None
        self.drop_last = drop_last
            
    def is_mix(self, detailed_doc: DetailedDoc) -> bool:
        if detailed_doc.proto_type == MM_DOC_SEQ:
            dtype_list = [mmdoc.dtype for mmdoc in detailed_doc.mm_doc_seq.doc_seq]
            if len(set(dtype_list)) > 1:
                return True
        return False
            
    def __call__(self, detailed_doc: DetailedDoc) -> Generator[DetailedDoc, None, None]:
        if self.is_mix(detailed_doc):
            yield detailed_doc
            return
        
        if self.segment_length is None:
            if detailed_doc.proto_type == MM_DOC_SEQ:
                self.segment_length = self.audio_only_segment_length
            else:
                self.segment_length = self.text_only_segment_length
                
        
        current_length = len(detailed_doc)
        
        while current_length > self.segment_length:
            data_to_yield, data_to_segment = detailed_doc.split(self.segment_length, overlap=0)
            # TODO: uncomment when resume excatly is needed
            lask_chunk = data_to_yield.position.chunk
            last_index = data_to_yield.position.index
            last_offset = data_to_yield.prev_len + self.segment_length
            data_to_yield.last_sample = LastSample(lask_chunk, last_index, last_offset)
            yield data_to_yield
            current_length = len(data_to_segment)
            detailed_doc = data_to_segment
        yield detailed_doc

