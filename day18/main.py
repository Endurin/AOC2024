from pathlib import Path
from a_star import Point, a_star

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> ...:
    points = []
    for line in open(path, 'r'):
        line = line.strip().split(',')
        points.append(Point(int(line[0]), int(line[1])))

    return points

def part1(path: Path, size, nb_bytes) -> int:
    walls = read_input(path)
    goal = Point(size-1,size-1)
    path = a_star(goal, size, walls[0:nb_bytes])
    return len(path)

def part2(path: Path, size, start) -> int:
    walls = read_input(path)
    goal = Point(size-1,size-1)
    path = None
    for i in range(start,len(walls)):
        try:
            # if the new wall isn't in the current fastest path, skip
            if path is not None and walls[i-1] not in path:
                continue
            print(f'Simulating walls {0}-{i}')
            path = a_star(goal, size, walls[0:i])
        except ValueError:
            return walls[i-1]
            
    raise ValueError('Did not find a blockade!')

assert(part1(VERIFICATION, 7, 12) == 22)
print(part1(INPUT, 71, 1024))
assert(part2(VERIFICATION, 7, 12) == Point(6,1))
print(part2(INPUT, 71, 1000))
