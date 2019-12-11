#!/usr/bin/env python

from copy import copy
from enum import Enum
from collections import defaultdict


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


def turn_robot(old_direction: tuple, turn: int):
    # up, left, bottom, right -- where (0, 0) is the top left corner
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    idx = directions.index(old_direction)

    # turn left 90 degrees (idx + 1)
    if turn == 0:
        return directions[(idx + 1) % len(directions)]
    # turn right 90 degrees (idx - 1)
    elif turn == 1:
        return directions[(idx - 1) % len(directions)]
    else:
        raise Exception(f'cannot turn robot with turn output {turn}')
    return


def main():
    with open('11.txt', 'r') as file:
        memory = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1(memory)}')


def part1(memory):
    robot_position = (0, 0)
    robot_direction = (0, -1)
    painting = defaultdict(int)

    program = IntcodeProgram(memory, [])

    while True:
        program.add_inputs([painting[robot_position]])

        output, complete = program.run()
        color, turn = output[0], output[1]

        # save color output
        painting[robot_position] = color
        # get new direction
        robot_direction = turn_robot(robot_direction, turn)
        # update robot position
        robot_position = (
            robot_position[0] + robot_direction[0],
            robot_position[1] + robot_direction[1]
        )

        if complete:
            break

    return len(painting.keys())


if __name__ == '__main__':
    main()
