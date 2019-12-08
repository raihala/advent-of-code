class IntcodeComputer(object):
    def __init__(self):
        self.memory = []
        self.cursor = 0
        self.halted = False

        self.opcodes = {
            1: {'instruction': self._add, 'num_params': 3},
            2: {'instruction': self._multiply, 'num_params': 3},
            3: {'instruction': self._input, 'num_params': 1},
            4: {'instruction': self._output, 'num_params': 1},
            99: {'instruction': self._halt, 'num_params': 0}
        }

    def _add(self, read_addr1, read_addr2, write_addr):
        self.memory[write_addr] = self.memory[read_addr1] + self.memory[read_addr2]

    def _multiply(self, read_addr1, read_addr2, write_addr):
        self.memory[write_addr] = self.memory[read_addr1] * self.memory[read_addr2]

    def _input(self, write_addr):
        val = input("Input instruction expects user input: ")
        self.memory[write_addr] = val.strip()

    def _output(self, read_addr):
        return self.memory[read_addr]

    def _halt(self):
        self.halted = True

    def step(self):
        if self.halted:
            return

        opcode_identifier = self.memory[self.cursor]
        try:
            opcode = self.opcodes[opcode_identifier]
        except KeyError:
            raise RuntimeError("Unrecognized opcode {} at address {}!".format(opcode_identifier, self.cursor))

        params = self.memory[(self.cursor + 1):(self.cursor + 1 + opcode['num_params'])]
        output = opcode['instruction'](*params)
        if output:
            print("Opcode {} at address {} yielded output: {}".format(opcode_identifier, self.cursor, output))
        self.cursor += 1 + opcode['num_params']

    def kontinue(self):
        while not self.halted:
            self.step()

    def reset(self):
        self.cursor = 0
        self.halted = False

    def run(self, program):
        self.reset()
        self.memory = program
        self.kontinue()
