class IntcodeProgram(object):
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.memory = self.initial_state.copy()
        self.cursor = 0
        self.halted = False

    def _add(self):
        index1 = self.memory[self.cursor + 1]
        index2 = self.memory[self.cursor + 2]
        index3 = self.memory[self.cursor + 3]
        val1 = self.memory[index1]
        val2 = self.memory[index2]

        self.memory[index3] = val1 + val2
        self.cursor += 4

    def _multiply(self):
        index1 = self.memory[self.cursor + 1]
        index2 = self.memory[self.cursor + 2]
        index3 = self.memory[self.cursor + 3]
        val1 = self.memory[index1]
        val2 = self.memory[index2]

        self.memory[index3] = val1 * val2
        self.cursor += 4

    def _halt(self):
        self.halted = True

    def step(self):
        if self.halted:
            return

        opcode = self.memory[self.cursor]
        if opcode == 1:
            self._add()
        elif opcode == 2:
            self._multiply()
        elif opcode == 99:
            self._halt()
        else:
            raise RuntimeError("Unrecognized opcode {} at position {}!".format(opcode, self.cursor))

    def kontinue(self):
        while not self.halted:
            self.step()

    def reset(self):
        self.memory = self.initial_state.copy()
        self.cursor = 0
        self.halted = False

    def run(self, input1=None, input2=None):
        self.reset()
        if input1 is not None:
            self.memory[1] = input1
        if input2 is not None:
            self.memory[2] = input2

        self.kontinue()
        return self.memory[0]


# Part 1
with open('day-2-input.txt') as f:
    data = [int(x) for x in f.readline().strip().split(',')]

program = IntcodeProgram(data)
result = program.run(12, 2)
print(result)

# for Part 2, see day-2-notes.txt
