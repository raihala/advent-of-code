import re
from collections import defaultdict, namedtuple

EnginePart = namedtuple('EnginePart', ['value', 'row', 'start_col', 'end_col'])

with open('input') as f:
    data = [line.strip() for line in f]

possible_engine_parts = []
for row in range(len(data)):
    matches = re.finditer('[0-9]+', data[row])
    for match in matches:
        possible_engine_parts.append(EnginePart(
            value=int(match.group(0)),
            row=row,
            start_col=match.start(),
            end_col=match.end()
        ))

part_one_res = 0
possible_gears = defaultdict(list)  # will map gear coordinates to lists of adjacent engine part numbers
for part in possible_engine_parts:
    is_engine_part = False
    for row in range(part.row - 1, part.row + 2):
        for col in range(part.start_col - 1, part.end_col + 1):
            try:
                if data[row][col] not in '0123456789.':
                    is_engine_part = True
                    if data[row][col] == '*':
                        possible_gears[(row, col)].append(part.value)
            except IndexError:
                continue
    if is_engine_part:
        part_one_res += part.value

part_two_res = 0
for adjacent_part_nos in possible_gears.values():
    if len(adjacent_part_nos) == 2:  # it's a gear!
        gear_ratio = adjacent_part_nos[0] * adjacent_part_nos[1]
        part_two_res += gear_ratio

print(part_one_res)
print(part_two_res)
