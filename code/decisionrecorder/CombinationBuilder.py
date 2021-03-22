from decisionrecorder.Combination import Combination
from decisionrecorder.Configuration import Configuration
from decisionrecorder.Constants import *


class CombinationBuilder:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def get_combinations(self):
        not_masked_indices = []

        combinations = []

        i = 0
        for m in self.configuration.mask:
            if m != UNKNOWN:
                not_masked_indices.append(i)
            i = i + 1

        number_combinations = pow(2, len(not_masked_indices))

        range_start = 0
        range_end = number_combinations

        if self.configuration.number_parallel_workers is not None and \
                self.configuration.number_worker is not None and \
                self.configuration.number_parallel_workers > 0 and \
                0 <= self.configuration.number_worker < self.configuration.number_parallel_workers:
            count_per_worker = number_combinations / self.configuration.number_parallel_workers

            range_start = int(count_per_worker * self.configuration.number_worker)
            range_end = int(count_per_worker * (self.configuration.number_worker + 1))

        for i in range(range_start, range_end):
            binary = self.decimal_to_binary_list(i)

            field = self.configuration.mask.copy()

            field[int(len(field) / 2)] = HEAD

            j = 0
            binary.reverse()
            for bit in binary:
                if bit == 1:
                    field[not_masked_indices[j]] = BLOCKED
                j = j + 1

            for direction in range(self.configuration.food_directions):
                combinations.append(Combination(field=field, food_direction=direction, number=i))

        return combinations

    @staticmethod
    def decimal_to_binary_list(x):
        if x == 0:
            return [0]

        bit = []
        while x:
            bit.append(x % 2)
            x >>= 1
        return bit[::-1]