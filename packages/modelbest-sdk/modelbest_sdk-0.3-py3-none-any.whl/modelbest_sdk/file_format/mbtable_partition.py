import json
import logging
import os

from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc, DocType, MmDocSeq
from modelbest_sdk.file_format.mbtable import MbTable, MbTableIterator, TwinMbTable, TwinMbTableListIterator

'''
MbTablePartition is designed to manage a directory of mbtable files, and provide a way to iterate over the rows of the files.
Note that each file can contain max 2 << 30 records.
'''
def valid_file_name(file: str):
    # 有时候生成的数据会有非 sstable 文件在文件夹内。姑且认为这也是合理需求，所以这里过滤掉这些文件，如果有更多的其他格式文件可以再加
    return file != "_SUCCESS" and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.jsonl')

class MbTablePartition:
    def __init__(self, partition_path: str):
        """
        calculate total count of rows in mbtable partition
        """
        self.partition_path = partition_path
        if self.from_metadata_json():
            logging.warning(f"Using cache metadata.json to initialize MbTablePartition: {self.partition_path}")
            return
        text_path = os.path.join(partition_path, 'doc')
        image_path = os.path.join(partition_path, 'image')
        self.is_twin = False
        if os.path.exists(text_path) and os.path.exists(image_path):
            self.is_twin = True
        self.total_count = 0
        if not self.is_twin:
            self.file_name_list = [file for file in os.listdir(partition_path) if valid_file_name(file)]
            assert len(self.file_name_list) > 0
            self.file_name_list.sort()
            self.abs_path_list = [os.path.join(partition_path, file) for file in self.file_name_list]
            self.abs_path_index_dict = {file: i for i, file in enumerate(self.abs_path_list)}
            self.file_handle_list = [MbTable(file) for file in self.abs_path_list]
        else:
            self.text_file_name_list = [file for file in os.listdir(text_path) if valid_file_name(file)]
            self.image_file_name_list = [file for file in os.listdir(image_path) if valid_file_name(file)]
            assert len(self.text_file_name_list) > 0
            assert len(self.image_file_name_list) > 0
            assert len(self.text_file_name_list) == len(self.image_file_name_list), "Text and image files count must match"
            self.text_file_name_list.sort()
            self.image_file_name_list.sort()
            self.text_abs_path_list = [os.path.join(text_path, file) for file in self.text_file_name_list]
            self.image_abs_path_list = [os.path.join(image_path, file) for file in self.image_file_name_list]
            self.abs_path_index_dict = {file: i for i, file in enumerate(self.text_abs_path_list)}
            self.file_handle_list = [TwinMbTable(text_file, image_file) for text_file, image_file in zip(self.text_abs_path_list, self.image_abs_path_list)]
        
        self.file_row_counts = []
        self.cumulative_row_counts = []

        cumulative_count = 0
        for handle in self.file_handle_list:
            count = len(handle)
            self.total_count += count
            self.file_row_counts.append(count)
            
            cumulative_count += count
            self.cumulative_row_counts.append(cumulative_count)
        
        self.generate_metadata_json()

    def to_broadcast_data(self):
        return {
            "partition_path": self.partition_path,
            "file_name_list": self.file_name_list,
            "file_row_counts": self.file_row_counts,
            "cumulative_row_counts": self.cumulative_row_counts,
        }

    @classmethod
    def from_broadcast_data(cls, broadcast_data):
        instance = cls.__new__(cls)
        instance.partition_path = broadcast_data["partition_path"]
        instance.file_name_list = broadcast_data["file_name_list"]
        instance.abs_path_list = [os.path.join(instance.partition_path, file) for file in instance.file_name_list]
        instance.abs_path_index_dict = {file: i for i, file in enumerate(instance.abs_path_list)}
        instance.file_row_counts = broadcast_data["file_row_counts"]
        instance.cumulative_row_counts = broadcast_data["cumulative_row_counts"]
        instance.total_count = sum(instance.file_row_counts)
        instance.file_handle_list = [MbTable(file) for file in instance.abs_path_list]
        instance.is_twin = False
        return instance
    
    def from_metadata_json(self) -> bool:
        cache_base_dir = os.getenv('CACHE_BASE_DIR')
        if cache_base_dir is None:
            logging.warning("CACHE_BASE_DIR is not set, metadata.json will not be used")
            return False
        meta_path = self.partition_path.lstrip('/')
        cache_file = os.path.join(cache_base_dir, meta_path, 'metadata.json')
        if not os.path.exists(cache_file):
            logging.warning(f"metadata.json not found: {cache_file}")
            return False
        
        with open(cache_file, 'r') as f:
            metadata = json.load(f)
        
        # 设置属性值
        self.file_name_list = metadata.get("file_name_list", [])
        self.file_row_counts = metadata.get("file_row_counts", [])
        self.cumulative_row_counts = metadata.get("cumulative_row_counts", [])
        
        # 根据文件名列表创建绝对路径列表和索引字典
        self.abs_path_list = [os.path.join(self.partition_path, file) for file in self.file_name_list]
        self.abs_path_index_dict = {file: i for i, file in enumerate(self.abs_path_list)}
        
        # 总行数计算
        self.total_count = sum(self.file_row_counts)
        
        # 文件句柄列表
        self.file_handle_list = [MbTable(file) for file in self.abs_path_list]
        
        # 默认其他参数
        self.is_twin = False
        return True
        
    def generate_metadata_json(self):
        cache_base_dir = os.getenv('CACHE_BASE_DIR')
        if cache_base_dir is None:
            logging.warning("CACHE_BASE_DIR is not set, metadata.json will not be generated")
            return
        meta_path = self.partition_path.lstrip('/')
        cache_file = os.path.join(cache_base_dir, meta_path, 'metadata.json')
        if os.path.exists(cache_file):
            logging.warning(f"metadata.json already exists: {cache_file}")
            return
        # 先创建文件夹
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        except OSError:
            logging.error(f"Failed to create cache directory: {os.path.dirname(cache_file)}")
            pass 
        
        # 创建包含所需属性的字典
        metadata = {
            "file_name_list": self.file_name_list,
            "file_row_counts": self.file_row_counts,
            "cumulative_row_counts": self.cumulative_row_counts
        }
        
        # 将数据写入 JSON 文件
        with open(cache_file, 'w') as f:
            json.dump(metadata, f, indent=4)
        

    def get_file_index_and_position(self, n):
        """
        根据行号n找到对应的文件以及该行在文件中的位置
        """
        if n > self.total_count:
            return None, None  # n 超出总行数

        # 确定n在哪个文件中
        for i, cumulative in enumerate(self.cumulative_row_counts):
            if n <= cumulative:
                # 确定在当前文件中的具体位置
                position_in_file = n - (self.cumulative_row_counts[i-1] if i > 0 else 0)
                return i, position_in_file
        
        return None, None  # 如果没有找到，返回None
    
    def get_total_count(self) -> int:
        return self.total_count
    
    def get_file_path(self, file_index):
        return self.abs_path_list[file_index]
    
    def get_twin_handle(self, file_index):
        if not self.is_twin:
            return None
        return self.file_handle_list[file_index]

    def get_next_file_index(self, file_index):
        if file_index == len(self.file_handle_list) - 1:
            return None
        else:
            return file_index + 1
        
    
class MbTablePartitionIterator:
    def __init__(self, mbtable_partition: MbTablePartition, start_index=0, max_iterations=None):
        self.mbtable_partition = mbtable_partition
        self.max_iterations = max_iterations
        self.iterations_count = 0
        assert start_index >= 0 and start_index <= mbtable_partition.get_total_count()
        self.current_file_index, self.current_pos = mbtable_partition.get_file_index_and_position(start_index)
        self.iterator = None
        
    def __iter__(self):
        return self
    
    def __enter__(self):
        if self.iterator is None:
            if self.mbtable_partition.is_twin:
                self.iterator = TwinMbTableListIterator(self.mbtable_partition.get_twin_handle(self.current_file_index), self.current_pos, self.max_iterations)
            else:
                self.iterator = MbTableIterator(self.mbtable_partition.get_file_path(self.current_file_index), self.current_pos, self.max_iterations)
            self.iterator.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.iterator.__exit__(exc_type, exc_val, exc_tb)
    
    def __next__(self):
        if self.max_iterations is not None and self.iterations_count >= self.max_iterations:
            raise StopIteration

        # 检查是否需要初始化或重置迭代器
        if self.iterator is None:
            # 计算剩余的迭代次数，如果 max_iterations 未定义，则不限制迭代器
            remaining_iterations = None if self.max_iterations is None else self.max_iterations - self.iterations_count
            if self.mbtable_partition.is_twin:
                self.iterator = TwinMbTableListIterator(self.mbtable_partition.get_twin_handle(self.current_file_index), self.current_pos, remaining_iterations)
            else:
                self.iterator = MbTableIterator(self.mbtable_partition.get_file_path(self.current_file_index), self.current_pos, remaining_iterations)
            self.iterator.__enter__()

        try:
            record = self.iterator.__next__()
            self.iterations_count += 1  # 更新已迭代的数量
            return record
        except StopIteration:
            self.current_file_index = self.mbtable_partition.get_next_file_index(self.current_file_index)
            if self.current_file_index is None:
                raise StopIteration
            self.current_pos = 0
            self.iterator.__exit__(None, None, None)
            self.iterator = None  # 重置迭代器以便于下次调用时重新初始化
            return self.__next__()


if __name__ == '__main__':
    mbtable_partition = MbTablePartition('example/mbtable_data/mmdoc/twin')
    total_count = mbtable_partition.get_total_count()
    print(f"total count: {total_count}")
    with MbTablePartitionIterator(mbtable_partition, start_index=0, max_iterations=6) as iterator:
        for row in iterator:
            base_list, image_list = row
            mm_doc_seq = MmDocSeq.from_twin_list(base_list, image_list)
            print(mm_doc_seq)
            for doc in mm_doc_seq.doc_seq:
                if doc.dtype == DocType.IMG:
                    doc.image.save('test.jpg')
            