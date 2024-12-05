import shutil
import unittest
import torch
from test.test_base import TestBase
from modelbest_sdk.dataset.batch_packer.batch_packer_factory import MEGATRON_BATCH_PACKER
from modelbest_sdk.dataset.sampler.sampler_factory import WEIGHTED_MEGATRON_SAMPLER
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT, CONDITIONAL_FIXED_LENGTH_SEGMENT
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetCheckpointList, DatasetInfo, DatasetInfoList
import os
import torch.distributed as dist
from modelbest_sdk.dataset.modelbest_dataloader import ModelbestDataloader
import torch.multiprocessing as mp

class TestCheckpoint(TestBase):
    def test_save_resume_with_same_settings(self):
        world_size = 2
        TestBase.generate_data(dataset_path='/tmp/text', file_count=1, doc_count_per_file=100, token_count=10, token_offset=1000, mask_pattern='text')
        TestBase.generate_data(dataset_path='/tmp/instruction', file_count=1, doc_count_per_file=10, token_count=10, token_offset=2000, mask_pattern='instruction')
        TestBase.generate_data(dataset_path='/tmp/other_text', file_count=1, doc_count_per_file=10, token_count=10, token_offset=1000, mask_pattern='text')
        mp.spawn(main, args=(world_size,), nprocs=world_size, join=True)
        new_world_size = 4
        mp.spawn(change_world_size, args=(new_world_size,), nprocs=new_world_size, join=True)
        shutil.rmtree('/tmp/text')
        shutil.rmtree('/tmp/instruction')
        shutil.rmtree('iter_10')
        shutil.rmtree('iter_20')
    
def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

def main(rank, world_size):
    setup(rank, world_size)
    from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
    context = DatasetContext(
        rank=rank,
        world_size=world_size,
        dataset_checkpoint_path='',
        seed=rank+world_size,
    )
    dp_group = dist.new_group(ranks=list(range(world_size)))
    dataset_info_list = DatasetInfoList([
        DatasetInfo(
            path='/tmp/text',
            weight=1,
        ),
        DatasetInfo(
            path='/tmp/instruction',
            weight=2,
        ),
        DatasetInfo(
            name='same_text_but_diff_name',
            path='/tmp/text',
            weight=1,
        ),
    ])
    dataloader = ModelbestDataloader(
        context, 
        dataset_info_list, 
        batch_size=2, 
        max_len=16, 
        chunk_size=16,
        segment_type=CONDITIONAL_FIXED_LENGTH_SEGMENT, 
        sampler_type=WEIGHTED_MEGATRON_SAMPLER, 
        batch_packer_type=MEGATRON_BATCH_PACKER,
        dp_group=dp_group
        )
    base_tokens = []
    base_position_ids = []
    base_indexes = []
    base_last_sample = []
    for i, batch in enumerate(dataloader, start=1):
        dataloader.update(batch["indexes"], batch["last_sample"])
        if i == 10:
            dataloader.save('iter_10')
        if i > 20 and i <= 30:
            base_tokens.append(batch['tokens'])
            base_position_ids.append(batch['position_ids'])
            base_indexes.append(batch['indexes'])
            base_last_sample.append(dict(batch['last_sample']))
        if i == 30:
            break
    dist.barrier()
    dataloader.resume('iter_10')
    for i, batch in enumerate(dataloader, start=11):
        dataloader.update(batch["indexes"], batch["last_sample"])
        if i == 20:
            dataloader.save('iter_20')
        if i > 20 and i <= 30:
            assert torch.equal(batch['tokens'], base_tokens[i-21])
            assert torch.equal(batch['position_ids'], base_position_ids[i-21])
            assert batch['indexes'] == base_indexes[i-21]
            assert dict(batch['last_sample']) == base_last_sample[i-21], f"{dict(batch['last_sample'])} != {base_last_sample[i-21]}"
        if i == 30:
            break

    dist.barrier()

    dataloader.resume('iter_20')
    for i, batch in enumerate(dataloader, start=21):
        dataloader.update(batch["indexes"], batch["last_sample"])
        assert torch.equal(batch['tokens'], base_tokens[i-21])
        assert torch.equal(batch['position_ids'], base_position_ids[i-21])
        assert batch['indexes'] == base_indexes[i-21]
        assert dict(batch['last_sample']) == base_last_sample[i-21]
        if i == 30:
            break
        
    new_dataset_info_list = DatasetInfoList([
        DatasetInfo(
            path='/tmp/text',
            weight=0,
        ),
        DatasetInfo(
            path='/tmp/other_text',
            weight=1,
        ),
        DatasetInfo(
            name='same_text_but_diff_name',
            path='/tmp/text',
            weight=1,
        ),
        DatasetInfo(
            path='/tmp/instruction',
            weight=2,
        ),
    ])
    new_dataloader = ModelbestDataloader(
        context, 
        new_dataset_info_list, 
        batch_size=2, 
        max_len=16, 
        chunk_size=16,
        segment_type=CONDITIONAL_FIXED_LENGTH_SEGMENT, 
        sampler_type=WEIGHTED_MEGATRON_SAMPLER, 
        batch_packer_type=MEGATRON_BATCH_PACKER,
        dp_group=dp_group
        )
    new_dataloader.resume('iter_20')
    for i, batch in enumerate(new_dataloader, start=21):
        new_dataloader.update(batch["indexes"], batch["last_sample"])
        print(batch['indexes'])
        print(batch['last_sample'])
        # no bug is good
        if i == 30:
            break
    cleanup()

def change_world_size(rank, world_size):
    setup(rank, world_size)
    from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
    context = DatasetContext(
        rank=rank,
        world_size=world_size,
        dataset_checkpoint_path='',
        seed=rank+world_size,
    )
    dp_group = dist.new_group(ranks=list(range(world_size)))
    dataset_info_list = DatasetInfoList([
        DatasetInfo(
            path='/tmp/text',
            weight=1,
        ),
        DatasetInfo(
            path='/tmp/instruction',
            weight=2,
        ),
        DatasetInfo(
            name='same_text_but_diff_name',
            path='/tmp/text',
            weight=1,
        ),
    ])
    dataloader = ModelbestDataloader(
        context, 
        dataset_info_list, 
        batch_size=2, 
        max_len=16, 
        chunk_size=16,
        segment_type=CONDITIONAL_FIXED_LENGTH_SEGMENT, 
        sampler_type=WEIGHTED_MEGATRON_SAMPLER, 
        batch_packer_type=MEGATRON_BATCH_PACKER,
        dp_group=dp_group
        )
    dataloader.resume('iter_20')
    for i, batch in enumerate(dataloader, start=21):
        dataloader.update(batch["indexes"], batch["last_sample"])
        print(batch['indexes'])
        print(batch['last_sample'])
        # no bug is good
        if i == 40:
            break
    cleanup()
if __name__ == '__main__':
    unittest.main()