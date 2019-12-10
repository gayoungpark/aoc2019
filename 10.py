#!/usr/bin/env python

import math
from collections import defaultdict


def main():
    with open('10.txt', 'r') as file:
        asteroid_map = file.read().splitlines()
    asteroids = get_asteroids(asteroid_map)

    print(f'part1: {part1(asteroids)}')
    print(f'part2: {part2(asteroids, (31, 20), 200)}')

def get_asteroids(asteroid_map: set):
    asteroids = set()
    for r in range(len(asteroid_map)):
        for c in range(len(asteroid_map[0])):
            point = asteroid_map[r][c]
            if point == '#':
                asteroids.add((c, r))
    return asteroids

def detectable_asteroids(asteroid: tuple, asteroids: set):
    others = asteroids.copy()
    if asteroid in others:
        others.remove(asteroid)

    vectors = set()
    for o in others:
        vectors.add(calc_vector(asteroid, o))
    return len(vectors)

def calc_vector(a1: tuple, a2: tuple):
    numerator = a2[1] - a1[1]
    denominator = (a2[0] - a1[0])
    if not numerator:
        return (0, -1 if denominator < 0 else 1)
    if not denominator:
        return (-1 if numerator < 0 else 1, 0)
    gcd = math.gcd(numerator, denominator)
    return (numerator // gcd, denominator // gcd)

def part1(asteroids):
    max_detections = 0
    best = None
    for a in asteroids:
        detections = detectable_asteroids(a, asteroids)
        if detections > max_detections:
            max_detections = detections
            best = a
    print(best)
    return max_detections

def calc_degree(delta_x, delta_y):
    """North is 0 degrees and we rotate clockwise"""
    radian = math.atan2(delta_y, delta_x)
    degree = radian * (180 / math.pi)
    # to adjust for y axis being flipped and north being 0 degrees
    degree += 90
    if degree < 0:
        degree += 360
    return degree

def calc_length(delta_x, delta_y):
    return math.sqrt(delta_x ** 2 + delta_y ** 2)

def part2(asteroids, laser, goal):
    to_destroy = asteroids.copy()
    to_destroy.remove(laser)

    degrees_to_relativepts = defaultdict(list)
    for asteroid in to_destroy:
        relative_point = (asteroid[0] - laser[0], asteroid[1] - laser[1])
        degree = calc_degree(*relative_point)
        degrees_to_relativepts[degree].append(relative_point)

    for degree, points in degrees_to_relativepts.items():
        points.sort(key=lambda point: calc_length(*point))

    ordered_degrees = sorted(degrees_to_relativepts.items(), key=lambda tup: tup[0])

    idx = 0
    vaporized = 0
    num_degrees = len(ordered_degrees)
    while True:
        deg, points = ordered_degrees[idx]
        if len(points):
            target, points = points[0], points[1:]
            vaporized += 1
            if vaporized == goal:
                absolutept = (target[0] + laser[0], target[1] + laser[1])
                return (absolutept[0] * 100 + absolutept[1])
        idx = (idx + 1) % num_degrees
    return 0


if __name__ == '__main__':
    main()
