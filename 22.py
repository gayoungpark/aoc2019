#!/usr/bin/env python


def main():
    with open('22.txt', 'r') as file:
        shuffles = [line.rstrip('\n') for line in file.readlines()]

    print(f'part1: {part1(shuffles)}')

def part1(shuffles):
    size = 10007
    deck = list(range(size))
    for shuffle in shuffles:
        technique = shuffle.split(' ')
        if len(technique) == 2:
            # cut n
            n = int(technique[-1])
            deck = deck[n:] + deck[:n]
        elif technique[2] == 'increment':
            # deal with increment n
            n = int(technique[-1])
            new_deck = [0] * size
            i = 0
            for card in deck:
                new_deck[i] = card
                i = (i + n) % size
            deck = new_deck
        else:
            # deal into new stack
            deck.reverse()

    for i in range(size):
        if deck[i] == 2019:
            return i
    return -1


if __name__ == '__main__':
    main()
