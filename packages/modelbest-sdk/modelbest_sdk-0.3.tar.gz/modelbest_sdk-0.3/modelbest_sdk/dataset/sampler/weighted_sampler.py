import numpy as np

from modelbest_sdk.dataset.sampler.sampler import Sampler


class WeightedSampler(Sampler):
    def __init__(self, weights, rank, world_size, seed, **kwargs):
        self.weights = weights
        self.n_samples = len(weights)
        np.random.seed(seed)
        
    def __call__(self):
        return np.random.choice(self.n_samples, p=self.weights)
    
    def remove_index(self, index):
        if 0 <= index < self.n_samples:
            # Remove the index by setting its weight to 0
            self.weights[index] = 0
            # Re-normalize the weights
            total_weight = np.sum(self.weights)
            if total_weight > 0:
                self.weights /= total_weight
            else:
                raise ValueError("All weights have been removed.")
        else:
            raise ValueError(f"Index {index} is out of bounds for a dataset with {self.n_samples} samples.")