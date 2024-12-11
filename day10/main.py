from pathlib import Path
from grid import Grid, Point

filedir = Path(__file__).parent.resolve()
SMALLER_VERIFICATION = filedir.joinpath("inputs/smaller_verification.txt")
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")


# Walk from 9 to all connected 0's and +1 them
def resolve_path(grid: Grid, pos: Point, trail_end: Point, zeros_counters: dict, value: int, count_unique: bool):
    if value == 0:
        if pos not in zeros_counters:
            if count_unique:
                zeros_counters[pos] = set()
            else:
                zeros_counters[pos] = 0
        if count_unique:
            zeros_counters[pos].add(trail_end)
        else:
            zeros_counters[pos] += 1
        return
    
    for nb in grid.get_neighbors_with_value(pos, value - 1):
        resolve_path(grid, nb, trail_end, zeros_counters, value - 1, count_unique)


def solve(path: Path, count_unique = True) -> int:
    grid = Grid(path)
    zeros_counters = {}
    for point, value in grid:
        if value == 9:
            resolve_path(grid, point, point, zeros_counters, value, count_unique)

    return sum(len(x) if count_unique else x for x in zeros_counters.values())


assert(solve(SMALLER_VERIFICATION) == 2)
assert(solve(VERIFICATION) == 36)
print(solve(INPUT))
assert(solve(VERIFICATION, False) == 81)
print(solve(INPUT, False))
