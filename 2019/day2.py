class IntcodeProgram(object):
    def __init__(self, program):
        self.program = program
        self.cursor = 0
        self.halted = False

    def _add(self):
        index1 = self.program[self.cursor + 1]
        index2 = self.program[self.cursor + 2]
        index3 = self.program[self.cursor + 3]
        val1 = self.program[index1]
        val2 = self.program[index2]

        self.program[index3] = val1 + val2
        self.cursor += 4

    def _multiply(self):
        index1 = self.program[self.cursor + 1]
        index2 = self.program[self.cursor + 2]
        index3 = self.program[self.cursor + 3]
        val1 = self.program[index1]
        val2 = self.program[index2]

        self.program[index3] = val1 * val2
        self.cursor += 4

    def _halt(self):
        self.halted = True

    def step(self):
        if self.halted:
            return

        opcode = self.program[self.cursor]
        if opcode == 1:
            self._add()
        elif opcode == 2:
            self._multiply()
        elif opcode == 99:
            self._halt()
        else:
            raise RuntimeError("Unrecognized opcode {} at position {}!".format(opcode, self.cursor))

    def run(self):
        while not self.halted:
            self.step()


# Part 1
with open('day-2-input.txt') as f:
    data = [int(x) for x in f.readline().strip().split(',')]

# reset to 1202 Program Alarm state
data[1] = 12
data[2] = 2

program = IntcodeProgram(data)
program.run()
print(program.program[0])
