from intcode import IntcodeComputer

with open('day-5-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()

# Part 1
outputs = computer.run(program, inputs=[1])
print(outputs)

# Part 2
outputs = computer.run(program, inputs=[5])
print(outputs)
