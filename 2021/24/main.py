div = []
add1 = []
add2 = []

with open('input') as f:
    for i in range(14):
        for _ in range(4):
            next(f)
        div.append(int(next(f).strip().split()[-1]))
        add1.append(int(next(f).strip().split()[-1]))
        for _ in range(9):
            next(f)
        add2.append(int(next(f).strip().split()[-1]))
        for _ in range(2):
            next(f)

pairs = []
stack = []
for i in range(14):
    if div[i] == 1:
        stack.append(i)
    else:
        pairs.append((stack.pop(), i))

digits_max = [0] * 14
digits_min = [0] * 14
for i, j in pairs:
    offset = add1[j] + add2[i]

    di_max = 9 - max(offset, 0)
    dj_max = di_max + offset
    digits_max[i] = di_max
    digits_max[j] = dj_max

    di_min = max(1, 1 - offset)
    dj_min = di_min + offset
    digits_min[i] = di_min
    digits_min[j] = dj_min

part_1_res = ''.join([str(d) for d in digits_max])
part_2_res = ''.join([str(d) for d in digits_min])
print(part_1_res)
print(part_2_res)
