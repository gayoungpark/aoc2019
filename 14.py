#!/usr/bin/env python

from collections import defaultdict
from math import ceil


class Chemical:
    def __init__(self, name, units):
        self.name = name
        self.units = units

    def __repr__(self):
        return f'({self.name}, {self.units})'


def main():
    with open('14.txt', 'r') as file:
        parsed = [
            parse_reaction(line.rstrip('\n'))
            for line in file.readlines()
        ]

    reactions = {
        output.name: (output, inputs)
        for inputs, output in parsed
    }

    print(f'part1: {part1(reactions)}')
    print(f'part2: {part2(reactions)}')

def part1(reactions):
    return get_min_ore_requirement(reactions, 'FUEL', 1)

def part2(reactions):
    max_ore = int(1e12)

    start = 0
    end = int(1e9)
    while (end - start) > 1:
        mid = (end + start) // 2
        ores = get_min_ore_requirement(reactions, 'FUEL', mid)
        if ores < max_ore:
            start = mid
        else:
            end = mid

    return start

def get_min_ore_requirement(reactions, goal, need):
    leftovers = {}
    return greedy_min_ore_requirement(reactions, goal, need, leftovers)

def greedy_min_ore_requirement(reactions, goal, need, leftovers):
    if goal == 'ORE':
        return need

    total = 0
    output, inputs = reactions.get(goal)

    # be greedy and try to use up leftovers as much as possible
    existing = leftovers.get(output.name)
    if existing:
        # i have more than i need
        if existing > need:
            use = need
        # use what i have
        else:
            use = existing
        # update leftovers and need
        leftovers[output.name] -= use
        need -= use

    if need > 0:
        multiple = ceil(need / output.units)

        # put away leftovers we'll create
        leftovers[goal] = multiple * output.units - need

        for chemical in inputs:
            total += greedy_min_ore_requirement(
                reactions, chemical.name, chemical.units * multiple, leftovers
            )

    return total

def parse_reaction(line):
    reaction = line.split(' => ', 1)
    inputs, outputs = reaction[0], reaction[1]

    input_chemicals = []
    for chemical in inputs.split(', '):
        c = chemical.split(' ')
        input_chemicals.append(Chemical(c[1], int(c[0])))

    output = outputs.split(' ')
    output_chemical = Chemical(output[1], int(output[0]))
    return (input_chemicals, output_chemical)


if __name__ == '__main__':
    main()
