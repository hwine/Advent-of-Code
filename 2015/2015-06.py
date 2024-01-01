#!/usr/bin/env python3

import fileinput
import re
from collections import defaultdict, namedtuple

fname = "2015-06.txt"

Point = namedtuple("Point", ["x", "y"])

line_pattern = re.compile(r'^([^0-9]+) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)')

class Display:
    def __init__(self):
        self.panel = defaultdict(bool)

    def turn_on(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] = True

    def turn_off(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] = False

    def toggle(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] = not self.panel[(x,y)]
    
    def lit_count(self) -> int:
        return sum([1 for v in self.panel.values() if v])

class Display_NG:
    def __init__(self):
        self.panel = defaultdict(int)

    def turn_on(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] += 1

    def turn_off(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] -= 1
                self.panel[(x,y)] = max(0, self.panel[(x,y)])

    def toggle(self, start:Point, thru: Point) -> None:
        for x in range(start.x, thru.x+1):
            for y in range(start.y, thru.y+1):
                self.panel[(x,y)] += 2
                
    def lit_count(self) -> int:
        return sum(self.panel.values())

def main():
    if False:
        d1 = Display()
        d1.turn_on(Point(0,0),Point(2,2))
        print(f"{d1.lit_count()} lit - expected 9")
        
        d2 = Display()
        d2.turn_on(Point(0,0), Point(999,999))
        print(f"{d2.lit_count()} lit - expected 1,000,000")
        d2.turn_off(Point(0,0), Point(999,0))
        print(f"{d2.lit_count()} lit - expected 999,000")
        d2.toggle(Point(499,499), Point(500,500))
        print(f"{d2.lit_count()} lit - expected 998,996")
    elif False:
        d3 = Display_NG()
        d3.turn_on(Point(0,0), Point(0,0))
        print(f"{d3.lit_count()} brightness - expected 1")
        d4 = Display_NG()
        print(f"{d4.lit_count()} brightness at start")
        d4.toggle(Point(0,0), Point(999,999))
        print(f"{d4.lit_count()} brightness - expected 2,000,000")
    else:
        # change class for part 1 vs part 2
        display = Display_NG()
        for line in fileinput.input(fname):
            hit = line_pattern.match(line)
            if hit:
                action, *numbers = hit.groups()
                x1, y1, x2, y2 = [int(x) for x in numbers]
                match action:
                    case "turn on":
                        display.turn_on(Point(x1,y1), Point(x2, y2))
                    case "turn off":
                        display.turn_off(Point(x1,y1), Point(x2, y2))
                    case "toggle":
                        display.toggle(Point(x1,y1), Point(x2, y2))
                    case _:
                        raise ValueError("Unknown action {}", action)
        print(f"{display.lit_count()} lights on")

if __name__ == "__main__":
    main()
