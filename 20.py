#!/usr/bin/env python


from collections import defaultdict
from copy import deepcopy
from enum import Enum
from queue import Queue


def main():
    with open('20.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]

    m = parse_map(raw_map)
    print(f'part1: {part1(m)}')

def part1(m):
    queue = Queue()
    queue.put((0, m.start))

    # set of visited position tuples (x, y)
    visited = set()

    # path = {m.start: None}
    while not queue.empty():
        dist, pos = queue.get()
        if pos == m.end:
            # print path for debugging purposes
            # node = pos
            # path_str = ''
            # while node:
            #     path_str = f'{node}, {m.m[node[1]][node[0]].char} -> {path_str}'
            #     node = path[node]
            # print(path_str)
            return dist
        neighbors = get_neighbors(m, pos[0], pos[1])
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.put((dist + 1, neighbor))
                # path[neighbor] = pos
        visited.add(pos)
    return 0

def get_neighbors(m, x, y):
    possibilities = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]

    neighbors = []
    # check cardinal neighbors
    for nx, ny in possibilities:
        n_tile = m.m[ny][nx]
        if n_tile.type in [TileType.PATH, TileType.PORTAL]:
            neighbors.append((nx, ny))
    # check portal neighbor
    if m.m[y][x].type == TileType.PORTAL:
        neighbors.append(m.portals[(x, y)])
    return neighbors

class TileType(Enum):
    PATH = 1
    WALL = 2
    PORTAL = 3

class Tile:
    def __init__(self, pos, tile_type, char):
        self.pos = pos
        self.type = tile_type
        self.char = char

    def __repr__(self):
        return f'{self.char}'

class Map:
    def __init__(self, m, start, end, portals):
        self.m = m
        self.start = start
        self.end = end
        self.portals = self.update_portals(portals)

    def update_portals(self, portals):
        # create a mapping for portals
        m = {}
        for label, positions in portals.items():
            if len(positions) != 2:
                raise Exception('There can only be 2 locations for each portal type.')
            p1, p2 = positions[0], positions[1]
            m[p1] = p2
            m[p2] = p1
            for p in positions:
                # update tile type for portals
                self.m[p[1]][p[0]].type = TileType.PORTAL
        return m

    def __repr__(self):
        m = ''
        for y in range(len(self.m)):
            row = ''
            for x in range(len(self.m[0])):
                row += f'{self.m[y][x]}'
            m += row + '\n'
        return m

def check_for_portal(raw_m, x, y):
    label = raw_m[y][x]
    height = len(raw_m)
    width = len(raw_m[0])

    if y + 1 < height and ord('A') <= ord(raw_m[y + 1][x]) <= ord('Z'):
        label += raw_m[y + 1][x]
        # check above label
        if y - 1 > 0 and raw_m[y - 1][x] == '.':
            pos = (x, y - 1)
        # check below label
        elif y + 2 < height and raw_m[y + 2][x] == '.':
            pos = (x, y + 2)
        return {'label': label, 'pos': pos}
    if x + 1 < width and ord('A') <= ord(raw_m[y][x + 1]) <= ord('Z'):
        label += raw_m[y][x + 1]
        # check left of label
        if x - 1 > 0 and raw_m[y][x - 1] == '.':
            pos = (x - 1, y)
        # check right of label
        elif x + 2 < width and raw_m[y][x + 2] == '.':
            pos = (x + 2, y)
        return {'label': label, 'pos': pos}
    return None

def parse_map(raw_m):
    portals = defaultdict(list)
    m = []

    for y in range(len(raw_m)):
        row = []
        for x in range(len(raw_m[0])):
            pos = (x, y)
            elem = raw_m[y][x]
            if elem in ['#', ' ']:
                tile = Tile(pos, TileType.WALL, elem)
            elif elem == '.':
                tile = Tile(pos, TileType.PATH, elem)
            elif ord('A') <= ord(elem) <= ord('Z'):
                portal = check_for_portal(raw_m, x, y)
                if portal:
                    if portal['label'] == 'AA':
                        start = portal['pos']
                    elif portal['label'] == 'ZZ':
                        end = portal['pos']
                    else:
                        portals[portal['label']].append(portal['pos'])
                tile = Tile(pos, TileType.WALL, elem)
            row.append(tile)
        m.append(row)
    return Map(m, start, end, portals)


if __name__ == '__main__':
    main()
