from pathlib import Path
import os

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> tuple[list, list]:
    print(f'Reading path: {path}')

    input1 = []
    input2 = []
    for line in open(path, 'r'):
        i1, i2 = line.split()
        input1.append(int(i1))
        input2.append(int(i2))
    return input1, input2


def part1(path: Path) -> int:
    input1, input2 = read_input(path)
    input1.sort()
    input2.sort()
    return sum(abs(a-b) for a,b in zip(input1, input2))

def part2(path: Path) -> int:
    input1, input2 = read_input(path)
    input2counts = {}
    for number in input2:
        if number not in input2counts:
            input2counts[number] = 0
        input2counts[number] += 1
    result = sum((input2counts[a] * a) if a in input2counts else 0 for a in input1)
    return result

assert(part1(VERIFICATION) == 11)
print(part1(INPUT))
assert(part2(VERIFICATION) == 31)
print(part2(INPUT))