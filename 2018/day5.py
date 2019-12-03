# This is a brute force solution that takes a long time.


def collapse_polymer(polymer):
    polymer_list = list(polymer)
    while True:
        start_len = len(polymer_list)
        for i in range(start_len-1):
            if (polymer_list[i].upper() == polymer_list[i + 1].upper() and
                    (polymer_list[i].isupper() and polymer_list[i + 1].islower() or
                     polymer_list[i].islower() and polymer_list[i + 1].isupper())
            ):
                del polymer_list[i:i + 2]
                break
        end_len = len(polymer_list)
        if start_len == end_len:
            break
    return ''.join(polymer_list)


# Part 1
with open('day-5-input.txt') as f:
    polymer = f.readline().strip()

collapsed_polymer = collapse_polymer(polymer)
print(len(collapsed_polymer))

# Part 2
for unit in 'abcdefghijklmnopqrstuvwxyz':
    polymer_list = [c for c in collapsed_polymer if c != unit and c != unit.upper()]
    print(f"With {unit} removed, collapsed length is: {len(collapse_polymer(polymer_list))}")
