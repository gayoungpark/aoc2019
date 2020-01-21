#!/usr/bin/env python


from collections import namedtuple
from copy import deepcopy
from enum import Enum
import heapq


def main():
    with open('18.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]

    print(f'part1: {part1(raw_map)}')


def part1(raw_map):
    m, state = parse_map(raw_map)
    return m.find_all_keys(state)


class TileType(Enum):
    PATH = 2
    WALL = 3
    KEY = 4
    DOOR = 5


class Tile:
    def __init__(self, point, tile_type, char):
        self.point = point
        self.type = tile_type
        self.char = char

    def __repr__(self):
        return f'{self.char}'


Point = namedtuple('Point', ['x', 'y'])


class State:
    def __init__(self, point, keys=None):
        self.keys = keys or frozenset()
        self.point = point

    def __repr__(self):
        return f'{self.point}, {self.keys}'


class Map:
    def __init__(self, m, keys, doors):
        self.m = m
        self.keys = keys
        self.doors = doors

    def __repr__(self):
        m = ''
        for y in range(len(self.m)):
            row = ''
            for x in range(len(self.m[0])):
                row += f'{self.m[y][x]}'
            m += row + '\n'
        return m

    def find_keys(self, state):
        queue = []
        queue.append((state.point, 0))
        visited = set()

        keys = []
        while len(queue):
            point, dist = queue.pop(0)
            # check if point is at a key
            tile = self.m[point.y][point.x]
            if tile.type == TileType.KEY and tile.char not in state.keys:
                keys.append((point, dist))
            else:
                # add all unvisited neighbors
                neighbors = self.get_neighbors(point, state.keys)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, dist + 1))
            visited.add(point)
        return keys

    def get_neighbors(self, point, keys):
        possibilities = [
            (point.x + 1, point.y),
            (point.x - 1, point.y),
            (point.x, point.y + 1),
            (point.x, point.y - 1),
        ]

        neighbors = []
        for nx, ny in possibilities:
            tile = self.m[ny][nx]
            if tile.type == TileType.DOOR:
                if tile.char.lower() in keys:
                    neighbors.append(Point(nx, ny))
            elif tile.type != TileType.WALL:
                neighbors.append(Point(nx, ny))
        return neighbors

    def find_all_keys(self, initial_state):
        pq = [(0, 0, initial_state)]
        visited = set()
        i = 1   # insert order to break ties in heap

        while True:
            dist, _, state = heapq.heappop(pq)
            if (state.point, state.keys) in visited:
                continue
            # check if we found all the keys
            if len(state.keys) == len(self.keys):
                return dist
            # add all unvisited neighboring keys
            keys = self.find_keys(state)
            for npoint, ndist in keys:
                new_keys = state.keys.union(set(self.m[npoint.y][npoint.x].char))
                if (npoint, new_keys) not in visited:
                    new_dist = dist + ndist
                    heapq.heappush(pq, (new_dist, i, State(npoint, new_keys)))
                    i += 1
            visited.add((state.point, state.keys))
        return -1


def parse_map(raw_m):
    me = None
    m = []
    keys = []
    doors = []
    for y in range(len(raw_m)):
        row = []
        for x in range(len(raw_m[0])):
            point = Point(x, y)
            elem = raw_m[y][x]
            if elem == '#':
                tile = Tile(point, TileType.WALL, elem)
            elif elem == '.':
                tile = Tile(point, TileType.PATH, elem)
            elif elem == '@':
                me = point
                tile = Tile(point, TileType.PATH, '.')
            elif ord('a') <= ord(elem) <= ord('z'):
                tile = Tile(point, TileType.KEY, elem)
                keys.append(tile)
            elif ord('A') <= ord(elem) <= ord('Z'):
                tile = Tile(point, TileType.DOOR, elem)
                doors.append(tile)
            row.append(tile)
        m.append(row)
    return Map(m, keys, doors), State(me)


if __name__ == '__main__':
    main()
