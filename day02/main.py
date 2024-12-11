from pathlib import Path
from itertools import pairwise
import os

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> list:
    inputs = []
    for line in open(path, 'r'):
        row = [int(a) for a in line.split()]
        inputs.append(row)
    return inputs

def test_report(report: list) -> bool:
    increasing = -1 # -1 unset, 0 false, 1 true
    for a,b in pairwise(report):
        if a == b:
            return False
        if abs(b - a) > 3:
            return False
        elif b > a:
            if increasing == 0:
                return False
            increasing = 1
        else:
            if increasing == 1:
                return False
            increasing = 0
    return True


def part1(path: Path) -> int:
    data = read_input(path)
    safe_counter = 0
    for report in data:
        safe_counter += int(test_report(report))

    return safe_counter

def part2(path: Path) -> int:
    data = read_input(path)
    safe_counter = 0
    for report in data:
        result = test_report(report)
        if result:
            safe_counter += 1
        else:
            for i in range(len(report)):
                sublist = report[:i] + report[i+1:]
                if(test_report(sublist)):
                    safe_counter += 1
                    break

    return safe_counter

assert(part1(VERIFICATION) == 2)
print(part1(INPUT))
assert(part2(VERIFICATION) == 4)
print(part2(INPUT))