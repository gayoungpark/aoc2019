#!/usr/bin/env python

from copy import copy
from enum import Enum
from itertools import product


class Opcode(Enum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    HALT = 99

class IntcodeProgram:
    def __init__(self, memory, input_vals):
        self.m = copy(memory)
        # current location of instruction pointer
        self.ip = 0
        self.inputs = input_vals
        self.outputs = []

    def get(self, mode):
        val = None
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            val = self.m[addr]
        # immediate mode
        elif mode == 1:
            val = self.m[self.ip]
        self.ip += 1
        return val

    def set(self, mode, val):
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            self.m[addr] = val
        # immediate mode
        elif mode == 1:
            self.m[self.ip] = val
        self.ip += 1

    def run(self):
        param_lens = {
            Opcode.ADD: 3,
            Opcode.MULT: 3,
            Opcode.INPUT: 1,
            Opcode.OUTPUT: 1,
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
                    raise IndexError('input is empty')
                input_val = self.inputs.pop(0)
                self.set(
                    param_modes[0],
                    input_val
                )
            elif opcode == Opcode.OUTPUT:
                self.outputs.append(self.get(param_modes[0]))
            elif opcode == Opcode.HALT:
                break
            else:
                raise ValueError(f'received invalid opcode: {opcode}')
        return self.outputs

    def _get_modes(self, mode_digits, num):
        modes = []
        for _ in range(num):
            mode = mode_digits % 10
            mode_digits //= 10
            modes.append(mode)
        return modes

def main():
    with open('05.txt', 'r') as file:
        memory = [int(v) for v in file.readline().split(',')]
        inputs = [1]
        program = IntcodeProgram(memory, inputs)

    print(f'part1: {part1(program)}')


def part1(program):
    outputs = program.run()
    print(outputs)

    return outputs[-1]



if __name__ == '__main__':
    main()
