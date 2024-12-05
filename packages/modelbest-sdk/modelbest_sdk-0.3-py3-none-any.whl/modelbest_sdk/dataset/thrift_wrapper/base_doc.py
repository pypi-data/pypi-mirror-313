import io
import logging
from typing import Any, Dict, List, Tuple, Union
import thriftpy2
from thriftpy2.utils import deserialize, serialize
import os
from PIL import Image
import torch
import numpy

from modelbest_sdk.dataset.constant import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk, DatasetInfo, LastSample
from modelbest_sdk.dataset.thrift_wrapper.messages import Messages
from modelbest_sdk.dataset.thrift_wrapper.utils import Utils

proto_dir = os.path.join(os.path.dirname(__file__), "../..", "proto")

doc_thrift = thriftpy2.load(os.path.join(proto_dir, "traindoc.thrift"))
mmdoc_thrift = thriftpy2.load(os.path.join(proto_dir, "mm_doc.thrift"))
imgdoc_thrift = thriftpy2.load(os.path.join(proto_dir, "image_doc.thrift"))

logger = logging.getLogger(__name__)

class BaseDoc:
    def __init__(self, token_ids=None, mask=None, docid=None, tag=None, token=None, tokenizer_version=None, reserved_col=None):
        self.token_ids = token_ids
        self.mask = mask
        self.docid = docid
        self.tag = tag
        self.token = token
        self.tokenizer_version = tokenizer_version
        self.reserved_col = reserved_col
    
    def split(self, offset, overlap=1) -> Tuple["BaseDoc", "BaseDoc"]:
        if not (1 <= offset <= len(self.token_ids)):
            raise ValueError("Offset must be between 1 and the length of the token_ids minus one.")
        # Split token_ids and mask with an overlap at offset
        token_ids_1, token_ids_2 = self.token_ids[:offset], self.token_ids[offset-overlap:]
        mask_1, mask_2 = self.mask[:offset], self.mask[offset-overlap:]
        
        doc1 = BaseDoc(token_ids=token_ids_1, mask=mask_1, docid=self.docid, tag=self.tag, token=self.token, tokenizer_version=self.tokenizer_version, reserved_col=self.reserved_col)
        doc2 = BaseDoc(token_ids=token_ids_2, mask=mask_2, docid=self.docid, tag=self.tag, token=self.token, tokenizer_version=self.tokenizer_version, reserved_col=self.reserved_col)
        return doc1, doc2
    
    def concat(self, other: "BaseDoc") -> "BaseDoc":
        if self.tag is None or other.tag is None:
            tag = None
        else:
            tag = list(set(self.tag + other.tag))
        return BaseDoc(
            token_ids=self.token_ids + other.token_ids,
            mask=self.mask + other.mask,
            docid=self.docid,
            tag=tag, # TODO：now there should be only one tag since concat happens in the same dataset, and same dataset should have only one tag
            token=self.token,
            tokenizer_version=self.tokenizer_version,
            reserved_col=self.reserved_col
        )

    @staticmethod
    def deserialize(bin):
        return BaseDoc.from_thrift(deserialize(doc_thrift.BaseDoc(), bin))
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    def to_thrift(self):#反射
        return doc_thrift.BaseDoc(
            token_ids=self.token_ids,
            mask=self.mask,
            docid=self.docid,
            tag=self.tag,
            token=self.token,
            tokenizer_version=self.tokenizer_version,
            reserved_col=self.reserved_col
        )
    
    @staticmethod
    def from_thrift(thrift_base_doc):
        return BaseDoc(
            token_ids=thrift_base_doc.token_ids,
            mask=thrift_base_doc.mask,
            docid=thrift_base_doc.docid,
            tag=thrift_base_doc.tag,
            token=thrift_base_doc.token,
            tokenizer_version=thrift_base_doc.tokenizer_version,
            reserved_col=thrift_base_doc.reserved_col
        )
        
    def __len__(self) -> int:
        return len(self.token_ids)
        
    def __repr__(self) -> str:
        return f"BaseDoc(token_ids={self.token_ids}, mask={self.mask}, tag={self.tag}, token={self.token}, tokenizer_version={self.tokenizer_version}, reserved_col={self.reserved_col})"

from enum import Enum

class DocType(Enum):
    UNKNOWN = 0
    TXT = 1
    IMG = 2
    AUDIO = 3
    VIDEO = 4
    AUDIO_SNIPPET = 5


class MmDoc:
    def __init__(self, dtype: DocType=None, token_info=None, token_buffer=None, text=None, audio_bytes=None, shape=None, mask=None, docid=None, tag=None, version=None, reserved_col=None, image_md5=None):
        self.dtype = dtype
        self.token_info = token_info
        self.token_buffer = token_buffer
        self.text = text
        self.audio_bytes = audio_bytes
        self.shape = shape
        self.mask = mask
        self.docid = docid
        self.tag = tag
        self.version = version
        self.reserved_col = reserved_col
        self.image_md5 = image_md5
        self.image: Image.Image = None

    def split(self, offset, overlap=1) -> Tuple["MmDoc", "MmDoc"]:
        if not (1 <= offset <= self.shape[1]):
            raise ValueError("Offset must be between 1 and the length of the token_ids minus one.")
        # Split token_ids and mask with an overlap of one token at offset
        
        token_info_2d = torch.Tensor(self.token_info).reshape(self.shape)
        token_ids_1, token_ids_2 = token_info_2d[:, :offset].reshape(-1).tolist(), token_info_2d[:, offset-overlap:].reshape(-1).tolist()
        if self.mask is not None:
            mask_1, mask_2 = self.mask[:offset], self.mask[offset-overlap:]
        else:
            mask_1, mask_2 = None, None
        return MmDoc(
            dtype=self.dtype,
            token_info=token_ids_1,
            shape=[self.shape[0], offset],
            mask=mask_1,
            docid=self.docid,
            tag=self.tag,
            version=self.version,
            reserved_col=self.reserved_col
        ), MmDoc(
            dtype=self.dtype,
            token_info=token_ids_2,
            shape=[self.shape[0], self.shape[1] - offset + overlap],
            mask=mask_2,
            docid=self.docid,
            tag=self.tag,
            version=self.version,
            reserved_col=self.reserved_col
        )
        
    def concat(self, other: "MmDoc") -> "MmDoc":
        if self.tag is None or other.tag is None:
            tag = None
        else:
            tag = list(set(self.tag + other.tag))
        token_ids = torch.cat([torch.Tensor(self.token_info).reshape(self.shape), torch.Tensor(other.token_info).reshape(other.shape)], dim=1).reshape(-1).tolist()
        if self.mask is not None and other.mask is not None:
            mask = self.mask + other.mask
        else:
            mask = None
        return MmDoc(
            dtype=self.dtype,
            token_info=token_ids,
            shape=[self.shape[0], self.shape[1] + other.shape[1]],
            mask=mask,
            docid=self.docid,
            tag=tag,
            version=self.version,
            reserved_col=self.reserved_col
        )
        

    @staticmethod
    def from_thrift(thrift_mm_doc):
        return MmDoc(
            dtype=DocType(thrift_mm_doc.dtype),
            token_info=numpy.frombuffer(thrift_mm_doc.token_buffer, numpy.int32).tolist() if thrift_mm_doc.token_buffer is not None else thrift_mm_doc.token_info,
            text=thrift_mm_doc.text,
            audio_bytes=thrift_mm_doc.audio_bytes,
            shape=thrift_mm_doc.shape,
            mask=thrift_mm_doc.mask,
            docid=thrift_mm_doc.docid,
            tag=thrift_mm_doc.tag,
            version=thrift_mm_doc.version,
            reserved_col=thrift_mm_doc.reserved_col,
            image_md5=thrift_mm_doc.image_md5
        )

    def to_thrift(self):
        return mmdoc_thrift.MmDoc(
            dtype=self.dtype.value,
            token_info=self.token_info,
            token_buffer=self.token_buffer,
            text=self.text,
            shape=self.shape,
            mask=self.mask,
            docid=self.docid,
            tag=self.tag,
            version=self.version,
            reserved_col=self.reserved_col,
            image_md5=self.image_md5
        )
        
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return MmDoc.from_thrift(deserialize(mmdoc_thrift.MmDoc(), bin))
    
    def __len__(self) -> int:
        if self.dtype == DocType.TXT:
            return len(self.token_info) if self.token_info else 0
        elif self.dtype == DocType.AUDIO:
            return self.shape[1]
        else:
            return 0
        # raise ValueError(f"unsupported dtype {self.dtype}")
    
    def __repr__(self) -> str:
        return f"MmDoc(dtype={self.dtype}, token_info={self.token_info}, text={self.text}, shape={self.shape}, mask={self.mask}, docid={self.docid}, tag={self.tag}, version={self.version}, reserved_col={self.reserved_col}, image_md5={self.image_md5})"


class Position:
    def __init__(self, chunk: Chunk, index: int, length: int=None, truncated: bool=False):
        self.chunk = chunk
        self.index = index
        self.length = length
        self.truncated = truncated
    
    def split(self, offset, overlap=1) -> Tuple["Position", "Position"]:
        if not (1 <= offset <= self.length):
            raise ValueError("Offset must be between 1 and the length of the position minus one.")
        # Split with an overlap of one token at offset
        position1 = Position(chunk=self.chunk, index=self.index, length=offset, truncated=True)
        position2 = Position(chunk=self.chunk, index=self.index, length=self.length - offset + overlap, truncated=True)
        return position1, position2

    def __repr__(self) -> str:
        return f"Position(chunk={self.chunk}, index={self.index}, length={self.length}, truncated={self.truncated})"

class MmDocSeq:
    def __init__(self, doc_seq: List[MmDoc]=None):
        self.doc_seq = doc_seq
        self.length = None
        
    @staticmethod
    def from_twin_list(base_list, image_list):
        mm_doc_seq = MmDocSeq.deserialize(base_list[0])
        image_list = [item for item in image_list if item != b'']
        image_inner_idx = 0
        for mm_doc in mm_doc_seq.doc_seq:
            if mm_doc.dtype == DocType.IMG:
                image_doc = ImageDoc.deserialize(image_list[image_inner_idx])
                image_bytes = image_doc.image_bytes
                #img_io = io.BytesIO(image_bytes)
                #img_io.seek(0)
                #mm_doc.image = Image.open(img_io).convert('RGB')
                mm_doc.image = image_bytes
                image_inner_idx += 1
                assert mm_doc.image_md5 == image_doc.image_md5, "image_md5 not match"
        return mm_doc_seq

    @staticmethod
    def from_thrift(thrift_mm_doc_seq):
        return MmDocSeq(doc_seq=[MmDoc.from_thrift(doc) for doc in thrift_mm_doc_seq.doc_seq])

    def to_thrift(self):
        return mmdoc_thrift.MmDocSeq(doc_seq=[doc.to_thrift() for doc in self.doc_seq])

    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return MmDocSeq.from_thrift(deserialize(mmdoc_thrift.MmDocSeq(), bin))
    
    def __len__(self) -> int:
        if self.length is None:
            self.length = sum(len(doc) for doc in self.doc_seq)
        return self.length
    
    def __repr__(self) -> str:
        return f"MmDocSeq(doc_seq={self.doc_seq})"

class ImageDoc:
    def __init__(self, image_bytes: bytes=None, image_md5: bytes=None):
        self.image_bytes = image_bytes
        self.image_md5 = image_md5
    
    @staticmethod
    def from_thrift(thrift_image_doc):
        return ImageDoc(image_bytes=thrift_image_doc.image_bytes, image_md5=thrift_image_doc.image_md5)
    
    def to_thrift(self):
        return imgdoc_thrift.ImageDoc(image_bytes=self.image_bytes, image_md5=self.image_md5)
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return ImageDoc.from_thrift(deserialize(imgdoc_thrift.ImageDoc(), bin))
    
    def __repr__(self) -> str:
        return f"ImageDoc(image_bytes={self.image_bytes}, image_md5={self.image_md5})"


class DetailedDoc:
    def __init__(
        self, 
        proto_type: str=None, 
        base_doc: BaseDoc=None, 
        mm_doc_seq: MmDocSeq=None, 
        messages: Messages=None,
        position: Position=None, 
        positions: List[Position]=None, 
        dataset_idx: int=None, 
        raw: str=None, 
        usage: str=None, 
        last_sample: LastSample=None, 
        prev_len: int=0,
        udd: Any=None,
        dataset_info: DatasetInfo=None,
    ):
        self.proto_type = proto_type
        self.base_doc = base_doc
        self.mm_doc_seq = mm_doc_seq
        self.messages = messages
        self.position = position
        self.positions = positions if positions is not None else [position]
        self.dataset_idx = dataset_idx
        self.raw = raw
        self.usage = usage
        self.last_sample = last_sample
        self.prev_len = prev_len
        self.udd = udd
        self.dataset_info = dataset_info
    
    @property
    def tag(self) -> Union[str, List[str]]:
        if self.base_doc is not None:
            return self.base_doc.tag
        else:
            return self.mm_doc_seq.doc_seq[0].tag
    
    @property
    def mask(self) -> List[int]:
        if self.base_doc is not None:
            return self.base_doc.mask
        else:
            return self.mm_doc_seq.doc_seq[0].mask
    
    @property
    def indexes_dict(self) -> Dict[Chunk, List[int]]:
        # there could be multiple positions for the same chunk, so we need to group them by chunk
        # also remove last_sample position if it exists
        indexes_dict = {}
        for pos in self.positions:
            if self.last_sample is not None and pos.chunk == self.last_sample.chunk and pos.index == self.last_sample.index:
                continue
            if pos.chunk not in indexes_dict:
                indexes_dict[pos.chunk] = []
            indexes_dict[pos.chunk].append(pos.index)
        return indexes_dict
    
    def split(self, offset, overlap=1) -> Tuple["DetailedDoc", "DetailedDoc"]:
        pos1, pos2 = self.position.split(offset, overlap)
        if self.base_doc is not None:
            doc1, doc2 = self.base_doc.split(offset, overlap)
            return DetailedDoc(proto_type=BASE_DOC, base_doc=doc1, position=pos1, dataset_idx=self.dataset_idx, raw=self.raw, usage=self.usage, prev_len=self.prev_len), \
                DetailedDoc(proto_type=BASE_DOC, base_doc=doc2, position=pos2, dataset_idx=self.dataset_idx, raw=self.raw, usage=self.usage, prev_len=self.prev_len+offset-overlap)
        else:
            doc1, doc2 = self.mm_doc_seq.doc_seq[0].split(offset, overlap)
            return DetailedDoc(proto_type=MM_DOC_SEQ, mm_doc_seq=MmDocSeq([doc1]), position=pos1, dataset_idx=self.dataset_idx, raw=self.raw, usage=self.usage, prev_len=self.prev_len), \
                DetailedDoc(proto_type=MM_DOC_SEQ, mm_doc_seq=MmDocSeq([doc2]), position=pos2, dataset_idx=self.dataset_idx, raw=self.raw, usage=self.usage, prev_len=self.prev_len+offset-overlap)

    @staticmethod
    def extend_position(self_positions: List[Position], other_positions: List[Position]):
        extended_positions = []
        extended_positions.extend(self_positions)
        extended_positions.extend(other_positions)
        return extended_positions
    
    def concat(self, other: "DetailedDoc") -> "DetailedDoc":
        # only used for merging data in the same dataset
        
        return DetailedDoc(
            proto_type=self.proto_type,
            base_doc=self.base_doc.concat(other.base_doc) if self.base_doc is not None else None,
            mm_doc_seq=MmDocSeq([self.mm_doc_seq.doc_seq[0].concat(other.mm_doc_seq.doc_seq[0])]) if self.mm_doc_seq is not None else None,
            positions=DetailedDoc.extend_position(self.positions, other.positions),
            dataset_idx=self.dataset_idx,
        )
        
    def deserialize(self) -> bool:
        try:
            if self.proto_type == BASE_DOC:
                self.base_doc = BaseDoc.deserialize(self.raw)
            elif self.proto_type == MM_DOC_SEQ:
                if isinstance(self.raw, bytes):
                    self.mm_doc_seq = MmDocSeq.deserialize(self.raw)
                else:
                    base_list, image_list = self.raw
                    self.mm_doc_seq = MmDocSeq.from_twin_list(base_list, image_list)
            elif self.proto_type == MESSAGES:
                self.messages = Messages.deserialize(self.raw)
            elif self.proto_type == ZIP or self.proto_type == RAW:
                return True
            self.position.length = len(self)
            self.raw = None
            return True
        except Exception as e:
            logger.error(f"Failed to deserialize detailed doc: {e}")
            return False
    
    def tag_or_default(self, default_tag: str):
        if self.proto_type == BASE_DOC:
            if self.base_doc.tag is None:
                self.base_doc.tag = default_tag
        elif self.proto_type == MM_DOC_SEQ: # TODO: in seq, tag is doc level not seq level, is this ok?
            if self.mm_doc_seq.doc_seq[0].tag is None:
                self.mm_doc_seq.doc_seq[0].tag = default_tag
    
    def __len__(self) -> int:
        if self.proto_type == BASE_DOC:
            return len(self.base_doc)
        elif self.proto_type == MM_DOC_SEQ:
            return len(self.mm_doc_seq)
        elif self.proto_type == MESSAGES:
            return len(self.messages)
        else:
            return 0
    
    def __repr__(self) -> str:
        return f"DetailedDoc(base_doc={self.base_doc}, mm_doc={self.mm_doc_seq}, position={self.position}, dataset_idx={self.dataset_idx})"
