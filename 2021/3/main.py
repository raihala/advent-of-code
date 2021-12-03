"""
Day 3 Part 2
"""

with open('input') as f:
    data = [line.strip() for line in f]

oxygen = data
for i in range(12):
    zeroes = [x for x in oxygen if x[i] == '0']
    ones = [x for x in oxygen if x[i] == '1']
    if len(ones) >= len(zeroes):
        oxygen = ones
    else:
        oxygen = zeroes
    if len(oxygen) == 1:
        oxygen = int(oxygen[0], base=2)
        break

co2 = data
for i in range(12):
    zeroes = [x for x in co2 if x[i] == '0']
    ones = [x for x in co2 if x[i] == '1']
    if len(ones) < len(zeroes):
        co2 = ones
    else:
        co2 = zeroes
    if len(co2) == 1:
        co2 = int(co2[0], base=2)
        break

print(oxygen * co2)
