from itertools import pairwise
from pathlib import Path

from grid import GridWalker, Point, Grid


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")


def part1(path: Path) -> int:
    grid = Grid()
    starting_pos = grid.read_inputs(path)
    walker = GridWalker(grid=grid, pos=starting_pos, dir=Point(0,-1))
    while not walker.done:
        walker.try_move()
    return len(walker.visited)

def part2(path: Path) -> int:
    grid = Grid()
    starting_pos = grid.read_inputs(path)
    walker = GridWalker(grid=grid, pos=starting_pos, dir=Point(0,-1), track_unique=False, track_path=True)
    while not walker.done:
        walker.try_move()

    print(f'Checking all paths, size: {len(walker.visited)}')
    i = 0
    loop_counter = 0
    blockaded_positions = set()
    for end, prev in pairwise(reversed(walker.visited)):
        if i%100==0:
            print(f'Path: {i}')
        if end in blockaded_positions:
            continue
        grid.set(end, '#')
        # WRONG! I can't start from here, the blockade may prevent me from even getting here!
        # dir = end - prev
        # partial_walker = GridWalker(grid=grid, pos=prev, dir=dir, track_unique=False, track_path=False)
        partial_walker = GridWalker(grid=grid, pos=starting_pos, dir=Point(0,-1), track_unique=False, track_path=False)
        while not partial_walker.done:
            partial_walker.try_move()
        if partial_walker.looping:
            blockaded_positions.add(end)
            loop_counter += 1
        grid.set(end, '.')
        i += 1
    
    return loop_counter

assert(part1(VERIFICATION) == 41)
print(part1(INPUT))
assert(part2(VERIFICATION) == 6)
print(part2(INPUT))

