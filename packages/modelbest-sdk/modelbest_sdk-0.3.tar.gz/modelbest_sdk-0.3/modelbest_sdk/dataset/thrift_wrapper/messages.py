import logging
from typing import Dict, List, Tuple, Union
import numpy
import thriftpy2
from thriftpy2.utils import deserialize, serialize
import os

from modelbest_sdk.dataset.constant import *
from modelbest_sdk.file_format.mbtable import MbTable, MbTableIterator
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder

proto_dir = os.path.join(os.path.dirname(__file__), "../..", "proto")


messages_thrift = thriftpy2.load(os.path.join(proto_dir, "messages.thrift"))
logger = logging.getLogger(__name__)

from enum import Enum

class DocType(Enum):
    UNKNOWN = 0
    TXT = 1
    IMG = 2
    AUDIO = 3
    VIDEO = 4
    AUDIO_SNIPPET = 5


'''
namespace cpp proto

enum DocType {
    UNKNOWN = 0,
    TXT = 1,
    IMG = 2,
    AUDIO = 3,
    VIDEO = 4,
    AUDIO_SNIPPET = 5,
}

struct AudioToken {
    10: required i32 start,   # 片段开始时间，ms
    20: required i32 stop,     # 片段结束时间，ms
    30: optional string text, # 音频片段对应的文本
}

struct AudioSnippet {
    10: required string wav_file_path,    # 音频文件路径
    20: required i32 start,               # 片段开始时间，ms
    30: required i32 stop,                 # 片段结束时间，ms
    40: optional string text,             # 音频片段对应的文本
    50: optional list<AudioToken> tokens,
}

struct Audio {
    10: required binary wav,  # 音频二进制
    11: optional binary token_buffer, # tokenized audio token id to bytes
    20: optional string text, # 音频对应的文本
    30: optional list<AudioToken> tokens,
}

struct Content {
    10: required DocType dtype,
    # 当 dtype 为 AUDIO_SNIPPET 时，value为 AudioSnippet 的序列化值；
    # 当 dtype 为 AUDIO 时，value为 Audio 的序列化值；
    20: optional binary value,
}

struct Msg {
    // 角色: system, user, assistant
    10: required string role,
    // 内容
    20: required list<Content> content,
    // 说话者
    30: optional string name,
    40: optional string reserved_column,
}

struct Metadata {
    10: optional string wav_file_path,
}

struct Messages {
    10: required list<Msg> messages,
    20: optional Metadata metadata,
    30: optional string reserved_column,
}
'''

class AudioToken:
    def __init__(self, start: int, stop: int, text: str = None):
        self.start = start
        self.stop = stop
        self.text = text
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return AudioToken.from_thrift(deserialize(messages_thrift.AudioToken(), bin))
    
    def to_thrift(self):
        return messages_thrift.AudioToken(
            start=self.start,
            stop=self.stop,
            text=self.text
        )
    
    @staticmethod
    def from_thrift(thrift_audio_token):
        return AudioToken(
            start=thrift_audio_token.start,
            stop=thrift_audio_token.stop,
            text=thrift_audio_token.text
        )
    
    def __repr__(self) -> str:
        return f"AudioToken(start={self.start}, stop={self.stop}, text={self.text})"

class AudioSnippet:
    def __init__(self, wav_file_path: str, start: int, stop: int, text: str = None):
        self.wav_file_path = wav_file_path
        self.start = start
        self.stop = stop
        self.text = text
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return AudioSnippet.from_thrift(deserialize(messages_thrift.AudioSnippet(), bin))
    
    def to_thrift(self):
        return messages_thrift.AudioSnippet(
            wav_file_path=self.wav_file_path,
            start=self.start,
            stop=self.stop,
            text=self.text
        )
    
    @staticmethod
    def from_thrift(thrift_audio_snippet):
        return AudioSnippet(
            wav_file_path=thrift_audio_snippet.wav_file_path,
            start=thrift_audio_snippet.start,
            stop=thrift_audio_snippet.stop,
            text=thrift_audio_snippet.text
        )
    
    def __repr__(self) -> str:
        return f"AudioSnippet(wav_file_path={self.wav_file_path}, start={self.start}, stop={self.stop}, text={self.text})"
    
class Audio:
    def __init__(self, wav: bytes, text: str = None, tokens: List[AudioToken] = None, token_ids: List = None):
        self.wav = wav
        self.text = text
        self.tokens = tokens
        self.token_ids = token_ids
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return Audio.from_thrift(deserialize(messages_thrift.Audio(), bin))
    
    def to_thrift(self):
        return messages_thrift.Audio(
            wav=self.wav,
            text=self.text,
            tokens=[token.to_thrift() for token in self.tokens] if self.tokens is not None else None,
            token_buffer=numpy.array(self.token_ids, dtype=numpy.int32).tobytes() if self.token_ids is not None else None
        )
    
    @staticmethod
    def from_thrift(thrift_audio):
        return Audio(
            wav=thrift_audio.wav,
            text=thrift_audio.text,
            tokens=[AudioToken.from_thrift(token) for token in thrift_audio.tokens] if thrift_audio.tokens is not None else None,
            token_ids=numpy.frombuffer(thrift_audio.token_buffer, dtype=numpy.int32) if thrift_audio.token_buffer is not None else None
        )
    
    def __repr__(self) -> str:
        return f"Audio(wav={self.wav}, text={self.text}, tokens={self.tokens}, token_ids={self.token_ids})"
    
class Content:
    def __init__(self, dtype: DocType, value: Union[AudioSnippet, Audio]):
        self.dtype = dtype
        self.value = value
        
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return Content.from_thrift(deserialize(messages_thrift.Content(), bin))
    
    def to_thrift(self):
        if self.dtype == DocType.AUDIO_SNIPPET:
            return messages_thrift.Content(dtype=self.dtype.value, value=self.value.serialize())
        elif self.dtype == DocType.AUDIO:
            return messages_thrift.Content(dtype=self.dtype.value, value=self.value.serialize())
        else:
            return messages_thrift.Content(dtype=self.dtype.value, value=self.value)
        
    @staticmethod
    def from_thrift(thrift_content):
        if thrift_content.dtype == DocType.AUDIO_SNIPPET.value:
            return Content(dtype=DocType.AUDIO_SNIPPET, value=AudioSnippet.deserialize(thrift_content.value))
        elif thrift_content.dtype == DocType.AUDIO.value:
            return Content(dtype=DocType.AUDIO, value=Audio.deserialize(thrift_content.value))
        else:
            return Content(dtype=DocType(thrift_content.dtype), value=thrift_content.value)
    
    def __repr__(self) -> str:
        return f"Content(dtype={self.dtype}, value={self.value})"

class Msg:
    def __init__(self, role: str, content: List[Content], name: str = None, reserved_column: str = None):
        self.role = role
        self.content = content
        self.name = name
        self.reserved_column = reserved_column
        
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return Msg.from_thrift(deserialize(messages_thrift.Msg(), bin))
    def to_thrift(self):
        return messages_thrift.Msg(
            role=self.role,
            content=[content.to_thrift() for content in self.content],
            name=self.name,
            reserved_column=self.reserved_column
        )
    
    @staticmethod
    def from_thrift(thrift_msg):
        return Msg(
            role=thrift_msg.role,
            content=[Content.from_thrift(content) for content in thrift_msg.content] if thrift_msg.content is not None else None,
            name=thrift_msg.name,
            reserved_column=thrift_msg.reserved_column
        )
    
    def __repr__(self) -> str:
        return f"Msg(role={self.role}, content={self.content}, name={self.name}, reserved_column={self.reserved_column})"

class Metadata:
    def __init__(self, wav_file_path: str = None):
        self.wav_file_path = wav_file_path
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return Metadata.from_thrift(deserialize(messages_thrift.Metadata(), bin))
    
    def to_thrift(self):
        return messages_thrift.Metadata(
            wav_file_path=self.wav_file_path,
        )
    
    @staticmethod
    def from_thrift(thrift_metadata):
        return Metadata(
            wav_file_path=thrift_metadata.wav_file_path,
        )
    
    def __repr__(self) -> str:
        return f"Metadata(wav_file_path={self.wav_file_path})"

class Messages:
    def __init__(self, messages: List[Msg], metadata: Metadata = None, reserved_column: str = None):
        self.messages = messages
        self.metadata = metadata
        self.reserved_column = reserved_column
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    @staticmethod
    def deserialize(bin):
        return Messages.from_thrift(deserialize(messages_thrift.Messages(), bin))
    
    def to_thrift(self):
        return messages_thrift.Messages(
            messages=[msg.to_thrift() for msg in self.messages],
            metadata=self.metadata.to_thrift() if self.metadata is not None else None,
            reserved_column=self.reserved_column
        )
    
    @staticmethod
    def from_thrift(thrift_messages):
        return Messages(
            messages=[Msg.from_thrift(msg) for msg in thrift_messages.messages] if thrift_messages.messages is not None else None,
            metadata=Metadata.from_thrift(thrift_messages.metadata) if thrift_messages.metadata is not None else None,
            reserved_column=thrift_messages.reserved_column
        )
    
    def __len__(self) -> int:
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"Messages(messages={self.messages}, metadata={self.metadata}, reserved_column={self.reserved_column})"

if __name__ == '__main__':
    file_path = 'test.sstable'
    # write
    builder = MbTableBuilder('test.sstable')
    for i in range(10):
        messages = Messages([
            Msg(role="role1", content=[Content(dtype=DocType.AUDIO_SNIPPET, value=AudioSnippet(wav_file_path="test.wav", start=0, stop=1000, text="hello world"))], name="name1", reserved_column="reserved1"),
            Msg(role="role2", content=[Content(dtype=DocType.AUDIO, value=Audio(wav=b"123456", text="audio1", tokens=[AudioToken(0, 1, '嗨')]))]),
            Msg(role="role3", content=[Content(dtype=DocType.TXT, value="text1"), Content(dtype=DocType.IMG, value="img1")])
        ])
        messages.metadata = Metadata(wav_file_path="test.wav")
        messages.reserved_column = 'test'
        builder.write(messages.serialize())
    builder.flush()
    
    # read
    print(MbTable(file_path).get_file_entry_count())
    with MbTableIterator(file_path) as iterator:    
        for record in iterator:
            messages = Messages.deserialize(record)
            for msg in messages.messages:
                print(msg.role)
                print(msg.content)
                print(msg.name)
                print(msg.reserved_column)
            print(messages.metadata)
            print(messages.reserved_column)
    
