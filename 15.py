#!/usr/bin/env python

from copy import copy
from enum import Enum
from queue import Queue


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
    global MEMORY
    with open('15.txt', 'r') as file:
        MEMORY = [int(v) for v in file.readline().strip().split(',')]

    print(f'part1: {part1()}')
    print(f'part2: {part2()}')

class Movement(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Tile(Enum):
    ROBOT = 1
    WALL = 2
    ROAD = 3
    OXYGEN = 4

def print_area(area,):
    points = area.keys()

    min_x = min([point[0] for point in points])
    max_x = max([point[0] for point in points])

    min_y = min([point[1] for point in points])
    max_y = max([point[1] for point in points])

    for y in range(max_y, min_y - 1, -1):
        line = f'{y:3} '
        for x in range(min_x, max_x + 1):
            tile = area.get((x, y))
            if tile == Tile.WALL:
                line += '#'
            elif tile == Tile.ROAD:
                line += '.'
            elif tile == Tile.OXYGEN:
                line += 'O'
            else:
                line += ' '
        print(line)

def get_neighbors(area, pos):
    x, y = pos
    possibilities = [
        ((x + 1, y), Movement.EAST),
        ((x - 1, y), Movement.WEST),
        ((x, y + 1), Movement.NORTH),
        ((x, y - 1), Movement.SOUTH),
    ]

    neighbors = []
    for position, direction in possibilities:
        if position not in area:
            neighbors.append((position, direction))
    return neighbors

def explore_path(path, direction):
    program = IntcodeProgram(MEMORY, path + [direction.value])

    outputs, complete = program.run()
    if complete:
        raise Exception('program completd')
    return outputs[-1]

def part1():
    found = False

    # map of position tuples (x, y) to their tile
    area = {}
    area[(0, 0)] = Tile.ROAD

    # queue of tuples (path, position tuple)
    explore = Queue()
    explore.put(([], (0, 0)))

    # set of visited position tuples (x, y)
    visited = set()

    while not found:
        path, pos = explore.get()

        neighbors = get_neighbors(area, pos)
        for neighbor, direction in neighbors:
            # try that direction
            status = explore_path(path, direction)
            if status == 0:
                area[neighbor] = Tile.WALL
            elif status == 1:
                area[neighbor] = Tile.ROAD
                if neighbor not in visited:
                    new_path = copy(path) + [direction.value]
                    explore.put((new_path, neighbor))
            elif status == 2:
                area[neighbor] = Tile.OXYGEN
                found = True
                break

        # update visited
        visited.add(pos)

    return len(path) + 1

def get_neighbors2(area, pos):
    x, y = pos
    possibilities = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]

    neighbors = []
    for position in possibilities:
        if area.get(position) == Tile.ROAD:
            neighbors.append(position)
    return neighbors


def find_longest_distance(area, start):
    max_dist = 0

    explore = Queue()
    explore.put((0, start))

    visited = set()
    while not explore.empty():
        dist, pos = explore.get()
        if dist > max_dist:
            max_dist = dist
        neighbors = get_neighbors2(area, pos)
        for neighbor in neighbors:
            if neighbor not in visited:
                explore.put((dist + 1, neighbor))
        visited.add(pos)

    return max_dist


def part2():
    # map of position tuples (x, y) to their tile
    area = {}
    area[(0, 0)] = Tile.ROAD

    # queue of tuples (path, position tuple)
    explore = Queue()
    explore.put(([], (0, 0)))

    # set of visited position tuples (x, y)
    visited = set()

    while not explore.empty():
        path, pos = explore.get()

        neighbors = get_neighbors(area, pos)
        for neighbor, direction in neighbors:
            # try that direction
            status = explore_path(path, direction)
            if status == 0:
                area[neighbor] = Tile.WALL
            elif status == 1:
                area[neighbor] = Tile.ROAD
                if neighbor not in visited:
                    new_path = copy(path) + [direction.value]
                    explore.put((new_path, neighbor))
            elif status == 2:
                area[neighbor] = Tile.OXYGEN
                oxygen = neighbor
                if neighbor not in visited:
                    new_path = copy(path) + [direction.value]
                    explore.put((new_path, neighbor))

        # update visited
        visited.add(pos)

    return find_longest_distance(area, oxygen)


if __name__ == '__main__':
    main()
