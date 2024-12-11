from __future__ import annotations
from pathlib import Path
import time


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

# linked-list approach to maintain order
class Stone:
    number: int
    next: Stone

    def __init__(self, number: int, next: Stone = None):
        self.next = next
        self.set_number(number)

    def set_number(self, number):
        self.number = int(number)

    def __repr__(self):
        return f'{self.number}'

    # return the next stone to be processed
    def step(self) -> Stone:
        if self.number == 0:
            self.number = 1
            return self.next

        number_str = str(self.number)
        length = len(number_str)
        if length % 2 == 0:
            self.set_number(number_str[:int(length/2)])
            new_stone = Stone(number_str[int(length/2):], self.next)
            self.next = new_stone
            return new_stone.next
        
        self.number *= 2024
        return self.next

def read_input(path: Path) -> Stone:
    front_stone = None
    previous_stone = None
    for line in open(path, 'r'):
        line = line.strip().split(' ')
        for number in line: 
            stone = Stone(int(number))
            if previous_stone is not None:
                previous_stone.next = stone
            if front_stone is None:
                front_stone = stone
            previous_stone = stone

    return front_stone


def part1(path: Path, steps: int) -> int:
    front_stone = read_input(path)

    for i in range(steps):
        start = time.time()
        stone = front_stone
        counter = 0
        while stone is not None:
            counter += 1
            stone = stone.step()
        print(f'Done with step {i} in {time.time() - start}, num steps: {counter}')


    stone = front_stone
    counter = 0
    while stone is not None:
        counter += 1
        stone = stone.next
    return counter


assert(part1(VERIFICATION, steps=6) == 22)
assert(part1(VERIFICATION, steps=25) == 55312)
print(part1(INPUT, steps=25))
