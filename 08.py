#!/usr/bin/env python

from collections import Counter


WIDTH, HEIGHT = 25, 6

def main():
    with open('08.txt', 'r') as file:
        pixels = file.readline().strip()

    layers = get_layers(pixels)

    print(f'part1: {part1(layers)}')

    print(f'part2:')
    part2(layers)

def get_layers(pixels):
    layer_size = WIDTH * HEIGHT
    return [
        pixels[i:i+layer_size]
        for i in range(0, len(pixels), layer_size)
    ]

def part1(layers):
    fewest_zeros = {}
    for layer in layers:
        counter = Counter(layer)
        if counter['0'] < fewest_zeros.get('0', WIDTH * HEIGHT):
            fewest_zeros = counter

    return fewest_zeros['1'] * fewest_zeros['2']

def part2(layers):
    output = []
    for idx in range(WIDTH * HEIGHT):
        output.append(_get_pixel([l[idx] for l in layers]))

    for r in range(HEIGHT):
        row = ''
        for idx in range(r * WIDTH, (r + 1) * WIDTH):
            row += output[idx]
        print(row)

def _get_pixel(pixels):
    for p in pixels:
        if p == '0':
            return '██'
        if p == '1':
            return '  '
    return '22'

if __name__ == '__main__':
    main()
