from pathlib import Path
from grid import Grid

filedir = Path(__file__).parent.resolve()
VERIFICATION1 = filedir.joinpath("inputs/verification1.txt")
VERIFICATION2 = filedir.joinpath("inputs/verification2.txt")
VERIFICATION3 = filedir.joinpath("inputs/verification3.txt")
VERIFICATION4 = filedir.joinpath("inputs/verification4.txt")
VERIFICATION5 = filedir.joinpath("inputs/verification5.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def solve(path: Path, part1 = True) -> int:
    grid = Grid(path)
    price = grid.compute_price(part1)
    return price


assert(solve(VERIFICATION1) == 140)
assert(solve(VERIFICATION2) == 772)
assert(solve(VERIFICATION3) == 1930)
print(solve(INPUT))
assert(solve(VERIFICATION1, False) == 80)
assert(solve(VERIFICATION2, False) == 436)
assert(solve(VERIFICATION4, False) == 236)
assert(solve(VERIFICATION5, False) == 368)
assert(solve(VERIFICATION3, False) == 1206)
print(solve(INPUT, False))
