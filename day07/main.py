from pathlib import Path
from itertools import permutations

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")


def read_input(path: Path) -> dict:
    rv = []
    for line in open(path, 'r'):
        line = line.strip()
        target, factors = line.split(':')
        target = int(target)
        factors = [int(f) for f in factors.strip().split()]
        rv.append((target, factors))
    return rv


def multiply_or_add_or_concat(target: int, current: int, remaining: list[int], concat: bool) -> bool:
    if(len(remaining) == 1):
        if target == current * remaining[0]:
            return True
        if target == current + remaining[0]:
            return True
        if concat and target == current * 10 ** len(str(remaining[0])) + remaining[0]:
            return True
        return False

    if multiply_or_add_or_concat(target, current * remaining[0], remaining[1:], concat):
        return True
    if multiply_or_add_or_concat(target, current + remaining[0], remaining[1:], concat):
        return True
    if concat:
        # concat by multiplying current by 10^ len( <next number> ) and then adding it
        if multiply_or_add_or_concat(target, current * 10 ** len(str(remaining[0])) + remaining[0], remaining[1:], concat):
            return True
    return False

def try_fit(target: int, factors: list[int], concat: bool) -> bool:
    start = factors[0]
    return multiply_or_add_or_concat(target, start, factors[1:], concat)

def solve(path: Path, concat: bool = False) -> int:
    counter = 0
    input = read_input(path)
    for target, factors in input:
        if try_fit(target, factors, concat):
            counter += target
    
    return counter



assert(solve(VERIFICATION) == 3749)
print(solve(INPUT))
assert(solve(VERIFICATION, True) == 11387)
print(solve(INPUT, True))

