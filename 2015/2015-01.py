#!/usr/bin/env python3

import enum
import sys

def floor(s:str, verbose=True) -> int:
    up = s.count('(')
    down = s.count(')')
    assert up + down == len(s)
    final = up - down
    if verbose:
        print(f"{final} for '{s}'")

    return final

def basement(s:str) -> int:
    floor = 0
    for p, c in enumerate(s):
        inc = 1 if c=='(' else -1
        floor += inc
        if floor < 0:
            return p + 1

floor('(())')
floor('()()')
basement(')')
basement('()())')

def main():
    for s in sys.argv[1:]:
        final_floor = floor(s, False)
        step = basement(s)
        print(f"{final_floor} floor, basement at {step}")

if __name__ == "__main__":
    main()
