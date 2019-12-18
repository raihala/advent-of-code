import itertools
from operator import mul


def calculate_pattern(multiplier):
    base_pattern = [0, 1, 0, -1]
    full_pattern = itertools.chain.from_iterable([itertools.repeat(n, multiplier) for n in base_pattern])
    infinite_pattern = itertools.cycle(full_pattern)
    next(infinite_pattern)  # skip first element
    return infinite_pattern


def phase(input_list):
    output_list = []
    for n in range(len(input_list)):
        pattern = calculate_pattern(n+1)
        output_element = abs(sum(map(mul, input_list, pattern))) % 10
        output_list.append(output_element)
    return output_list


with open('day-16-input.txt') as f:
    data = [int(char) for char in f.readline().strip()]

for _ in range(100):
    data = phase(data)

print(''.join([str(c) for c in data[:8]]))
