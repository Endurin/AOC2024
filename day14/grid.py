from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))


class GridWalker:
    grid: LoopingGrid
    pos: Point
    vel: Point

    def __init__(self, line: str, grid: LoopingGrid):
        self.grid = grid
        p, v = line.strip().split(' ')
        p = p.split('=')[1].split(',')
        v = v.split('=')[1].split(',')
        self.pos = Point(int(p[0]), int(p[1]))
        self.vel = Point(int(v[0]), int(v[1]))

        grid.add(self.pos, 1)
    
    def move(self):
        self.grid.add(self.pos, -1)
        self.pos = self.grid.get_pos(self.pos, self.vel)
        self.grid.add(self.pos, 1)

    def __repr__(self):
        return f'[{self.pos},{self.vel}]'
    
    def __hash__(self):
        return hash((self.pos, self.vel))

NEIGHBOR_DIRS = [Point(0,1), Point(1,0), Point(-1,0), Point(0,-1),
                 Point(1,1), Point(1,-1), Point(-1,1), Point(-1,-1)]

class LoopingGrid:
    x_max: int
    y_max: int
    walker: list[GridWalker]
    grid: list[list]

    def __init__(self, wide: int, tall: int):
        self.x_max = wide
        self.y_max = tall
        self.walkers = []

        self.grid = []
        for y in range(self.y_max):
            self.grid.append([0]*self.x_max)

    def get_quadrant_score(self, walkers: list[GridWalker]) -> int:
        quadrant_sums = [0, 0, 0, 0]
        x_half = (self.x_max-1)/2
        y_half = (self.y_max-1)/2
        for walker in walkers:
            pos = walker.pos
            if pos.x < x_half:
                if pos.y < y_half:
                    quadrant_sums[0] += 1
                elif pos.y > y_half:
                    quadrant_sums[1] += 1
            elif pos.x > x_half:
                if pos.y < y_half:
                    quadrant_sums[2] += 1
                elif pos.y > y_half:
                    quadrant_sums[3] += 1
        return math.prod(quadrant_sums)
    
    def out_of_bounds(self, pos: Point) -> bool:
        return pos.y < 0 or pos.y >= self.y_max or pos.x < 0 or pos.x >= self.x_max

    def get_pos(self, pos: Point, dxy: Point):
        new_pos = pos + dxy
        if self.out_of_bounds(new_pos):
            new_pos.x = new_pos.x % self.x_max
            new_pos.y = new_pos.y % self.y_max
        return new_pos

    def add(self, pos: Point, value: int):
        self.grid[pos.y][pos.x] += value

    def get(self, point: Point) -> int:
        return self.grid[point.y][point.x]

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pt = Point(x,y)
                yield pt, self.get(pt)

    def neighbor_sum_at_least(self, pos: Point, at_least: int) -> list:
        total = 0
        for nb_dir in NEIGHBOR_DIRS:
            nb = pos + nb_dir
            if self.out_of_bounds(nb):
                continue
            if self.get(nb) > 0:
                total += 1
            if total >= at_least:
                return True
        return False

    # A picture probably has a lot of points touching?
    def has_picture_maybe(self) -> bool:
        touch_counter = 0
        total_counter = 0
        for pos, value in self:
            if value == 0:
                continue
            total_counter += 1
            # 1-1 touching happens a lot, narrow it to at least touching 2
            if self.neighbor_sum_at_least(pos, 2):
                touch_counter += 1
        
        return touch_counter > 0.5*total_counter
