from collections import Counter


def decode(signals):
    char_map = {}
    count = Counter(''.join(signals))
    for k, v in count.items():
        if v == 4:
            char_map[k] = set('e')
        elif v == 6:
            char_map[k] = set('b')
        elif v == 7:
            char_map[k] = set('dg')
        elif v == 8:
            char_map[k] = set('ac')
        else:
            char_map[k] = set('f')

    segments = set('abcdefg')
    one, seven, four = [set(x) for x in sorted(signals, key=len)[:3]]

    # differentiate a and c
    for c in seven - one:
        char_map[c] = set('a')
    for c in segments - (seven - one):
        char_map[c] -= set('a')

    # differentiate d and g
    for c in four - one:
        char_map[c] &= set('bd')
    for c in segments - (four - one):
        char_map[c] -= set('bd')

    return {k: list(v)[0] for k, v in char_map.items()}


data = []
with open('input') as f:
    for line in f:
        data.append(line.strip().split())

part_1_res = len([x for d in data for x in d[-4:] if len(x) in (2, 3, 4, 7)])
print(part_1_res)

digits = {
    'abcefg': '0',
    'cf': '1',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9'
}
part_2_res = 0
for d in data:
    char_map = str.maketrans(decode(d[:10]))
    output = [''.join(sorted(x.translate(char_map))) for x in d[-4:]]
    output_num = int(''.join([digits[x] for x in output]))
    part_2_res += output_num

print(part_2_res)
