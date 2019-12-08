from intcode import IntcodeComputer


# Part 1
with open('day-2-input.txt') as f:
    data = [int(x) for x in f.readline().strip().split(',')]

program = IntcodeComputer(data)
result = program.run(12, 2)
print(result)

# for Part 2, see day-2-notes.txt
