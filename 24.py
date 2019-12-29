#!/usr/bin/env python


def main():
    with open('24.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]

    print(f'part1: {part1(raw_map)}')

def get_neighbors(m, x, y):
    possibilities = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    neighbors = []
    for nx, ny in possibilities:
        if 0 <= nx < len(m[0]) and 0 <= ny < len(m):
            neighbors.append((nx, ny))
    return neighbors

def get_new_bug_state(m, neighbors):
    count = 0
    for nx, ny in neighbors:
        if m[ny][nx] == '#':
            count += 1
    return '#' if count == 1 else '.'

def get_new_empty_state(m, neighbors):
    count = 0
    for nx, ny in neighbors:
        if m[ny][nx] == '#':
            count += 1
    return '#' if count in [1, 2] else '.'

def print_map(m):
    for row in m:
        print(row)
    print('')

def calc_score(m):
    points = 0
    for y in range(len(m)):
        for x in range(len(m[0])):
            multiple = len(m)
            power = y * multiple + x
            if m[y][x] == '#':
                points += 2 ** power
    return points

def get_new_map(m):
    new_map = []
    for y in range(len(m)):
        new_row = ''
        for x in range(len(m[0])):
            tile = m[y][x]
            if tile == '#':
                new_row += get_new_bug_state(m, get_neighbors(m, x, y))
            elif tile == '.':
                new_row += get_new_empty_state(m, get_neighbors(m, x, y))
            else:
                raise Exception(f'Map has unknown tile type -- tile: {tile}, x: {x}, y: {y}')
        new_map.append(new_row)
    return new_map

def part1(m):
    scores = set()

    while True:
        new_map = get_new_map(m)
        score = calc_score(new_map)
        if score in scores:
            return score
        else:
            scores.add(score)
        m = new_map
    return -1


if __name__ == '__main__':
    main()
