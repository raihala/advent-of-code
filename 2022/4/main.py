import re

part_1_res = 0
part_2_res = 0
with open('input') as f:
    pattern = '([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)'
    for line in f:
        match = re.match(pattern, line)
        min1, max1, min2, max2 = map(int, match.groups())
        if (min1 <= min2 and max1 >= max2) or (min2 <= min1 and max2 >= max1):
            part_1_res += 1
        if (min1 <= min2 <= max1) or (min2 <= min1 <= max2):
            part_2_res += 1

print(part_1_res)
print(part_2_res)
