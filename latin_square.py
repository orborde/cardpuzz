#!/usr/bin/env python3

import functools
import itertools

N=5
SQUARE = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 0],
    [2, 3, 4, 0, 1],
    [3, 4, 0, 1, 2],
    [4, 0, 1, 2, 3],
]

SPACE = range(N)

def m(a,b) -> int:
    return SQUARE[a][b]

def square(size, seq):
    return [seq[i:(i+size)] for i in range(0, len(seq), size)]
    
def generate_square(size, prefix=[]):
    sq = square(size, prefix)

    if not is_latin(sq):
        return
    
    num_elements = size*size
    if len(prefix) == num_elements:
        yield sq
        return

    for i in range(size):
        yield from generate_square(size, prefix+[i])

def generate_square_verify():
    for sq in generate_square(5):
        assert is_latin(sq)
        for row in sq:
            for item in row:
                print(item, end='')
            print()
        print()

def is_latin(square):
    return (
        all(len(set(row)) == len(row) for row in square) and
        all(len(set(col)) == len(col) for col in zip(*square))
        )

def associative_counterexample(m, space):
    for a,b,c in itertools.product(space, repeat=3):
         if m(a, m(b, c)) != m(m(a,b), c):
             return (a,b,c)

def commutative_counterexample(m, space):
    for a,b in itertools.product(space, repeat=2):
        if m(a,b) != m(b,a):
            return (a,b)

assert is_latin(SQUARE)
assert associative_counterexample(m, SPACE) is None
assert commutative_counterexample(m, SPACE) is None

def solve(m,space,view,x):
    q = functools.reduce(m, view)
    for c in space:
        if m(q,c) == x:
            return c

def pl(*args, **kwargs):
    print(*args, end=' ', **kwargs)

def check():
    for gamestate in itertools.product(SPACE, repeat=N):
        pl(gamestate)

        solved=False
        for player in range(N):
            hidden = gamestate[player]
            view = gamestate[:player] + gamestate[(player+1):]
            guess = solve(m, SPACE, view, player)
            pl(f'{player}:{guess}')
            if guess == hidden:
                pl('✅')
                solved=True
            else:
                pl('❌')

        if not solved:
            pl('NOT SOLVED')

        print()

check()
