import os
import unittest
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder
from modelbest_sdk.file_format.mbtable_partition import MbTablePartition, MbTablePartitionIterator


class TestMbTablePartition(unittest.TestCase):
    def setUp(self):
        for i in range(10):
            builder = MbTableBuilder(f"test/partition_data/part_{i}.mbt")
            for j in range(100):
                builder.write(str({"col": f"value_{j}"}))
            builder.add_metadata("meta_key", "meta_value")
            builder.flush()
        self.mbtable_partition = MbTablePartition("test/partition_data")
    
    def tearDown(self):
        for i in range(10):
            file_path = f"test/partition_data/part_{i}.mbt"
            if os.path.exists(file_path):
                os.remove(file_path)
                
    def test_get_total_count(self):
        self.mbtable_partition.get_total_count()
        assert self.mbtable_partition.total_count == 1000
                
    def test_get_file_and_position(self):
        index, postion = self.mbtable_partition.get_file_index_and_position(0)
        assert index == 0
        assert postion == 0
        
        index, postion = self.mbtable_partition.get_file_index_and_position(999)
        assert index == 9
        assert postion == 99
        
        index, postion = self.mbtable_partition.get_file_index_and_position(1001)
        assert index == None
        assert postion == None

    
    def test_get_next_file(self):
        next_file_index = self.mbtable_partition.get_next_file_index(0)
        assert next_file_index == 1
        
        next_file_index = self.mbtable_partition.get_next_file_index(9)
        assert next_file_index == None
        
class TestMbTablePartitionIterator(TestMbTablePartition):
    def test_iterator(self):
        cnt = 0
        with MbTablePartitionIterator(self.mbtable_partition, start_index=0, max_iterations=1000) as iterator:
            for i, record in enumerate(iterator):
                assert record == str({"col": f"value_{i%100}"}).encode()          
                cnt += 1
                assert iterator.current_file_index == i // 100
        assert cnt == 1000


if __name__ == '__main__':
    unittest.main()