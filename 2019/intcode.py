from itertools import zip_longest


class IntcodeComputer(object):
    def __init__(self):
        self.memory = []
        self.cursor = 0
        self.halted = False

        self.opcodes = {
            1: {'function': self._add, 'num_params': 3, 'moves_cursor': False},
            2: {'function': self._multiply, 'num_params': 3, 'moves_cursor': False},
            3: {'function': self._input, 'num_params': 1, 'moves_cursor': False},
            4: {'function': self._output, 'num_params': 1, 'moves_cursor': False},
            5: {'function': self._jump_if_true, 'num_params': 2, 'moves_cursor': True},
            6: {'function': self._jump_if_false, 'num_params': 2, 'moves_cursor': True},
            7: {'function': self._less_than, 'num_params': 3, 'moves_cursor': False},
            8: {'function': self._equals, 'num_params': 3, 'moves_cursor': False},
            99: {'function': self._halt, 'num_params': 0, 'moves_cursor': False}
        }

    @staticmethod
    def _parse_instruction(instruction):
        """
        Split an instruction into the opcode identifier and
        parameter modes it represents.
        """
        instruction, opcode_identifier = divmod(instruction, 100)
        parameter_modes = []
        while instruction:
            instruction, parameter_mode = divmod(instruction, 10)
            parameter_modes.append(parameter_mode)

        return opcode_identifier, parameter_modes

    def _add(self, param1, param2, write_addr):
        val1, mode1 = param1
        val2, mode2 = param2
        write_addr, _ = write_addr  # write_addr will always be in position mode

        # dereference non-write parameters if they are in position mode
        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        self.memory[write_addr] = val1 + val2

    def _multiply(self, param1, param2, write_addr):
        val1, mode1 = param1
        val2, mode2 = param2
        write_addr, _ = write_addr  # write_addr will always be in position mode

        # dereference non-write parameters if they are in position mode
        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        self.memory[write_addr] = val1 * val2

    def _input(self, write_addr):
        write_addr, _ = write_addr  # write_addr will always be in position mode
        val = input("Input opcode expects user input: ")
        self.memory[write_addr] = int(val.strip())

    def _output(self, param):
        val, mode = param
        if mode == 0:
            val = self.memory[val]

        return val

    def _jump_if_true(self, param1, param2):
        val1, mode1 = param1
        val2, mode2 = param2

        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        if val1 != 0:
            self.cursor = val2
        else:
            self.cursor += 3

    def _jump_if_false(self, param1, param2):
        val1, mode1 = param1
        val2, mode2 = param2

        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        if val1 == 0:
            self.cursor = val2
        else:
            self.cursor += 3

    def _less_than(self, param1, param2, write_addr):
        val1, mode1 = param1
        val2, mode2 = param2
        write_addr, _ = write_addr  # write_addr will always be in position mode

        # dereference non-write parameters if they are in position mode
        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        output = 0
        if val1 < val2:
            output = 1
        self.memory[write_addr] = output

    def _equals(self, param1, param2, write_addr):
        val1, mode1 = param1
        val2, mode2 = param2
        write_addr, _ = write_addr  # write_addr will always be in position mode

        # dereference non-write parameters if they are in position mode
        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        output = 0
        if val1 == val2:
            output = 1
        self.memory[write_addr] = output

    def _halt(self):
        self.halted = True

    def step(self):
        if self.halted:
            return

        instruction = self.memory[self.cursor]
        opcode_identifier, param_modes = self._parse_instruction(instruction)
        try:
            opcode = self.opcodes[opcode_identifier]
        except KeyError:
            raise RuntimeError("Unrecognized opcode {} at address {}!".format(opcode_identifier, self.cursor))
        param_values = self.memory[(self.cursor + 1):(self.cursor + 1 + opcode['num_params'])]
        params = zip_longest(param_values, param_modes, fillvalue=0)

        output = opcode['function'](*params)
        if output is not None:
            print("Opcode {} at address {} yielded output: {}".format(opcode_identifier, self.cursor, output))

        # If the opcode takes responsibility for moving the
        # instruction pointer, don't do anything. Otherwise go
        # ahead and advance the instruction pointer here.
        if opcode['moves_cursor'] is False:
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
