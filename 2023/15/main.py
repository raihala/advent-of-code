from collections import defaultdict


def holiday_hash(string):
    res = 0
    for char in string:
        res += ord(char)
        res *= 17
        res %= 256
    return res


with open('input') as f:
    data = next(f).strip().split(',')

part_one_res = 0
boxes = defaultdict(list)
focal_lengths = defaultdict(dict)

for step in data:
    part_one_res += holiday_hash(step)
    if '-' in step:
        label = step[:-1]
        box = holiday_hash(label)
        try:
            boxes[box].remove(label)
        except ValueError:
            pass
    elif '=' in step:
        label = step[:-2]
        focal_length = int(step[-1])
        box = holiday_hash(label)
        focal_lengths[box][label] = focal_length
        if label not in boxes[box]:
            boxes[box].append(label)

part_two_res = 0
for box, lenses in boxes.items():
    for i in range(len(lenses)):
        focusing_power = (box + 1) * (i + 1) * focal_lengths[box][lenses[i]]
        part_two_res += focusing_power

print(part_one_res)
print(part_two_res)
