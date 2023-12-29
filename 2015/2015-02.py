#!/usr/bin/env python3

import fileinput
from functools import reduce
import sys

def calc_area(dimensions:str) -> int:
    l, w, h = [int(x) for x in dimensions.split('x')]
    sides = (l*w, w*h, h*l)
    surface = 2 * sum(sides)
    extra = min(sides)
    return surface + extra

def calc_ribbon_needed(dimensions:str, verbose=False) -> int:
    sides = [int(x) for x in dimensions.split('x')]
    sides.sort()
    # since sides is sorted, we want the first 2
    perimeter = 2 * sum(sides[:2])
    volume = reduce(lambda x,y: x*y, sides, 1)
    if verbose:
        print(f"{dimensions.strip()}, {sides}, {volume}, {perimeter}")
        print(f"{perimeter+volume}, {2*(sides[0]+sides[1])}, {sides[0]*sides[1]*sides[2]}")
    return perimeter+volume

for d in ("4x2x3", "10x1x1"):
    print(f"{calc_ribbon_needed(d, True)} for {d}")

def main():
    sq_ft_total = 0
    ribbon_length_total = 0
    for line in fileinput.input():
        area = calc_area(line)
        sq_ft_total += area
        ribbon_length_total += calc_ribbon_needed(line)
    print(f"{sq_ft_total} sq ft wrapping paper needed")
    print(f"{ribbon_length_total} feet of ribbon needed")

if __name__ == "__main__":
    main()
