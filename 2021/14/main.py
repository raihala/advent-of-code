from collections import Counter

RULES = {}
COUNT = {}


def count(string, steps):
    if steps == 0:
        return Counter(string)
    elif (string, steps) in COUNT:
        return COUNT[(string, steps)]
    counter = Counter()
    for i in range(1, len(string)):
        pair = string[i-1:i+1]
        new_string = pair[0] + RULES[pair] + pair[1]
        subcounter = count(new_string, steps-1)
        COUNT[(new_string, steps-1)] = subcounter
        counter += subcounter
    for interior_char in string[1:len(string)-1]:
        # need to adjust for double counting
        counter[interior_char] -= 1
    COUNT[(string, steps)] = counter
    return counter


with open('input') as f:
    polymer = next(f).strip()
    next(f)
    for line in f:
        pair, element = line.strip().split(' -> ')
        RULES[pair] = element


part_1_count = count(polymer, 10)
part_1_sorted = part_1_count.most_common()
part_1_res = part_1_sorted[0][1] - part_1_sorted[-1][1]
print(part_1_res)

part_2_count = count(polymer, 40)
part_2_sorted = part_2_count.most_common()
part_2_res = part_2_sorted[0][1] - part_2_sorted[-1][1]
print(part_2_res)
