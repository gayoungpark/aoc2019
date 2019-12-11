#!/usr/bin/env python

from copy import copy
from enum import Enum
from itertools import permutations


class Opcode(Enum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

class IntcodeProgram:
    def __init__(self, memory, input_vals):
        self.m = copy(memory)
        # current location of instruction pointer
        self.ip = 0
        self.inputs = input_vals

    def get(self, mode):
        val = None
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            val = self.m[addr]
        # immediate mode
        elif mode == 1:
            val = self.m[self.ip]
        else:
            raise ValueError(f'received invalid parameter get mode: {mode}')
        self.ip += 1
        return val

    def set(self, mode, val):
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            self.m[addr] = val
        else:
            raise ValueError(f'received invalid parameter set mode: {mode}')
        self.ip += 1

    def add_inputs(self, new_inputs):
        self.inputs += new_inputs

    def run(self):
        complete = False
        outputs = []

        param_lens = {
            Opcode.ADD: 3,
            Opcode.MULT: 3,
            Opcode.INPUT: 1,
            Opcode.OUTPUT: 1,
            Opcode.JUMP_IF_TRUE: 2,
            Opcode.JUMP_IF_FALSE: 2,
            Opcode.LESS_THAN: 3,
            Opcode.EQUALS: 3,
            Opcode.HALT: 0,
        }

        while self.ip < len(self.m):
            instruction = self.m[self.ip]
            opcode = Opcode(instruction % 100)
            param_modes = self._get_modes(instruction // 100, param_lens[opcode])

            self.ip += 1

            if opcode == Opcode.ADD:
                self.set(
                    param_modes[2],
                    self.get(param_modes[0]) + self.get(param_modes[1])
                )
            elif opcode == Opcode.MULT:
                self.set(
                    param_modes[2],
                    self.get(param_modes[0]) * self.get(param_modes[1])
                )
            elif opcode == Opcode.INPUT:
                if len(self.inputs) == 0:
                    self.ip -= 1
                    break
                input_val = self.inputs.pop(0)
                self.set(
                    param_modes[0],
                    input_val
                )
            elif opcode == Opcode.OUTPUT:
                outputs.append(self.get(param_modes[0]))
            elif opcode == Opcode.JUMP_IF_TRUE:
                condition = self.get(param_modes[0])
                dest = self.get(param_modes[1])
                if condition:
                    self.ip = dest
            elif opcode == Opcode.JUMP_IF_FALSE:
                condition = self.get(param_modes[0])
                dest = self.get(param_modes[1])
                if not condition:
                    self.ip = dest
            elif opcode == Opcode.LESS_THAN:
                self.set(
                    param_modes[2],
                    int(self.get(param_modes[0]) < self.get(param_modes[1]))
                )
            elif opcode == Opcode.EQUALS:
                self.set(
                    param_modes[2],
                    int(self.get(param_modes[0]) == self.get(param_modes[1]))
                )
            elif opcode == Opcode.HALT:
                complete = True
                break
            else:
                raise ValueError(f'received invalid opcode: {opcode}')

        return outputs, complete

    def _get_modes(self, mode_digits, num):
        modes = []
        for _ in range(num):
            mode = mode_digits % 10
            mode_digits //= 10
            modes.append(mode)
        return modes

def main():
    with open('07.txt', 'r') as file:
        memory = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1(memory)}')
    print(f'part2: {part2(memory)}')

def part1(memory):
    max_signal = 0
    for phase_settings in permutations(range(5)):
        outputs = [0]
        for phase_setting in phase_settings:
            amp = IntcodeProgram(memory, [phase_setting] + outputs)
            outputs, _ = amp.run()
        max_signal = max(max_signal, outputs[-1])
    return max_signal

def part2(memory):
    max_signal = 0
    for phase_settings in permutations(range(5, 10)):

        machines = []
        # set up machines with each phase setting
        for phase_setting in phase_settings:
            machine = IntcodeProgram(memory, [phase_setting])
            outputs, complete = machine.run()
            if len(outputs) != 0:
                raise Exception('output should be zero')
            if complete:
                raise Exception('machine should not be done executing program')
            machines.append(machine)

        idx = 0
        outputs = [0]
        while True:
            machine = machines[idx]
            machine.add_inputs(outputs)
            outputs, complete = machine.run()
            if complete:
                del machines[idx]
                if len(machines) == 0:
                    break
                idx = idx % len(machines)
            else:
                idx = (idx + 1) % len(machines)

        max_signal = max(max_signal, outputs[-1])

    return max_signal

if __name__ == '__main__':
    main()
