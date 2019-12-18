#!/usr/bin/env python


from copy import deepcopy
from enum import Enum


def main():
    with open('18.txt', 'r') as file:
        raw_map = [line.rstrip('\n') for line in file.readlines()]
    m = parse_map(raw_map)
    print(m)


class TileType(Enum):
    PATH = 2
    WALL = 3
    KEY = 4
    DOOR = 5


class Tile:
    def __init__(self, pos, tile_type, char):
        self.pos = pos
        self.type = tile_type
        self.char = char

    def __repr__(self):
        return f'{self.char}'


class Map:
    def __init__(self, m, me, keys, doors):
        self.m = m
        self.me = me
        self.keys = keys
        self.doors = doors

    def __repr__(self):
        m_copy = deepcopy(self.m)
        m_copy[self.me[1]][self.me[0]] = '@'
        m = ''
        for y in range(len(m_copy)):
            row = ''
            for x in range(len(m_copy[0])):
                row += f'{m_copy[y][x]}'
            m += row + '\n'
        return m


def parse_map(raw_m):
    me = None
    m = []
    keys = []
    doors = []
    for y in range(len(raw_m)):
        row = []
        for x in range(len(raw_m[0])):
            pos = (x, y)
            elem = raw_m[y][x]
            if elem == '#':
                tile = Tile(pos, TileType.WALL, elem)
            elif elem == '.':
                tile = Tile(pos, TileType.PATH, elem)
            elif elem == '@':
                me = pos
                tile = Tile(pos, TileType.PATH, '.')
            elif ord('a') <= ord(elem) <= ord('z'):
                tile = Tile(pos, TileType.KEY, elem)
                keys.append(tile)
            elif ord('A') <= ord(elem) <= ord('Z'):
                tile = Tile(pos, TileType.DOOR, elem)
                doors.append(tile)
            row.append(tile)
        m.append(row)
    return Map(m, me, keys, doors)


if __name__ == '__main__':
    main()
