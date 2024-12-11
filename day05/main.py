from pathlib import Path
import numpy as np
from functools import cmp_to_key

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> list:
    to_checks = []
    ruleset = {}
    for line in open(path, 'r'):
        line = line.strip()
        if line.count('|'):
            before, after = line.split('|')
            before = int(before)
            after = int(after)
            if after not in ruleset:
                ruleset[after] = []
            ruleset[after].append(before)
        elif len(line):
            to_check = [int(a) for a in line.split(',')]
            to_checks.append(to_check)
    return to_checks, ruleset

def check(to_check: list, ruleset: dict, just_check_first = False) -> bool:
    for i, value in enumerate(to_check):
        if value in ruleset:
            must_come_before = ruleset[value]
            if not set(to_check[i+1:]).isdisjoint(must_come_before):
                return False
        if just_check_first:
            return True
    return True

def part1(path: Path) -> int:
    to_check, ruleset = read_input(path)
    total = 0
    for update in to_check:
        if check(update, ruleset):
            # add middle value
            total += update[len(update)//2]
    return total

# Swap the first item in input with one that must come before
def swap_first_wrong_element(input: np.array, must_come_before: list):
    for i, elem in enumerate(input):
        if elem in must_come_before:
            input[0], input[i] = input[i], input[0]
            return
    raise ValueError('Should have swapped something!')

def swapsort(input: list, ruleset: dict) -> np.array:
    # Loop over elements and swap if wrong
    # Use numpy copy of array so my array slice is a reference
    np_input = np.array(input)
    for i in range(np_input.size):
        sublist = np_input[i:]
        while not check(sublist, ruleset, just_check_first=True):
            swap_first_wrong_element(sublist, ruleset[sublist[0]])
    return np_input

def part2(path: Path) -> int:
    to_check, ruleset = read_input(path)
    total = 0
    for update in to_check:
        if not check(update, ruleset):
            np_input = swapsort(update, ruleset)
            # add middle value
            total += np_input[np_input.size//2]
    return total

# Global dict for cheating
RULESET = {}

def compare(item1, item2):
    if item1 in RULESET:
        if item2 in RULESET[item1]:
            return 1
    if item2 in RULESET:
        if item1 in RULESET[item2]:
            return -1
    return 0

def part2_with_standard_sort(path: Path) -> int:
    global RULESET
    to_check, RULESET = read_input(path)
    total = 0
    for update in to_check:
        sorted_update = sorted(update, key=cmp_to_key(compare))
        if sorted_update == update:
            continue
        total += sorted_update[len(sorted_update)//2]
    return total


assert(part1(VERIFICATION) == 143)
print(part1(INPUT))
assert(part2(VERIFICATION) == 123)
assert(part2_with_standard_sort(VERIFICATION) == 123)
print(part2(INPUT))
