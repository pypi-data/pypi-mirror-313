import thriftpy2
from thriftpy2.utils import deserialize, serialize

import os

proto_dir = os.path.join(os.path.dirname(__file__), "../..", "proto")
metadata_thrift = thriftpy2.load(os.path.join(proto_dir, "metadata.thrift"))

def enum_to_string(enum_value):
    if enum_value == metadata_thrift.TableType.RECORD_TABLE:
        return 'RECORD_TABLE'
    elif enum_value == metadata_thrift.TableType.LIST_TABLE:
        return 'LIST_TABLE'
    else:
        print('Unknown type: ', enum_value)
        return None

def str_to_enum(enum_class, enum_str):
    for name, value in enum_class.__dict__.items():
        if name == enum_str:
            return value
    return 0

class SSTableMetadata:
    def __init__(self,
                 table_type=None,
                 total_count=None,
                 tokenizer_version=None,
                 proto_type=None):
        self.table_type = table_type
        self.total_count = total_count
        self.tokenizer_version = tokenizer_version
        self.proto_type = proto_type
    
    @staticmethod
    def deserialize(bin):
        if bin == b'':
            return SSTableMetadata()
        return SSTableMetadata.from_thrift(
                deserialize(metadata_thrift.SSTableMetadata(), bin))

    @staticmethod
    def from_thrift(meta_proto):
        return SSTableMetadata(
            table_type=enum_to_string(meta_proto.tabletype),
            total_count=meta_proto.total_count,
            tokenizer_version=meta_proto.tokenizer_version,
            proto_type=meta_proto.proto_type,
        )

    def serialize(self):
        return serialize(self.to_thrift())
    
    def to_thrift(self):
        return metadata_thrift.SSTableMetadata(
            tabletype=str_to_enum(metadata_thrift.TableType, self.table_type),
            total_count=self.total_count,
            tokenizer_version=self.tokenizer_version,
            proto_type=self.proto_type,
        )
    
    def __repr__(self) -> str:
        return f"SSTableMetadata(table_type={self.table_type}, total_count={self.total_count}, tokenizer_version={self.tokenizer_version}, proto_type={self.proto_type})"

