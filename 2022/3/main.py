def priority(char):
    if char.islower():
        return ord(char) - 96
    else:
        return ord(char) - 38


with open('input') as f:
    data = [line.strip() for line in f]

part_1_res = 0
for line in data:
    half = len(line) // 2
    for char in line[:half]:
        if char in line[half:]:
            part_1_res += priority(char)
            break

part_2_res = 0
for i in range(0, len(data), 3):
    for char in data[i]:
        if char in data[i+1] and char in data[i+2]:
            part_2_res += priority(char)
            break

print(part_1_res)
print(part_2_res)
