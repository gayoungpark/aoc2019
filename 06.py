#!/usr/bin/env python

def main():
    with open('06.txt', 'r') as file:
        orbits = file.read().splitlines()

    tree = {}
    for orbit in orbits:
        parent, child = parse_orbit(orbit)
        tree[child] = parent

    print(f'part1: {part1(tree)}')
    print(f'part2: {part2(tree)}')

def part1(tree):
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

def part2(tree):
    san_ancestors = {}
    dist = 1
    key = 'SAN'
    while tree.get(key):
        parent = tree.get(key)
        san_ancestors[parent] = dist
        dist += 1
        key = parent

    you_ancestors = []
    key = 'YOU'
    while tree.get(key):
        parent = tree.get(key)
        if parent in san_ancestors.keys():
            intersect_key = parent
            break
        you_ancestors.append(parent)
        key = parent

    return len(you_ancestors) + san_ancestors[intersect_key] - 1

if __name__ == '__main__':
    main()
