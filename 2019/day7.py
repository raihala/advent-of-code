from intcode import IntcodeComputer
from itertools import permutations

with open('day-7-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]


def find_max_output(phases, program):
    computers = [IntcodeComputer() for _ in range(len(phases))]
    phase_permutations = permutations(phases)

    max_output = 0
    for permutation in phase_permutations:
        # initialize computers, set initial IO signal to 0
        for i in range(5):
            computers[i].load(program, [permutation[i]])
        io_signals = [0]

        # continue looping through computers until all have halted
        while not all([c.halted for c in computers]):
            for c in computers:
                c.send_inputs(io_signals)
                io_signals = c.kontinue()

        output = io_signals[0]
        max_output = max(max_output, output)

    return max_output


part_1_answer = find_max_output(range(0, 5), program)
part_2_answer = find_max_output(range(5, 10), program)

print(part_1_answer)
print(part_2_answer)
