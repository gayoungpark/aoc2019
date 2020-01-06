#!/usr/bin/env python


def main():
    with open('22.txt', 'r') as file:
        shuffles = [line.rstrip('\n') for line in file.readlines()]

    print(f'part1: {part1(shuffles)}')
    print(f'part2: {part2(shuffles)}')

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

def part2(shuffles):
    size = 119315717514047

    start, jump = 0, 1
    for shuffle in shuffles:
        technique = shuffle.split(' ')
        if len(technique) == 2:
            # cut n
            n = int(technique[-1])
            start = (start + jump * n) % size
        elif technique[2] == 'increment':
            # deal with increment n
            n = int(technique[-1])
            mod_inv = modinv(n, size)
            jump = (jump * mod_inv) % size
        else:
            # deal into new stack
            jump = (jump * (size - 1)) % size
            start = (start + jump) % size
    start, jump = repeat(start, jump, 101741582076661, size)

    return (start + 2020 * jump) % size

def repeat(s, m, k, p):
    m_k = pow(m, k, p)
    s_k = (s * ((1 - m_k) % p) * modinv((1 - m) % p, p)) % p
    return s_k, m_k


# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


if __name__ == '__main__':
    main()
