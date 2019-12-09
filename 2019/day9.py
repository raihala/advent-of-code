from intcode import IntcodeComputer

with open('day-9-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()

# Part 1
outputs = computer.run(program, [1])
print(outputs)

# Part 2
outputs = computer.run(program, [2])
print(outputs)
