from modelbest_sdk.dataset.sampler.weighted_megatron_sampler import WeightedMegatronSampler
from modelbest_sdk.dataset.sampler.weighted_sampler import WeightedSampler

WEIGHTED_SAMPLER = 'weighted_sampler'
WEIGHTED_MEGATRON_SAMPLER = 'weighted_megatron_sampler'

class SamplerFactory:
    @staticmethod
    def create_sampler(sampler_type, weights, rank, world_size, seed=None, **kwargs):
        if sampler_type == WEIGHTED_SAMPLER:
            return WeightedSampler(weights, rank, world_size, seed, **kwargs)
        elif sampler_type == WEIGHTED_MEGATRON_SAMPLER:
            return WeightedMegatronSampler(weights, rank, world_size, seed, **kwargs)
        else:
            raise ValueError(f"Unsupported sampler type: {sampler_type}")