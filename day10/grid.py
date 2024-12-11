from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

NEIGHBOR_DIRS = [Point(0,1), Point(1,0), Point(-1,0), Point(0,-1)]

class Grid:
    grid: list[list]

    def __init__(self, path: Path):
        self.read_inputs(path)

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pt = Point(x,y)
                yield pt, self.get(pt)

    def read_inputs(self, path: Path) -> Point:
        self.grid = []
        for line in open(path, 'r'):
            grid_line = []
            for char in line.strip():
                grid_line.append(int(char))
            self.grid.append(grid_line)
    
    def out_of_bounds(self, pos: Point) -> bool:
        return pos.y < 0 or pos.y > len(self.grid) - 1 or pos.x < 0 or pos.x > len(self.grid[0]) - 1

    def get_neighbors_with_value(self, pos: Point, value: int) -> list:
        rv = []
        for nb_dir in NEIGHBOR_DIRS:
            nb = pos + nb_dir
            if self.out_of_bounds(nb):
                continue
            if self.get(nb) != value:
                continue
            rv.append(nb)
        return rv

    def get(self, point: Point) -> int:
        return self.grid[point.y][point.x]