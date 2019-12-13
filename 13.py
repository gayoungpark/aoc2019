#!/usr/bin/env python

from copy import copy
from enum import Enum
from collections import Counter


class Opcode(Enum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    SET_REL = 9
    HALT = 99


class IntcodeProgram:
    def __init__(self, memory, input_vals):
        self.m = copy(memory) + [0] * 1_000_000
        # current location of instruction pointer
        self.ip = 0
        self.inputs = input_vals
        self.relative_base = 0

    def get(self, mode):
        val = None
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            val = self.m[addr]
        # immediate mode
        elif mode == 1:
            val = self.m[self.ip]
        # relative mode
        elif mode == 2:
            addr = self.relative_base + self.m[self.ip]
            val = self.m[addr]
        else:
            raise ValueError(f'received invalid parameter get mode: {mode}')
        self.ip += 1
        return val

    def set(self, mode, val):
        # position mode
        if mode == 0:
            addr = self.m[self.ip]
            self.m[addr] = val
        # relative mode
        elif mode == 2:
            addr = self.relative_base + self.m[self.ip]
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
            Opcode.SET_REL: 1,
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
            elif opcode == Opcode.SET_REL:
                self.relative_base += self.get(param_modes[0])
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
    with open('13.txt', 'r') as file:
        memory = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1(memory)}')
    print(f'part2: {part2(memory)}')

def part1(memory):
    program = IntcodeProgram(memory, [])
    outputs, _ = program.run()

    # map of location tuples (x, y) to their tile
    states = {}
    for start in range(0, len(outputs), 3):
        location = tuple(outputs[start:start+2])
        state = outputs[start+2]
        states[location] = state

    state_counts = Counter(states.values())
    return state_counts[2]

def get_joystick_move(ball, paddle):
    if ball == paddle:
        return 0
    elif ball < paddle:
        return -1
    else:
        return 1

def part2(memory):
    # update memory address 0 to play for free
    memory[0] = 2

    program = IntcodeProgram(memory, [])
    outputs, complete = program.run()

    # map of location tuples (x, y) to their tile
    states = {}
    while not complete:
        # process outputs
        while len(outputs) >= 3:
            location, tile, outputs = tuple(outputs[0:2]), outputs[2], outputs[3:]
            states[location] = tile
            if tile == 4:
                ball = location[0]
            if tile == 3:
                paddle = location[0]
        # get new input
        program.add_inputs([get_joystick_move(ball, paddle)])
        # run game again
        next_outputs, complete = program.run()
        outputs += next_outputs

    while len(outputs) >= 3:
        location, tile, outputs = tuple(outputs[0:2]), outputs[2], outputs[3:]
        states[location] = tile

    return states[(-1, 0)]


if __name__ == '__main__':
    main()
