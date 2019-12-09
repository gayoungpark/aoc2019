#!/usr/bin/env python

from collections import namedtuple


def main():
    with open('03.txt', 'r') as file:
        wires = [wire.rstrip('\n').split(',') for wire in file.readlines()]

    # print(f'part2: {part2()}')

    paths = []
    for wire in wires:
        paths.append(get_wire_path(wire))

    intersections = paths[0].keys() & paths[1].keys()

    closest = min(intersections, key=lambda p: abs(p.x) + abs(p.y))
    print(f'part1: {abs(closest.x) + abs(closest.y)}')

    least_steps = min(intersections, key=lambda p: paths[0][p] + paths[1][p])
    print(f'part2: {paths[0][least_steps] + paths[1][least_steps]}')

def get_wire_path(wire):
    x, y, total = 0, 0, 0

    points = {}
    Point = namedtuple('Point', ['x', 'y'])

    for step in wire:
        direction, count = parse_step(step)
        for c in range(1, count + 1):
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1
            total += 1
            points[Point(x, y)] = total

    return points

def parse_step(step):
    # parse cardinal direction
    direction = step[0]
    if direction not in ['U', 'D', 'L', 'R']:
        raise ValueError(f'invalid direction provided: {direction}')

    # parse step's count
    try:
        count = int(step[1:])
    except ValueError:
        raise ValueError(f'cannot parse number of steps in {step}')

    return direction, count

if __name__ == '__main__':
    main()
