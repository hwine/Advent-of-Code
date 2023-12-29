#!/usr/bin/env python3

import fileinput
from collections import Counter
from dataclasses import dataclass
from typing import Iterator, Self

@dataclass
class Location:
    x: int
    y: int

    def __add__(self, other:Self) -> Self:
        if not isinstance(other, Location):
            raise NotImplemented
        result = Location(
            self.x + other.x,
            self.y + other.y
        )
        return result
    
    def __hash__(self):
        return tuple((self.x, self.y)).__hash__()

start_location = Location(0,0)

fname = "2015-03.txt"

def _get_delta(path:str) -> Iterator[Location]:
    for c in path:
        delta = Location(0,0)
        match c:
            case '<':
                delta = Location(-1, 0)
            case '>':
                delta = Location(+1, 0)
            case '^':
                delta = Location(0, +1)
            case 'v':
                delta = Location(0, -1)
            case _:
                raise ValueError(f"unexpected direction '{c}' ({hex(ord(c))})")
        yield delta

def walk(path:str, start:Location=start_location) -> Location:
    cur_loc: Location = start
    for delta in _get_delta(path):
        cur_loc += delta
        yield cur_loc

def calc_visits(path:str) -> dict[Location,int]:
    houses = Counter()
    # visit starting house
    houses[start_location] += 1
    for location in walk(path):
        houses[location] += 1
    return houses

def calc_visits2(path:str) -> tuple[dict[Location,int], dict[Location,int]]:
    santa = Counter()
    robot = Counter()
    santa_loc = Location(0,0)
    robot_loc = Location(0,0)
    # visit starting house
    santa[santa_loc] += 1
    robot[robot_loc] += 1
    move_santa = True
    for delta in _get_delta(path):
        if move_santa:
            santa_loc += delta
            santa[santa_loc] += 1
        else:
            robot_loc += delta
            robot[robot_loc] += 1
        move_santa = not move_santa
    return santa, robot

def main():
    for line in fileinput.input(fname):
        visited = calc_visits(line)
        print(f"{len(visited)} houses visited")
        santa, robot = calc_visits2(line)
        combined = santa + robot
        print(f"{len(combined)} houses visited (santa={len(santa)}; robot={len(robot)})")
        print(f"{sum(visited.values())} presents delivered year 1")
        print(f"{combined.total()} presents delivered year 2")

if __name__ == "__main__":
    main()
