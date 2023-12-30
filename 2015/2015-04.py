#!/usr/bin/env python3

from hashlib import md5
#import fileinput
#from collections import Counter

# no input file for puzzle 4 
#fname = "2015-04.txt"
seed = "yzbqklnj"

def find_num(seed:str, num_zeros:int=5) -> int:
    encoded_seed = bytes(seed, "utf-8")
    leading_zeros = '0' * num_zeros
    for i in range(1, 10_000_000):
        hash = md5(encoded_seed+bytes(str(i), 'utf-8')).hexdigest()
        if hash.startswith(leading_zeros):
            return i
        if i % 10_000 == 0:
            print(end='.')

    raise ValueError("no pattern found for {}", seed)


def main():
    # for line in fileinput.input(fname):
    # for seed, answer in (('abcdef', 609043), ('pqrstuv', 1048970)):
    #     num = find_num(seed)
    #     assert num == answer
    #     print(f"\ngot {num} for {seed}. ({answer})")

    for num_zeros in 5, 6:
        num = find_num(seed, num_zeros)
        print(f"\ngot {num} for {seed} with {num_zeros} leading zeros.")

if __name__ == "__main__":
    main()
