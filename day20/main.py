from pathlib import Path
from grid import Grid, Point

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")


# Look at the path, grab pairs of nodes sufficient steps away, 
# and see if their distance is within the cheat distance.
def get_num_cheats(route: list[Point], min_saved: int, max_cheat_dist: int, print_progress) -> int:
    cheats = 0
    counter = 0
    for i, p1 in enumerate(route):
        if counter%100 ==0 and print_progress:
            print(f'Finished {counter} out of {len(route)}, found {cheats} so far')
        for j, p2 in enumerate(route[i+min_saved:]):
            dist = p1.manhattan_distance(p2)
            steps_saved = j + min_saved - dist
            if dist <= max_cheat_dist and steps_saved >= min_saved:
                cheats += 1
        counter += 1

    return cheats


def solve(path: Path, min_saved: int, max_cheat_dist = 2, print_progress = False) -> int:
    grid = Grid(path)
    route = grid.get_a_route()
    cheats = get_num_cheats(route, min_saved, max_cheat_dist, print_progress)

    return cheats

# part 1
assert(solve(VERIFICATION, 65) == 0)
assert(solve(VERIFICATION, 64) == 1)
assert(solve(VERIFICATION, 63) == 1)
assert(solve(VERIFICATION, 40) == 2)
assert(solve(VERIFICATION, 1) == 44)
print(solve(INPUT, 100, print_progress=True))
# part 2
assert(solve(VERIFICATION, 76, 20) == 3)
assert(solve(VERIFICATION, 74, 20) == 7)
print(solve(INPUT, 100, 20, print_progress=True))
