with open('input') as f:
    data = next(f).strip()

part_1_res = 0
part_2_res = 0

for i in range(len(data)):
    if not part_1_res and len(set(data[i:i + 4])) == 4:
        part_1_res = i + 4
    if len(set(data[i:i + 14])) == 14:
        part_2_res = i + 14
        break

print(part_1_res)
print(part_2_res)
