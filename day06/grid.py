from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def copy(self) -> Point:
        return Point(self.x, self.y)
    
    # for dict[] lookup
    def __hash__(self):
        return hash((self.x, self.y))


# 0,0   xmax  
# 
# ymax  xmax,ymax

ROTATE_90_DEG = {
   Point(0,1): Point(-1,0),
   Point(-1,0): Point(0,-1),
   Point(0,-1): Point(1,0),
   Point(1,0): Point(0,1),
}
assert(ROTATE_90_DEG[ROTATE_90_DEG[ROTATE_90_DEG[ROTATE_90_DEG[Point(0,1)]]]] == Point(0,1))

class GridWalker:
    grid: Grid
    pos: Point
    dir: Point
    done: bool
    looping: bool
    track_unique: bool
    track_path: bool
    visited: list
    visited_with_dir: set


    def __init__(self, grid: Grid, pos: Point, dir: Point, track_unique: bool = True, track_path: bool = False):
        self.grid = grid
        self.pos = pos
        self.dir = dir
        self.done = False
        self.looping = False
        self.track_unique = track_unique
        self.track_path = track_path
        self.visited = [pos]
        self.visited_with_dir = {(pos,dir)}
    
    def try_move(self):
        next_pos = self.pos + self.dir
        if self.grid.out_of_bounds(next_pos):
            self.done = True
            return
        if self.grid.wall(next_pos):
            self.dir = ROTATE_90_DEG[self.dir]
            return

        self.pos = next_pos

        if self.track_path or self.track_unique and self.pos not in self.visited:
            self.visited.append(self.pos)

        # loopcheck
        if (self.pos, self.dir) in self.visited_with_dir:
            self.looping = True
            self.done = True
            return

        self.visited_with_dir.add((self.pos, self.dir))

class Grid:
    grid: list[list]

    def __init__(self):
        self.grid = []

    def read_inputs(self, path: Path) -> Point:
        self.grid = []
        starting_point = None
        for line in open(path, 'r'):
            grid_line = []
            for char in line.strip():
                if char == '^':
                    starting_point = Point(len(grid_line), len(self.grid))
                grid_line.append(char)
            self.grid.append(grid_line)
        
        return starting_point
    
    def out_of_bounds(self, pos: Point) -> bool:
        return pos.y < 0 or pos.y > len(self.grid) - 1 or pos.x < 0 or pos.x > len(self.grid[0]) - 1
    
    def wall(self, pos: Point) -> bool:
        return self.grid[pos.y][pos.x] == '#'

    def set(self, pos: Point, char):
        if not self.out_of_bounds(pos):
            self.grid[pos.y][pos.x] = char
