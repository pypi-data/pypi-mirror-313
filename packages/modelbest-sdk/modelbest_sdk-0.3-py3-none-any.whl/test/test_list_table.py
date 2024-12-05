import json
import os
import unittest
import sys
import thriftpy2
from thriftpy2.utils import deserialize, serialize

cur_path = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(cur_path, "../")))

from modelbest_sdk.dataset.thrift_wrapper.metadata import SSTableMetadata
from modelbest_sdk.file_format.mbtable import MbTable, MbTableListIterator
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder

metadata_thrift = thriftpy2.load('modelbest_sdk/proto/metadata.thrift')


class TestListTable(unittest.TestCase):
    def setUp(self):
        self.path = "test/data/list_table.mbt"
        builder = MbTableBuilder(self.path)
        for i in range(10):
            values=[]
            for j in range(9):
                values.append(json.dumps({"col": f"value_{i}_{j}"}))
            values.append("")
            builder.write_list(values)
        meta = metadata_thrift.SSTableMetadata(
                tabletype=metadata_thrift.TableType.LIST_TABLE,
                total_count=10)
        builder.add_metadata('metadata', serialize(meta))
        builder.add_metadata('other', 'value')
        builder.flush()
        self.mbtable = MbTable(self.path)
    
    def tearDown(self):
        os.remove(self.path)
    
    def test_get_metadata(self):
        meta = SSTableMetadata.deserialize(self.mbtable.get_metadata('metadata'))
        self.assertEqual('LIST_TABLE', meta.table_type)
        self.assertEqual(10, meta.total_count)
        self.assertEqual(b'value', self.mbtable.get_metadata('other'))
        self.assertEqual(b'', self.mbtable.get_metadata('not_exist'))

        meta = SSTableMetadata.deserialize(self.mbtable.get_file_metadata('metadata'))
        self.assertEqual('LIST_TABLE', meta.table_type)
        self.assertEqual(10, meta.total_count)
        self.assertEqual(b'value', self.mbtable.get_file_metadata('other'))
        self.assertEqual(b'', self.mbtable.get_file_metadata('not_exist'))
        
        meta = SSTableMetadata.deserialize(self.mbtable.get_file_metadata('non_exist'))
        self.assertEqual(None, meta.table_type)
        self.assertEqual(None, meta.total_count)

    def test_get_entry_count(self):
        self.assertEqual(self.mbtable.get_entry_count(), 100)
        self.assertEqual(self.mbtable.get_file_entry_count(), 100)
        self.assertEqual(10, self.mbtable.get_entry_count_from_metadata())

    def test_get_record(self):
        with self.assertRaises(TypeError):
            self.mbtable.read(0)

    def test_get_list(self):
        for i in range(10): 
            values=[]
            for j in range(9):
                values.append(json.dumps({"col": f"value_{i}_{j}"}).encode())
            values.append(b"")
            self.assertEqual(values, self.mbtable.read_list(i)) 


class TestMbTableListIterator(TestListTable):
    def test_iterator(self):
        cnt = 0
        with MbTableListIterator(self.path) as iterator:
            expected = []
            for i in range(10):
                values = []
                for j in range(9):
                    values.append(json.dumps({"col": f"value_{i}_{j}"}).encode())
                values.append(b"")
                expected.append(values)
            for record in iterator:
                self.assertEqual(expected[cnt], record)
                cnt += 1
        assert cnt == 10
    
    def test_iterator_raw(self):
        iterator = MbTableListIterator(self.path)
        iterator.__enter__()
        record = iterator.__next__()
        iterator.__exit__(None, None, None)
        expected =[]
        for j in range(9):
            expected.append(json.dumps({"col": f"value_0_{j}"}).encode())
        expected.append(b"")
        self.assertEqual(expected, record)
        pass
        

    def test_iterator_with_args(self):
        key, cnt = 5, 0
        with MbTableListIterator(self.path, start_index=key, max_iterations=2) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 2
        
        key, cnt = 9, 0
        with MbTableListIterator(self.path, start_index=key, max_iterations=1000) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 1
    
        key, cnt = 1000, 0
        # !!! note that key in mbtable is string and is sorted in lexicographic order
        # so key 1000 is greater than 10 but less than 11, this would start from 11
        with MbTableListIterator(self.path, start_index=key, max_iterations=1000) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 0


if __name__ == '__main__':
    unittest.main()
