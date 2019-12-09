#!/usr/bin/env python

from collections import Counter


def main():
    start = 231832
    end = 767346
    print(f'part1: {part1(start, end)}')
    print(f'part2: {part2(start, end)}')

def part1(start, end):
    count = 0
    for n in range(start, end + 1):
        # It is a six-digit number
        if len(str(n)) != 6:
            continue
        # Two adjacent digits are the same (like 22 in 122345)
        if not has_duplicate(n):
            continue
        # Going from left to right, the digits never decrease
        if digits_decrease(n):
            continue
        count += 1
    return count

def part2(start, end):
    count = 0
    for n in range(start, end + 1):
        # It is a six-digit number
        if len(str(n)) != 6:
            continue
        # Two adjacent digits are the same and not part of n (like 22 in 122345)
        if not has_length_two_duplicate(n):
            continue
        # Going from left to right, the digits never decrease
        if digits_decrease(n):
            continue
        count += 1
    return count

def has_duplicate(n):
    prev = ''
    for digit in str(n):
        if digit == prev:
            return True
        prev = digit
    return False

def has_length_two_duplicate(n):
    """The two adjacent matching digits are not part of a larger group of matching digits.

    Examples:
        112233 meets these criteria because the digits never decrease and
               all repeated digits are exactly two digits long.
        123444 no longer meets the criteria (the repeated 44 is part of a
               larger group of 444).
        111122 meets the criteria (even though 1 is repeated more than twice,
               it still contains a double 22).
    """
    counter = Counter(str(n))
    for n, count in counter.items():
        if count == 2:
            return True
    return False

def digits_decrease(n):
    prev = -1
    for digit in str(n):
        digit = int(digit)
        if digit < prev:
            return True
        prev = digit
    return False

if __name__ == '__main__':
    main()
