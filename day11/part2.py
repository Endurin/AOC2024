from __future__ import annotations
from pathlib import Path
import time


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")


class MultiStone:
    number: int
    counter: int

    def __init__(self, number: int, counter: int = 1):
        self.number = int(number)
        self.counter = counter

    def __lt__(self, other: MultiStone):
        return self.number < other.number


def read_input(path: Path) -> list:
    rv = []
    for line in open(path, 'r'):
        line = line.strip().split(' ')
        for number in line: 
            rv.append(MultiStone(number))
    return rv


def get_new_stones_after_blink(stone: MultiStone) -> list:
    number = stone.number
    if number == 0:
        return [MultiStone(1, stone.counter)]

    number_str = str(number)
    length = len(number_str)
    if length % 2 == 0:
        rv = []
        rv.append(MultiStone(number_str[:int(length/2)], stone.counter))
        rv.append(MultiStone(number_str[int(length/2):], stone.counter))
        return rv

    return [MultiStone(number * 2024, stone.counter)]


def squash(input = list[MultiStone]):
    idx = 0
    while idx < len(input) - 1:
        number = input[idx].number
        while input[idx + 1].number == number and idx + 1 < len(input):
            same_stone = input.pop(idx + 1)
            input[idx].counter += same_stone.counter
        idx += 1

# Drop the order of the stones, wasn't needed
# A lot of sequences return to splitting into many 1-digit numbers
# Squash these together and keep a counter per step should be fast enough

def part2(path: Path, steps: int) -> int:
    stones = read_input(path)

    for i in range(steps):
        start = time.time()
        stones_next = []
        counter = 0
        for stone in stones:
            counter += 1
            stones_next.extend(get_new_stones_after_blink(stone))
        stones_next.sort()
        squash(stones_next)
        stones = stones_next

        print(f'Done with step {i} in {time.time() - start}, num steps: {counter}')

    counter = 0
    for stone in stones:
        counter += stone.counter
    return counter


assert(part2(VERIFICATION, steps=6) == 22)
assert(part2(VERIFICATION, steps=25) == 55312)
print(part2(INPUT, steps=75))
