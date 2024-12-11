from pathlib import Path

from grid import Grid

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def part1(path: Path) -> int:
    grid = Grid()
    grid.read_inputs(path)
    return grid.count_XMAS_occurances()

def part2(path: Path) -> int:
    grid = Grid()
    grid.read_inputs(path)
    return grid.count_X_MAS_occurances()

assert(part1(VERIFICATION) == 18)
print(part1(INPUT))
assert(part2(VERIFICATION) == 9)
print(part2(INPUT))
