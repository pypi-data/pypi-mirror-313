import numpy as np

from modelbest_sdk.dataset.sampler.sampler import Sampler


class WeightedMegatronSampler(Sampler):
    def __init__(self, weights, rank, world_size, seed, **kwargs):
        self.weights = np.array(weights)
        self.rank = rank
        self.world_size = world_size
        self.sample_idx = 0
        self.current_samples = np.zeros(len(self.weights), dtype=np.int64)
        self.kwargs = kwargs
        self.generator = self.generate_indices()
        for _ in range(self.rank):
            next(self.generator)
                    
    def generate_indices(self):
        while True:
            errors = self.weights * self.sample_idx - self.current_samples
            max_error_index = np.argmax(errors)
            self.current_samples[max_error_index] += 1
            yield max_error_index
            self.sample_idx += 1

    def __call__(self):
        index = next(self.generator)
        for _ in range(self.world_size - 1):
            next(self.generator)
        return index
    
    def resume(self, sample_idx, current_samples):
        self.sample_idx = sample_idx
        self.current_samples = current_samples
        self.generator = self.generate_indices()
        for _ in range(self.rank):
            next(self.generator)
    
if __name__ == '__main__':
    weights = [0.39, 0.11, 0.05, 0.08, 0.05, 0.02, 0.24, 0.06]
    rank = 15
    world_size = 16
    
    sampler = WeightedMegatronSampler(weights, rank, world_size)
    for i in range(30):
        print(sampler())