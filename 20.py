#!/usr/bin/env python


from collections import defaultdict, namedtuple
from copy import deepcopy
from enum import Enum
from queue import Queue


def main():
    with open('20.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]

    m = parse_map(raw_map)
    print(f'part1: {part1(m)}')
    print(f'part2: {part2(m)}')

def part1(m):
    queue = Queue()
    queue.put((0, m.start))

    # set of visited position tuples (x, y)
    visited = set()

    while not queue.empty():
        dist, pos = queue.get()
        if pos == m.end:
            return dist
        neighbors = get_neighbors(m, pos[0], pos[1])
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.put((dist + 1, neighbor))
        visited.add(pos)
    return -1

def part2(m):
    Node = namedtuple('Node', ['dist', 'level', 'x', 'y'])

    queue = Queue()
    queue.put(Node(0, 0, m.start[0], m.start[1]))

    # set of visited position tuples (x, y)
    visited = set()

    while not queue.empty():
        node = queue.get()
        if node.level == 0 and node.x == m.end[0] and node.y == m.end[1]:
            return node.dist
        neighbors = get_recusive_neighbors(m, node.level, node.x, node.y)
        for nlevel, nx, ny in neighbors:
            if (nlevel, nx, ny) not in visited:
                queue.put(Node(node.dist + 1, nlevel, nx, ny))
        visited.add((node.level, node.x, node.y))
    return -1

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
        if n_tile.type != TileType.WALL:
            neighbors.append((nx, ny))
    # check portal neighbor
    if m.m[y][x].type in [TileType.INNER_PORTAL, TileType.OUTER_PORTAL]:
        neighbors.append(m.portals[(x, y)])
    return neighbors

def get_recusive_neighbors(m, level, x, y):
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
        if n_tile.type != TileType.WALL:
            neighbors.append((level, nx, ny))
    # check portal neighbor
    center_type = m.m[y][x].type
    if center_type == TileType.INNER_PORTAL:
        nx, ny = m.portals[(x, y)]
        neighbors.append((level + 1, nx, ny))
    elif center_type == TileType.OUTER_PORTAL and level != 0:
        nx, ny = m.portals[(x, y)]
        neighbors.append((level - 1, nx, ny))
    return neighbors

class TileType(Enum):
    PATH = 1
    WALL = 2
    INNER_PORTAL = 3
    OUTER_PORTAL = 4

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
        self.portals = self._update_portals(portals)

    def _get_portal_type(self, position):
        x, y = position
        # outer portals are near the border
        if x in [2, len(self.m[0]) - 3] or y in [2, len(self.m) - 3]:
            return TileType.OUTER_PORTAL
        else:
            return TileType.INNER_PORTAL

    def _update_portals(self, portals):
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
                self.m[p[1]][p[0]].type = self._get_portal_type(p)
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
