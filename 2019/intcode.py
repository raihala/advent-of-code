from collections import namedtuple
from enum import Enum, auto
from itertools import zip_longest

Opcode = namedtuple('Opcode', ['function', 'num_params', 'moves_cursor'])


class HaltException(Exception):
    pass


class WaitingForInputException(Exception):
    pass


class State(Enum):
    READY = auto()
    WAITING = auto()
    HALTED = auto()


class IntcodeComputer(object):
    def __init__(self):
        self.memory = []
        self.inputs = []
        self.cursor = 0
        self.state = State.READY

        self.opcodes = {
            1: Opcode(self._add, 3, False),
            2: Opcode(self._multiply, 3, False),
            3: Opcode(self._input, 1, False),
            4: Opcode(self._output, 1, False),
            5: Opcode(self._jump_if_true, 2, True),
            6: Opcode(self._jump_if_false, 2, True),
            7: Opcode(self._less_than, 3, False),
            8: Opcode(self._equals, 3, False),
            99: Opcode(self._halt, 0, False)
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
        if not self.inputs:
            raise WaitingForInputException()

        write_addr, _ = write_addr  # write_addr will always be in position mode
        value, self.inputs = self.inputs[0], self.inputs[1:]
        self.memory[write_addr] = value

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

        if val1 < val2:
            self.memory[write_addr] = 1
        else:
            self.memory[write_addr] = 0

    def _equals(self, param1, param2, write_addr):
        val1, mode1 = param1
        val2, mode2 = param2
        write_addr, _ = write_addr  # write_addr will always be in position mode

        # dereference non-write parameters if they are in position mode
        if mode1 == 0:
            val1 = self.memory[val1]
        if mode2 == 0:
            val2 = self.memory[val2]

        if val1 == val2:
            self.memory[write_addr] = 1
        else:
            self.memory[write_addr] = 0

    def _halt(self):
        self.state = State.HALTED

    def step(self):
        if self.state is not State.READY:
            return

        instruction = self.memory[self.cursor]
        opcode_identifier, param_modes = self._parse_instruction(instruction)
        try:
            opcode = self.opcodes[opcode_identifier]
        except KeyError:
            raise RuntimeError("Unrecognized opcode {} at address {}!".format(opcode_identifier, self.cursor))
        param_values = self.memory[(self.cursor + 1):(self.cursor + 1 + opcode.num_params)]
        params = zip_longest(param_values, param_modes, fillvalue=0)

        try:
            output = opcode.function(*params)
        except HaltException:
            self.state = State.HALTED
            return
        except WaitingForInputException:
            self.state = State.WAITING
            return

        # If the opcode takes responsibility for moving the
        # instruction pointer, don't do anything. Otherwise go
        # ahead and advance the instruction pointer here.
        if opcode.moves_cursor is False:
            self.cursor += 1 + opcode.num_params

        return output

    def kontinue(self):
        outputs = []
        while self.state is State.READY:
            output = self.step()
            if output is not None:
                outputs.append(output)
        return outputs

    def load(self, program, inputs=None):
        self.reset()
        self.memory = program.copy()
        self.inputs = inputs.copy() if inputs else []

    def reset(self):
        self.memory = []
        self.inputs = []
        self.cursor = 0
        self.state = State.READY

    def run(self, program, inputs=None):
        self.load(program, inputs)
        outputs = self.kontinue()
        return outputs

    def send_inputs(self, values):
        self.inputs.extend(values)
        if self.state is State.WAITING:
            self.state = State.READY

    @property
    def ready(self):
        return self.state is State.READY

    @property
    def waiting(self):
        return self.state is State.WAITING

    @property
    def halted(self):
        return self.state is State.HALTED
