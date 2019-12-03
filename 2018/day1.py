import math
from collections import defaultdict

# Part 1
with open('day-1-input.txt') as f:
    frequencies = [int(line.strip()) for line in f]

sum_frequencies = sum(frequencies)
print(sum_frequencies)

# Part 2
"""
from the n frequencies {f1, ... fn} we get sums {S1, ... Sn}
iterated = {S1, ... Sn, S1 + SUM, ... Sn + SUM, S1 + SUM*2, ... }
what is the first time that two sums are the same?
ie what is the first time that Sa + SUM*c = Sb + SUM*d, where Sa, Sb in {S1, ... Sn} and WLOG d >= c >= 0?
=> what is the first time that Sa = Sb + SUM(d - c)?
=> what is the smallest k for which there exist Sa, Sb such that Sa = Sb + SUM*k?
For each i in 0...(SUM - 1), we can find all S in {S1, ... Sn} ~= i % SUM.
Then for each set, we can find the smallest difference between two sums.
If there is a tie, we want the pair where the SMALLER number occurs the earliest.
"""
sums = [0]
for f in frequencies:
    sums.append(f + sums[-1])
sums = sums[1:]  # 0 isn't included in the sums that are iterated upon

congruence_classes = defaultdict(list)
for s in sums:
    congruence_classes[s % sum_frequencies].append(s)
congruence_classes = [sorted(v) for v in congruence_classes.values() if len(v) > 1]

min_diff = math.inf
min_index = math.inf
for cclass in congruence_classes:
    for i in range(len(cclass) - 1):
        diff = cclass[i + 1] - cclass[i]
        index = sums.index(cclass[i])  # again, we want the index of the SMALLER sum
        if diff < min_diff:
            min_diff = diff
            min_index = index
        elif diff == min_diff:
            min_index = min(min_index, index)

index_a = min_index
freq_a = sums[min_index]
freq_b = freq_a + min_diff
index_b = sums.index(freq_b)
print("sums[{}]={}, sums[{}]={}. {} is the first repeated frequency"
      .format(index_a, freq_a, index_b, freq_b, freq_b)
)
