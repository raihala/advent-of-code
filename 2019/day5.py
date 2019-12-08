from intcode import IntcodeComputer

with open('day-5-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

# For Part 1, input 1 when prompted. For Part 2, input 5.
computer = IntcodeComputer()
computer.run(program)
