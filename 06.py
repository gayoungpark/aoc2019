#!/usr/bin/env python

def main():
    with open('06.txt', 'r') as file:
        orbits = file.read().splitlines()

    print(f'part1: {part1(orbits)}')

def part1(orbits):
    tree = {}
    for orbit in orbits:
        parent, child = parse_orbit(orbit)
        tree[child] = parent

    total = 0
    for node in tree.keys():
        total += count_orbits(tree, node)

    return total

def parse_orbit(orbit):
    return tuple(orbit.split(')', 1))

def count_orbits(tree, child):
    parent = tree.get(child)
    if not parent:
        return 0
    return 1 + count_orbits(tree, parent)

if __name__ == '__main__':
    main()
