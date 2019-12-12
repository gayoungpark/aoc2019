#!/usr/bin/env python

import re
from itertools import combinations

class Moon:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __repr__(self):
        return f'pos={self.pos}, vel={self.vel}'

def main():
    with open('12.txt', 'r') as file:
        coords = file.readlines()

    print(f'part1: {part1(coords, 1000)}')

def part1(coords, steps):
    moons = [
        Moon(
            [int(s) for s in re.findall(r'-?\d+', coord)],
            [0, 0, 0]
        )
        for coord in coords
    ]

    for step in range(steps):
        update_velocity(moons)
        for moon in moons:
            apply_velocity(moon)

    return sum([calc_energy(moon) for moon in moons])

def update_velocity(moons):
    for m1, m2 in list(combinations(moons, 2)):
        for i in range(3):
            pos1, pos2 = m1.pos[i], m2.pos[i]
            if pos1 > pos2:
                m1.vel[i] -= 1
                m2.vel[i] += 1
            elif pos1 < pos2:
                m1.vel[i] += 1
                m2.vel[i] -= 1
    return

def apply_velocity(moon):
    for i in range(3):
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


if __name__ == '__main__':
    main()
