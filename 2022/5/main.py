import re

part_1_data = [[] for _ in range(9)]
part_2_data = [[] for _ in range(9)]

with open('input') as f:
    line = next(f)
    while line[1] != '1':
        for index in range(len(line)):
            char = line[index]
            if char.isalpha():
                part_1_data[(index - 1) // 4].insert(0, char)
                part_2_data[(index - 1) // 4].insert(0, char)
        line = next(f)

    next(f)

    pattern = 'move ([0-9]+) from ([0-9]) to ([0-9])'
    for line in f:
        match = re.match(pattern, line)
        num_to_move, from_stack, to_stack = map(int, match.groups())

        bottom = part_1_data[from_stack - 1][:-num_to_move]
        top = part_1_data[from_stack - 1][-num_to_move:]
        part_1_data[from_stack - 1] = bottom
        part_1_data[to_stack - 1].extend(top[::-1])

        bottom = part_2_data[from_stack - 1][:-num_to_move]
        top = part_2_data[from_stack - 1][-num_to_move:]
        part_2_data[from_stack - 1] = bottom
        part_2_data[to_stack - 1].extend(top)

part_1_res = ''.join([stack[-1] for stack in part_1_data])
part_2_res = ''.join([stack[-1] for stack in part_2_data])

print(part_1_res)
print(part_2_res)
