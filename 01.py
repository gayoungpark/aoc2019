#!/usr/bin/env python

import math


def main():
    with open('01.txt', 'r') as file:
        module_fuel = part1(file)
        print(f'part 1: {module_fuel}')

    with open('01.txt', 'r') as file:
        total_fuel = part2(file)
        print(f'part 2: {total_fuel}')

def part1(file):
    total = 0
    for line in file:
        total += _measure_fuel(int(line))
    return total

def part2(file):
    total = 0
    for line in file:
        module_fuel = _measure_fuel(int(line))
        total += _measure_total_fuel(module_fuel, module_fuel)
    return total

def _measure_total_fuel(fuel, remaining):
    additional_fuel = _measure_fuel(remaining)
    if additional_fuel <= 0:
        return fuel
    else:
        return _measure_total_fuel(fuel + additional_fuel, additional_fuel)

def _measure_fuel(mass):
    return math.floor(mass / 3) - 2

def test_part1():
    for mass, expected in [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583)
    ]:
        print(_measure_fuel(mass) == expected)

def test_part2():
    for mass, expected in [
        (14, 2),
        (1969, 966),
        (100756, 50346)
    ]:
        module_fuel = _measure_fuel(mass)
        print(_measure_total_fuel(module_fuel, module_fuel) == expected)

if __name__ == '__main__':
    main()
