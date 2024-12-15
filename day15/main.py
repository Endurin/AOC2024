from pathlib import Path
from grid import Grid, Grid2, Point, RIGHT, LEFT, UP

filedir = Path(__file__).parent.resolve()
VERIFICATION1 = filedir.joinpath("inputs/verification1.txt")
VERIFICATION2 = filedir.joinpath("inputs/verification2.txt")
INPUT = filedir.joinpath("inputs/input.txt")


def solve(path: Path, part1 = True) -> int:
    grid = Grid() if part1 else Grid2()
    walker, instructions = grid.read_inputs(path)
    for i in instructions:
        walker.do(i)
    return grid.get_gps_score()

assert(solve(VERIFICATION1) == 2028)
assert(solve(VERIFICATION2) == 10092)
print(solve(INPUT))

# Lazily test some left/right/up/down shifting
gr = Grid2()
gr.grid = [['.','[',']','[',']','.']]
assert(gr.resolve_box(Point(4,0),LEFT))
assert(gr.grid == [['[',']','[',']','.','.']])
assert(gr.resolve_box(Point(0,0),RIGHT))
assert(gr.grid == [['.','[',']','[',']','.']])

gr.grid = [['.','.','.','.','.','.'],
           ['.','[',']','[',']','.'],
           ['.','.','[',']','.','.']]
assert(gr.resolve_box(Point(2,2),UP))
assert(gr.grid == [['.','[',']','[',']','.'],
                   ['.','.','[',']','.','.'],
                   ['.','.','.','.','.','.']])
gr.grid = [['.','#','.','.','.','.'],
           ['.','[',']','[',']','.'],
           ['.','.','[',']','.','.']]
assert(not gr.resolve_box(Point(2,2),UP))

assert(solve(VERIFICATION2, part1=False) == 9021)
print(solve(INPUT, part1=False))
