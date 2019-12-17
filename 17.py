#!/usr/bin/env python


from copy import copy
from enum import Enum


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
    with open('17.txt', 'r') as file:
        memory = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1(memory)}')
    print(f'part2: {part2(memory)}')

def print_grid(grid):
    for row in grid:
        print(row)

def get_neighbors(r, c):
    return [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
    ]

def get_intersections(grid):
    intersections = []
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] == '#':
                count = 0
                neighbors = get_neighbors(r, c)
                for neighbor in neighbors:
                    y, x = neighbor
                    if grid[y][x] == '#':
                        count += 1
                if count == 4:
                    intersections.append((r, c))
    return intersections

def part1(memory):
    program = IntcodeProgram(memory, [])
    outputs, complete = program.run()

    grid_str = ''
    for c in outputs:
        grid_str += chr(c)
    grid = grid_str.rstrip('\n').split('\n')

    print_grid(grid)

    intersections = get_intersections(grid)
    return sum([point[0] * point[1] for point in intersections])

def part2(memory):
    '''
    Robot path is:
        A:  R,10,R,10,R,6,R,4
        B:  R,10,R,10,L,4
        A:  R,10,R,10,R,6,R,4
        C:  R,4,L,4,L,10,L,10
        A:  R,10,R,10,R,6,R,4
        B:  R,10,R,10,L,4
        C:  R,4,L,4,L,10,L,10
        B:  R,10,R,10,L,4
        C:  R,4,L,4,L,10,L,10
        B:  R,10,R,10,L,4
    '''
    # force robot to wake up
    memory[0] = 2

    main_routine = 'A,B,A,C,A,B,C,B,C,B\n'
    fn_A = 'R,10,R,10,R,6,R,4\n'
    fn_B = 'R,10,R,10,L,4\n'
    fn_C = 'R,4,L,4,L,10,L,10\n'

    continuous_video_feed = 'n\n'

    program = IntcodeProgram(memory, [])
    for fn in [main_routine, fn_A, fn_B, fn_C, continuous_video_feed]:
        program.add_inputs([ord(c) for c in fn])
        outputs, complete = program.run()
    return outputs[-1]

if __name__ == '__main__':
    main()
