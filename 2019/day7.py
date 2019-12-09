from intcode import IntcodeComputer

with open('day-7-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()


def max_output(amplifiers, input_signal, available_phases):
    """
    Recursively determine the maximum possible output phase
    """
    # base case
    if amplifiers == 0:
        return input_signal

    outputs = []
    for phase in available_phases:
        remaining_phases = available_phases.copy()
        remaining_phases.remove(phase)
        output = max_output(
            amplifiers=amplifiers-1,
            input_signal=computer.run(program, [phase, input_signal])[0],
            available_phases=remaining_phases
        )
        outputs.append(output)

    return max(outputs)


res = max_output(5, 0, list(range(5)))  # range object doesn't have remove
print(res)
