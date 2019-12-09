from collections import namedtuple
from enum import Enum, auto

Opcode = namedtuple('Opcode', ['function', 'num_params', 'moves_cursor'])


class HaltException(Exception):
    pass


class WaitingForInputException(Exception):
    pass


class State(Enum):
    READY = auto()
    WAITING = auto()
    HALTED = auto()


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Parameter(object):
    def __init__(self, computer, value, mode=ParameterMode.POSITION):
        self._computer = computer
        self.value = value
        self.mode = mode

    @property
    def ref(self):
        """
        Return the memory address associated with this parameter, if any.
        """
        if self.mode is ParameterMode.IMMEDIATE:
            return None  # should this throw an exception?
        elif self.mode is ParameterMode.POSITION:
            return self.value
        elif self.mode is ParameterMode.RELATIVE:
            return self.value + self._computer.relative_base

    @property
    def deref(self):
        """
        Return the data associated with this parameter.
        """
        if self.mode is ParameterMode.IMMEDIATE:
            return self.value
        elif self.mode is ParameterMode.POSITION:
            return self._computer.memory[self.value]
        elif self.mode is ParameterMode.RELATIVE:
            return self._computer.memory[self.value + self._computer.relative_base]


class IntcodeComputer(object):
    def __init__(self):
        self.memory = []
        self.inputs = []
        self.cursor = 0
        self.relative_base = 0
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
            9: Opcode(self._adjust_relative_base, 1, False),
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
            instruction, mode = divmod(instruction, 10)
            parameter_modes.append(ParameterMode(mode))

        return opcode_identifier, parameter_modes

    def _add(self, val1, val2, write_addr):
        self.memory[write_addr.ref] = val1.deref + val2.deref

    def _multiply(self, val1, val2, write_addr):
        self.memory[write_addr.ref] = val1.deref * val2.deref

    def _input(self, write_addr):
        if not self.inputs:
            raise WaitingForInputException()

        value, self.inputs = self.inputs[0], self.inputs[1:]
        self.memory[write_addr.ref] = value

    def _output(self, val):
        return val.deref

    def _jump_if_true(self, val, cursor_addr):
        if val.deref != 0:
            self.cursor = cursor_addr.deref
        else:
            self.cursor += 3

    def _jump_if_false(self, val, cursor_addr):
        if val.deref == 0:
            self.cursor = cursor_addr.deref
        else:
            self.cursor += 3

    def _less_than(self, val1, val2, write_addr):
        if val1.deref < val2.deref:
            self.memory[write_addr.ref] = 1
        else:
            self.memory[write_addr.ref] = 0

    def _equals(self, val1, val2, write_addr):
        if val1.deref == val2.deref:
            self.memory[write_addr.ref] = 1
        else:
            self.memory[write_addr.ref] = 0

    def _adjust_relative_base(self, val):
        self.relative_base += val.deref

    def _halt(self):
        raise HaltException()

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
        param_modes += [ParameterMode.POSITION] * (opcode.num_params - len(param_modes))
        params = []
        for i in range(opcode.num_params):
            params.append(
                Parameter(
                    computer=self,
                    value=param_values[i],
                    mode=param_modes[i]
                )
            )

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
        self.relative_base = 0
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
