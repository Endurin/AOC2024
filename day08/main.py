from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))


def read_input(path: Path) -> tuple[dict, Point]:
    rv = {}
    max_y = 0
    max_x = 0
    for y, line in enumerate(open(path, 'r')):
        line = line.strip()
        max_y = y
        for x, char in enumerate(line):
            max_x = x
            if char != '.':
                if char not in rv:
                    rv[char] = []
                rv[char].append(Point(x,y))

    return rv, Point(max_x, max_y)

def in_bounds(point: Point, max_point: Point) -> bool:
    return 0 <= point.x <= max_point.x and 0 <= point.y <= max_point.y

def get_resonance_points(point1: Point, point2: Point, max_point: Point, two_to_one: bool):
    rv = []
    vector = point2 - point1
    
    if two_to_one:
        rp1 = point1 - vector
        if in_bounds(rp1, max_point):
            rv.append(rp1)

        rp2 = point2 + vector
        if in_bounds(rp2, max_point):
            rv.append(rp2)
    else:
        rp = point2 - vector
        while in_bounds(rp, max_point):
            rv.append(rp)
            rp -= vector
        rp = point1 + vector
        while in_bounds(rp, max_point):
            rv.append(rp)
            rp += vector
    return rv

def get_all_resonance_points(input_points: list, max_point: Point, two_to_one: bool) -> list:
    rps = []
    for i, point in enumerate(input_points):
        for other in input_points[i+1:]:
            rps.extend(get_resonance_points(point, other, max_point, two_to_one))
    return rps

def solve(path: Path, two_to_one: bool = True) -> int:
    char_to_points, max_point = read_input(path)
    unique_rps = set()
    for points in char_to_points.values():
        rps = get_all_resonance_points(points, max_point, two_to_one)
        for rp in rps:
            unique_rps.add(rp)

    return len(unique_rps)


assert(solve(VERIFICATION) == 14)
print(solve(INPUT))
assert(solve(VERIFICATION, False) == 34)
print(solve(INPUT, False))
