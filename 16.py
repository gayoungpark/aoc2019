#!/usr/bin/env python

from copy import copy


def main():
    with open('16.txt', 'r') as file:
        raw_nums = file.readline()
        nums = [int(n) for n in raw_nums.rstrip('\n')]

    print(f'part1: {part1(nums)}')
    print(f'part2: {part2(nums)}')

def part1(nums):
    for i in range(100):
        nums = run_phase(nums)
    return convert_arr_to_str(nums[:8])

def convert_arr_to_str(arr):
    output = ''
    for i in range(len(arr)):
        output += str(arr[i])
    return output

def part2(nums):
    # calculate offset (first seven digits of my initial input)
    offset = int(convert_arr_to_str(nums[:7]))
    nums = nums * 10_000
    nums = nums[offset:]

    for i in range(100):
        prev = nums
        nums = run_phase_fast(prev)
    return convert_arr_to_str(nums[:8])

def get_pattern(multiple, n):
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for p in base_pattern:
        for _ in range(multiple):
            pattern.append(p)
    while len(pattern) < (n + 1):
        pattern += pattern
    return pattern[1:n+1]

def run_phase(nums):
    n = len(nums)
    new_nums = []

    for multiple in range(1, n + 1):
        pattern = get_pattern(multiple, n)

        digit = 0
        for i in range(n):
            val = nums[i] * pattern[i]
            digit += val

        new_nums.append(abs(digit) % 10)

    return new_nums

def run_phase_fast(prev):
    nxt = [0] * len(prev)
    nxt[-1] = prev[-1]
    for i in range(len(prev) - 2, -1, -1):
        nxt[i] = (nxt[i+1] + prev[i]) % 10
    return nxt

if __name__ == '__main__':
    main()
