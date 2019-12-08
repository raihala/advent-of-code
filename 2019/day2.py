from intcode import IntcodeComputer


# Part 1
with open('day-2-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]
program[1] = 12
program[2] = 2

computer = IntcodeComputer()
computer.run(program)
result = computer.memory[0]
print(result)

# for Part 2, see day-2-notes.txt
