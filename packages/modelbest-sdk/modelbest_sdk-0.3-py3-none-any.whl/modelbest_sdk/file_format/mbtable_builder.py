import ctypes
import os
import platform
from modelbest_sdk.file_format.mbtable import ByteArray, ByteArrayList

def get_so_file_path():
    system = platform.system().lower()
    machine = platform.machine().lower()
    base_path = os.path.join(os.path.dirname(__file__), 'lib')

    if system == 'linux' and machine == 'x86_64':
        so_file = 'libmbtable_sdk_shared_linux_x86.so'
    elif system == 'linux' and machine == 'aarch64':
        so_file = 'libmbtable_sdk_shared_linux_arm.so'
    elif system == 'darwin':
        so_file = 'libmbtable_sdk_shared_macos.so'
    else:
        raise OSError(f"Unsupported platform: {system} {machine}")

    return os.path.join(base_path, so_file)

lib_path = get_so_file_path()
lib = ctypes.CDLL(lib_path)

lib.MbTableBuilderCreate.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.MbTableBuilderCreate.restype = ctypes.c_void_p

lib.MbTableBuilderWrite.argtypes = [ctypes.c_void_p, ctypes.POINTER(ByteArray)]
lib.MbTableBuilderWrite.restype = ctypes.c_int

lib.MbTableBuilderWriteList.argtypes = [ctypes.c_void_p,
                                        ctypes.POINTER(ByteArrayList)]
lib.MbTableBuilderWriteList.restype = ctypes.c_int

lib.MbTableBuilderAddMetaData.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                          ctypes.POINTER(ByteArray)]
lib.MbTableBuilderAddMetaData.restype = None

lib.MbTableBuilderBuild.argtypes = [ctypes.c_void_p]
lib.MbTableBuilderBuild.restype = None

def create_byte_array(data):
    return ByteArray(ctypes.cast(ctypes.c_char_p(data), ctypes.POINTER(ctypes.c_char)), len(data))

class MbTableBuilder:
    def __init__(self, path: str, codec: str = 'kZlib'):
        """
        Initializes an instance of the class, setting up the underlying MbTable builder with the specified path and compression codec.

        The `codec` parameter specifies the compression method to be used for the MbTable. It must be a string that matches one of the predefined compression codec names. The available codecs are as follows:
        - 'kLzo': LZO compression.
        - 'kZlib': zlib compression.
        - 'kUnCompress': No compression.
        - 'kGzip': Gzip compression.
        - 'kSnappy': Snappy compression.
        - 'kUnknown': Represents an unknown or unsupported compression codec. It's recommended to use one of the supported codecs for compatibility.

        Args:
            path (str): The file system path where the MbTable will be created.
            codec (str, optional): The name of the compression codec to use. Defaults to 'kZlib'.

        Note:
            The path and codec arguments are encoded in UTF-8 before being passed to the underlying `CreateMbTableBuilder` function of the `lib` library.
        """
        dir_name = os.path.dirname(path)
        if dir_name == '':
            dir_name = '.'
        os.makedirs(dir_name, exist_ok=True)
        self.builder = lib.MbTableBuilderCreate(path.encode('utf-8'), codec.encode('utf-8'))

    def write(self, record):
        if isinstance(record, str):
            record = record.encode('utf-8')
        record_ba = create_byte_array(record)
        ret = lib.MbTableBuilderWrite(self.builder, ctypes.byref(record_ba))
        if ret == -1:
            raise Exception('Maximum of records 2^30 reached')
            
    def write_list(self, records):
        bal = ByteArrayList()
        bal.size = len(records)
        array_list = ByteArray * bal.size
        data_list = array_list()
        i = 0
        for record in records:
            if isinstance(record, str):
                record = record.encode('utf-8')
            data_list[i] = create_byte_array(record)
            i+=1
        bal.data_list = ctypes.cast(data_list, ctypes.POINTER(ByteArray))
        ret = lib.MbTableBuilderWriteList(self.builder, ctypes.byref(bal))
        if ret == -1:
            raise Exception('Maximum of records 2^20 reached')
            
    def add_metadata(self, key: str, value):
        if isinstance(value, str):
            value = value.encode('utf-8')
        value_ba =  create_byte_array(value)
        lib.MbTableBuilderAddMetaData(self.builder, key.encode('utf-8'), ctypes.byref(value_ba))

    def flush(self):
        lib.MbTableBuilderBuild(self.builder)

if __name__ == '__main__':
    from modelbest_sdk.dataset.thrift_wrapper.base_doc import MmDocSeq, MmDoc, DocType
    builder = MbTableBuilder('./mm1.mbt', 'kZlib')
    
    for i in range(10):
        doc_list = []
        for j in range(4):
            mmdoc = MmDoc(
                dtype=DocType.AUDIO,
                token_info=[1, 2, 3, 4, 5, 6],
                shape=[10, 10],
                mask=[False, False, True, True, False, False],
                docid='123',
                tag=['tag1', 'tag2'],
                version='1.0',
                reserved_col='reserved_col',
            )
            doc_list.append(mmdoc)
        doc_seq = MmDocSeq(doc_list)
        builder.write(doc_seq.serialize())
    builder.flush()
