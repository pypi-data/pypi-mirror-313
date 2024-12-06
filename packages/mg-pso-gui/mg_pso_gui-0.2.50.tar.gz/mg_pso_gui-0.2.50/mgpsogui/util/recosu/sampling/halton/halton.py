from collections.abc import Iterable
import math
from ...sampling.halton.prime import generate_n_primes


def halton(index: int, base: int) -> float:
    fraction: float = 1.0
    result: float = 0

    while index > 0:
        fraction = fraction / base
        result += fraction * (index % base)
        index = math.floor(index / base)

    return result


class HaltonSampleGenerator:
    index: int
    maxIndex: int
    primes: list[int]

    def __init__(self, count: int, offset: int, num_parameters: int):
        assert (count > 0)
        assert (offset >= 0)
        self.index = offset + 1
        self.maxIndex = offset + count + 1
        self.primes = generate_n_primes(num_parameters)

    def __iter__(self) -> Iterable[tuple[int, list[float]]]:
        return self

    def __next__(self) -> tuple[int, list[float]]:
        if self.index >= self.maxIndex:
            raise StopIteration

        i = 0
        values: list[float] = []
        for base in self.primes:
            values.append(halton(self.index, base))

        result: tuple[int, list[float]] = (self.index, values)
        self.index = self.index + 1
        return result

