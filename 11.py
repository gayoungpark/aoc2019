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


def paint(position, direction, painting, program):
    while True:
        program.add_inputs([painting[position]])

        output, complete = program.run()
        color, turn = output[0], output[1]

        # save color output
        painting[position] = color
        # get new direction
        direction = turn_robot(direction, turn)
        # move robot
        position = (
            position[0] + direction[0],
            position[1] + direction[1]
        )

        if complete:
            break

    return painting

def turn_robot(old_direction: tuple, turn: int):
    # up, left, bottom, right
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
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

def print_painting(painting):
    points = painting.keys()

    min_x = min([point[0] for point in points])
    max_x = max([point[0] for point in points])

    min_y = min([point[1] for point in points])
    max_y = max([point[1] for point in points])

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print('██' if painting[(x, y)] else '  ', end = '')
        print()


def main():
    with open('11.txt', 'r') as file:
        memory = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1(memory)}')
    print(f'part2:')
    part2(memory)

def part1(memory):
    robot_position = (0, 0)
    robot_direction = (0, 1)
    painting = defaultdict(int)

    program = IntcodeProgram(memory, [])

    painting = paint(robot_position, robot_direction, painting, program)

    return len(painting.keys())

def part2(memory):
    robot_position = (0, 0)
    robot_direction = (0, 1)
    painting = defaultdict(int)

    program = IntcodeProgram(memory, [])

    # start on a white panel
    painting[robot_position] = 1
    painting = paint(robot_position, robot_direction, painting, program)

    print_painting(painting)


if __name__ == '__main__':
    main()
