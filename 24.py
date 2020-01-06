#!/usr/bin/env python


from collections import defaultdict


def main():
    with open('24.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]

    print(f'part1: {part1(raw_map)}')
    print(f'part2: {part2(raw_map)}')

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

def get_recursive_neighbors(location):
    x, y, l = location
    neighbors = []

    size = 5
    center = size // 2

    # same level neighbors
    possibilities = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    for nx, ny in possibilities:
        if 0 <= nx < size and 0 <= ny < size:
            # exclude ?
            if nx == center and ny == center:
                continue
            neighbors.append((nx, ny, l))

    # inner neighbors (level + 1)
    # 8
    if x == 2 and y == 1:
        for nx in range(size):
            neighbors.append((nx, 0, l + 1))
    # 12
    elif x == 1 and y == 2:
        for ny in range(size):
            neighbors.append((0, ny, l + 1))
    # 14
    elif x == 3 and y == 2:
        for ny in range(size):
            neighbors.append((size - 1, ny, l + 1))
    # 18
    elif x == 2 and y == 3:
        for nx in range(size):
            neighbors.append((nx, size - 1, l + 1))

    # outer neighbors (level - 1)
    # 1, 2, 3, 4, 5
    if y == 0:
        # add 8
        neighbors.append((2, 1, l - 1))
    # 21, 22, 23, 24, 25
    elif y == size - 1:
        # add 18
        neighbors.append((2, 3, l - 1))
    # 1, 6, 11, 16, 21
    if x == 0:
        # add 12
        neighbors.append((1, 2, l - 1))
    # 5, 10, 15, 20, 25
    elif x == size - 1:
        # add 14
        neighbors.append((3, 2, l - 1))

    return neighbors

def bug_to_bug(bugs, neighbors):
    count = 0
    for neighbor in neighbors:
        if neighbor in bugs:
            count += 1
    return count == 1

def empty_to_bug(bugs, neighbors):
    count = 0
    for neighbor in neighbors:
        if neighbor in bugs:
            count += 1
    return count in [1, 2]

def run(bugs):
    new_bugs = set()
    visited = set()

    for bug in bugs:
        neighbors = get_recursive_neighbors(bug)
        if bug_to_bug(bugs, neighbors):
            new_bugs.add(bug)
        for neighbor in neighbors:
            if neighbor in visited or neighbor in bugs:
                continue
            if empty_to_bug(bugs, get_recursive_neighbors(neighbor)):
                new_bugs.add(neighbor)
            visited.add(neighbor)
    return new_bugs

def print_bugs(bugs):
    depth_points = defaultdict(list)
    for bug in bugs:
        x, y, l = bug
        depth_points[l].append((x, y))

    levels = sorted(depth_points.keys())
    for level in levels:
        print(f'Depth {level}:')
        # create an empty map
        m = [['.'] * 5 for _ in range(5)]
        # add bugs
        for x, y in depth_points[level]:
            m[y][x] = '#'
        # print map
        for row in m:
            line = ''
            for item in row:
                line += item
            print(line)
        print('')

def part2(m):
    time = 200

    # get initial set of bugs
    bugs = set()
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == '#':
                bugs.add((x, y, 0))

    # repeat for 'time' minutes
    for _ in range(time):
        bugs = run(bugs)

    return len(bugs)


if __name__ == '__main__':
    main()
