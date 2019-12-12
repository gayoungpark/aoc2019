#!/usr/bin/env python

import re
from copy import deepcopy
from functools import reduce
from itertools import combinations
from math import gcd


class Moon:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __repr__(self):
        return f'pos={self.pos}, vel={self.vel}'

def main():
    with open('12.txt', 'r') as file:
        coords = [
            [int(s) for s in re.findall(r'-?\d+', coord)]
            for coord in file.readlines()
        ]

    print(f'part1: {part1(deepcopy(coords), 1000)}')
    print(f'part2: {part2(deepcopy(coords))}')

def part1(coords, steps):
    moons = [
        Moon(coord, [0, 0, 0])
        for coord in coords
    ]

    for step in range(steps):
        update_velocity(moons)
        for moon in moons:
            apply_velocity(moon)

    return sum([calc_energy(moon) for moon in moons])

def part2(coords):
    repeats = []

    for axis in range(len(coords[0])):
        moons = [
            Moon([coord[axis]], [0])
            for coord in coords
        ]

        state_to_steps = {}
        steps = 0
        while True:
            state = tuple([m.pos[0] for m in moons] + [m.vel[0] for m in moons])
            if state in state_to_steps:
                break
            state_to_steps[state] = steps

            update_velocity(moons)
            for moon in moons:
                apply_velocity(moon)
            steps += 1

        repeats.append(steps)

    return lcm(repeats)

def update_velocity(moons):
    for m1, m2 in list(combinations(moons, 2)):
        for i in range(len(m1.pos)):
            pos1, pos2 = m1.pos[i], m2.pos[i]
            if pos1 > pos2:
                m1.vel[i] -= 1
                m2.vel[i] += 1
            elif pos1 < pos2:
                m1.vel[i] += 1
                m2.vel[i] -= 1
    return

def apply_velocity(moon):
    for i in range(len(moon.pos)):
        moon.pos[i] += moon.vel[i]
    return

def calc_pot(moon):
    # the sum of the absolute values of its x, y, and z position coordinates
    return sum([abs(p) for p in moon.pos])

def calc_kin(moon):
    # the sum of the absolute values of its velocity coordinates
    return sum([abs(p) for p in moon.vel])

def calc_energy(moon):
    return calc_pot(moon) * calc_kin(moon)

def lcm(nums):
    return reduce(lambda x, y: x * y // gcd(x, y), nums)

if __name__ == '__main__':
    main()
