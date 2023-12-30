#!/usr/bin/env python3

import fileinput
import re

fname = "2015-05.txt"

bad_names = re.compile(r"ab|cd|pq|xy")
req_1 = re.compile(r"([aeiou].*){3}")
req_2 = re.compile(r"([a-z])\1")

def is_nice(name:str) -> bool:
    if bad_names.search(name):
        return False
    has_3_vowels = req_1.search(name)
    has_double_letter = req_2.search(name)
    if has_3_vowels and has_double_letter:
        return True
    return False

naughty_examples = (
    "jchzalrnumimnmhp",
    "haegwjzuvuyypxyu",
    "dvszwmarrgswjxmb",
)

nice_examples = (
    "ugknbfddgicrmopn",
    "aaa",
)

for b in naughty_examples:
    assert not is_nice(b)
for g in nice_examples:
    assert is_nice(g)
    


def main():
    nice = 0
    for line in fileinput.input(fname):
        if is_nice(line):
            nice += 1
    print(f"found {nice} names")

if __name__ == "__main__":
    main()
