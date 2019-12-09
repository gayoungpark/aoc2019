#!/usr/bin/env python

from copy import copy
from itertools import product

class IntcodeProgram:
    def __init__(self, memory):
        self.m = copy(memory)
        # current location of instruction pointer
        self.ip = 0

    def update(self, addr, new_val):
        self.m[addr] = new_val

    def get(self, addr):
        return self.m[addr]

    def addr(self):
        if len(self.m) < self.ip + 3:
            raise IndexError('not enough parameters to complete instruction addr')
        a = self.m[self.ip + 1]
        b = self.m[self.ip + 2]
        c = self.m[self.ip + 3]

        self.m[c] = self.m[a] + self.m[b]
        self.ip += 4

    def multr(self):
        if len(self.m) < self.ip + 3:
            raise IndexError('not enough parameters to complete instruction multr')
        a = self.m[self.ip + 1]
        b = self.m[self.ip + 2]
        c = self.m[self.ip + 3]

        self.m[c] = self.m[a] * self.m[b]
        self.ip += 4

    def run(self):
        while (self.ip < len(self.m)) and (self.m[self.ip] != 99):
            opcode = self.m[self.ip]
            if opcode == 1:
                self.addr()
            elif opcode == 2:
                self.multr()
            else:
                raise ValueError(f'received invalid opcode: {opcode}')


def main():
    with open('02.txt', 'r') as file:
        memory = [int(v) for v in file.readline().split(',')]
        program = IntcodeProgram(memory)

    print(f'part1: {part1(program)}')

    print(f'part2: {part2(memory)}')


def part1(program):
    # required restorations
    program.update(1, 12)
    program.update(2, 2)

    program.run()

    return program.get(0)

def part2(memory):
    # noun, verb: [0, 99]
    for noun, verb in product(range(100), range(100)):
        program = IntcodeProgram(memory)
        program.update(1, noun)
        program.update(2, verb)

        program.run()
        output = program.get(0)

        if output == 19690720:
            return 100 * noun + verb
    return 0


if __name__ == '__main__':
    main()
