from __future__ import annotations
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x-other.x) + abs(self.y-other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

LEFT = Point(-1,0)
RIGHT = Point(1,0)
DOWN = Point(0,1)
UP = Point(0,-1)
START = 'S'
END = 'E'
WALL = '#'
PATH = '.'

NEIGHBOR_DIRS = [LEFT, RIGHT, DOWN, UP]

class Grid:
    grid: list[list]
    start: Point
    end: Point

    def __init__(self, path: Path):
        self.read_inputs(path)

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pt = Point(x,y)
                yield pt, self.get(pt)

    def read_inputs(self, path: Path):
        self.start = None
        self.end = None
        self.grid = []
        for line in open(path, 'r'):
            line = line.strip()
            self.grid.append(list(line))
        
        for point, val in self:
            if val == START:
                self.start = point
            if val == END:
                self.end = point
        assert(self.start is not None)
        assert(self.end is not None)
    
    def out_of_bounds(self, pos: Point) -> bool:
        return pos.y < 0 or pos.y >= len(self.grid) or pos.x < 0 or pos.x >= len(self.grid[0])
    
    def wall(self, pos: Point) -> bool:
        return self.grid[pos.y][pos.x] == WALL

    def get(self, pos: Point):
        if self.out_of_bounds(pos):
            return ''
        return self.grid[pos.y][pos.x]
    
    def set(self, val: str, point: Point):
        if not self.out_of_bounds(point):
            self.grid[point.y][point.x] = val

    def get_neighbors(self, point: Point, exclude: set) -> list[tuple[Point, Point]]:
        rv = []
        for nb_dir in NEIGHBOR_DIRS:
            nb = point + nb_dir
            if nb in exclude:
                continue
            if self.out_of_bounds(nb):
                continue
            if self.wall(nb):
                continue
            rv.append(nb)
        return rv
    
    def get_a_route(self) -> list[Point]:
        path = [self.start]
        pos = path[-1]
        while pos != self.end:
            nbs = self.get_neighbors(pos, set(path))
            assert(len(nbs) == 1)
            pos = nbs[0]
            path.append(pos)

        return path
