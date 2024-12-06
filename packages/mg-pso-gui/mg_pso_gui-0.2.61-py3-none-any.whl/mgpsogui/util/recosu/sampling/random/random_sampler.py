from collections.abc import Iterable
import random


class RandomSampleGenerator:
    index: int
    count: int
    num_parameters: int
    rand: random.Random

    def __init__(self, count: int, num_parameters: int):
        assert (count > 0)
        self.index = 1
        self.count = count + 1
        self.num_parameters = num_parameters
        self.rand = random.Random()

    def __iter__(self) -> Iterable[tuple[int, list[float]]]:
        return self

    def __next__(self) -> tuple[int, list[float]]:
        if self.index >= self.count:
            raise StopIteration

        i: int = 0
        values: list[float] = []
        while i < self.num_parameters:
            values.append(self.rand.uniform(0, 1))
            i = i + 1

        result: tuple[int, list[float]] = (self.index, values)
        self.index = self.index + 1
        return result

