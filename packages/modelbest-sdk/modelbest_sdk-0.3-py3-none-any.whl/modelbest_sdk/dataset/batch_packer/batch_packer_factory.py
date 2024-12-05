from modelbest_sdk.dataset.batch_packer.audio_batch_packer import AudioBatchPacker
from modelbest_sdk.dataset.batch_packer.cpm_flash_attn_batch_packer import CpmFlashAttnBatchPacker
from modelbest_sdk.dataset.batch_packer.megatron_batch_packer import MegatronBatchPacker
from modelbest_sdk.dataset.batch_packer.mmseq_batch_packer import MmSeqBatchPacker


CPM_FLASH_ATTN_BATCH_PACKER = "cpm_flash_attn_batch_packer"
MEGATRON_BATCH_PACKER = "megatron_batch_packer"
AUDIO_BATCH_PACKER = "audio_batch_packer"
MMSEQ_BATCH_PACKER = "mmseq_batch_packer"

class BatchPackerFactory:
    @staticmethod
    def create_batch_packer(batch_packer_type, batch_size, max_len, dataset_cnt, **kwargs):
        packer_class = BatchPackerRegistry.get_batch_packer(batch_packer_type)
        return packer_class(batch_size, max_len, dataset_cnt, **kwargs)

    @staticmethod
    def collate_fn(batch_packer_type):
        return BatchPackerRegistry.get_collate_fn(batch_packer_type)

class BatchPackerRegistry:
    _registry = {}

    @classmethod
    def register_batch_packer(cls, key, packer_class):
        if key in cls._registry:
            raise ValueError(f"Batch packer type '{key}' is already registered.")
        cls._registry[key] = packer_class

    @classmethod
    def get_batch_packer(cls, key):
        if key not in cls._registry:
            raise ValueError(f"Unsupported batch packer type: {key}")
        return cls._registry[key]

    @classmethod
    def get_collate_fn(cls, key):
        packer_class = cls.get_batch_packer(key)
        return packer_class.collate_fn

BatchPackerRegistry.register_batch_packer(CPM_FLASH_ATTN_BATCH_PACKER, CpmFlashAttnBatchPacker)
BatchPackerRegistry.register_batch_packer(MEGATRON_BATCH_PACKER, MegatronBatchPacker)
BatchPackerRegistry.register_batch_packer(AUDIO_BATCH_PACKER, AudioBatchPacker)
BatchPackerRegistry.register_batch_packer(MMSEQ_BATCH_PACKER, MmSeqBatchPacker)