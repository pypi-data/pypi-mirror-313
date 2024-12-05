import unittest

from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext

class TestDatasetContext(unittest.TestCase):
    def test_read_from_file(self):
        simple_dataset_context = DatasetContext(
            rank=1,
            world_size=10,
            dataset_config_path="/path/to/dataset_config",
            dataset_checkpoint_path="/path/to/checkpoint",
        )
        simple_dataset_context.save_to_file("/tmp/test_context.mbt")
        new_context = DatasetContext.load_from_file("/tmp/test_context.mbt")
        assert new_context.rank == simple_dataset_context.rank
        assert new_context.world_size == simple_dataset_context.world_size
        assert new_context.dataset_config_path == simple_dataset_context.dataset_config_path
        assert new_context.dataset_checkpoint_path == simple_dataset_context.dataset_checkpoint_path
