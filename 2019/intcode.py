class IntcodeComputer(object):
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.memory = self.initial_state.copy()
        self.cursor = 0
        self.halted = False

        self.opcodes = {
            1: {'instruction': self._add, 'num_params': 3},
            2: {'instruction': self._multiply, 'num_params': 3},
            99: {'instruction': self._halt, 'num_params': 0}
        }

    def _add(self, read_addr1, read_addr2, write_addr):
        self.memory[write_addr] = self.memory[read_addr1] + self.memory[read_addr2]

    def _multiply(self, read_addr1, read_addr2, write_addr):
        self.memory[write_addr] = self.memory[read_addr1] * self.memory[read_addr2]

    def _halt(self):
        self.halted = True

    def step(self):
        if self.halted:
            return

        opcode_identifier = self.memory[self.cursor]
        try:
            opcode = self.opcodes[opcode_identifier]
        except KeyError:
            raise RuntimeError("Unrecognized opcode {} at position {}!".format(opcode, self.cursor))

        params = self.memory[(self.cursor + 1):(self.cursor + 1 + opcode['num_params'])]
        opcode['instruction'](*params)
        self.cursor += 1 + opcode['num_params']

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
