import math
import random


def random_range(start, stop=None, step=None):
    """
    Generator of non-repeated random permutation with the same inteface of python
    `range`. Obtained from https://stackoverflow.com/a/53551417
    The random.shuffle(list) and random.sample(list, len(list)) require
    materialize the lists, which result in a long initalization period.
    """
    if stop is None:
        start, stop = 0, start
    if step is None:
        step = 1
    # Use a mapping to convert a standard range into the desired range.
    mapping = lambda i: (i * step) + start
    # Compute the number of numbers in this range.
    maximum = int(math.ceil((stop - start) / step))
    if maximum == 0:
        # early return with empty range
        yield from ()
        return
    # Seed range with a random integer.
    value = random.randint(0, maximum)
    # Construct an offset, multiplier, and modulus for a linear
    # congruential generator. These generators are cyclic and
    # non-repeating when they maintain the properties:
    #
    #   1) "modulus" and "offset" are relatively prime.
    #   2) ["multiplier" - 1] is divisible by all prime factors of "modulus".
    #   3) ["multiplier" - 1] is divisible by 4 if "modulus" is divisible by 4.

    # Pick a random odd-valued offset.
    offset = random.randint(0, maximum) * 2 + 1
    # Pick a multiplier 1 greater than a multiple of 4.
    multiplier = 4 * (maximum // 4) + 1
    # Pick a modulus just big enough to generate all numbers (power of 2).
    modulus = int(2 ** math.ceil(math.log2(maximum)))
    # Track how many random numbers have been returned.
    found = 0
    while found < maximum:
        # If this is a valid value, yield it in generator fashion.
        if value < maximum:
            found += 1
            yield mapping(value)
        # Calculate the next value in the sequence.
        value = (value * multiplier + offset) % modulus


class Range(object):
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        return f"Range({self.start}, {self.stop}, {self.step})"

    def iterate(self):
        yield from range(self.start, self.stop, self.step)

    def list(self):
        return list(range(self.start, self.stop, self.step))

    def subrange(self, split, nsplits):
        # strided spliting range params
        # e.g., [0, 3, 5, 7, 9] can be split into [0, 5, 9] and [3, 7]
        return Range(self.start + self.step * split, self.stop, self.step * nsplits)

    def random_iterate(self):
        yield from random_range(self.start, self.stop, self.step)
