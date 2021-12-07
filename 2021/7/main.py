with open('input') as f:
    data = sorted([int(x) for x in next(f).strip().split(',')])

# part 1 best is a/the median
median = data[len(data) // 2]
part_1_cost = sum([abs(x - median) for x in data])
print(part_1_cost)

# part 2 best is likely very close to the mean so this
# should work. if it doesn't, expand the search range.
mean = sum(data) // len(data)
part_2_cost = 10 ** 100
for n in range(mean - 10, mean + 10):
    cost = 0
    for x in data:
        d = abs(x - n)
        cost += d * (d + 1) // 2
    if cost < part_2_cost:
        part_2_cost = cost

print(part_2_cost)
