with open('input') as f:
    pairs = {'()', '[]', '{}', '<>'}
    illegal_chars = []
    incomplete_stacks = []
    for line in f:
        stack = []
        for c in line:
            if c in '([{<':
                stack.append(c)
            elif c in ')]}>':
                try:
                    prev = stack.pop()
                except IndexError:
                    illegal_chars.append(c)
                    break
                if f'{prev}{c}' not in pairs:
                    illegal_chars.append(c)
                    break
            elif c == '\n':
                incomplete_stacks.append(stack)

part_1_key = {')': 3, ']': 57, '}': 1197, '>': 25137}
part_1_res = sum([part_1_key[c] for c in illegal_chars])
print(part_1_res)

part_2_key = {'(': 1, '[': 2, '{': 3, '<': 4}
scores = []
for stack in incomplete_stacks:
    score = 0
    for c in stack[::-1]:
        score *= 5
        score += part_2_key[c]
    scores.append(score)

part_2_res = sorted(scores)[len(scores) // 2]
print(part_2_res)
