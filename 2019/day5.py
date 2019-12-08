from intcode import IntcodeComputer

# Part 1
with open('day-5-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()
computer.run(program)
