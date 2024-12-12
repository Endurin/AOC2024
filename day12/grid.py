from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Point:
    x: float = 0
    y: float = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

NEIGHBOR_DIRS = [Point(0,1), Point(1,0), Point(-1,0), Point(0,-1)]


class Grid:
    grid: list[list]
    visited: list[list]

    def __init__(self, path: Path):
        self.read_inputs(path)

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                yield Point(x,y)

    def read_inputs(self, path: Path) -> Grid:
        self.grid = []
        self.visited = []
        for line in open(path, 'r'):
            grid_line = []
            visited_line = []
            for char in line.strip():
                grid_line.append(char)
                visited_line.append(False)
            self.grid.append(grid_line)
            self.visited.append(visited_line)
    
    def out_of_bounds(self, pos: Point) -> bool:
        return pos.y < 0 or pos.y > len(self.grid) - 1 or pos.x < 0 or pos.x > len(self.grid[0]) - 1

    def compute_price(self, part1: bool) -> int:
        total = 0
        for pos in self:
            pos_tiles, pos_fences = self.count_neighbors_with_same_value(pos, part1)
            total += pos_tiles * pos_fences
        return total

    # arbitrary geometric condition to mark only once fence per straight
    def has_highest_xy_in_fence_line(self, pos: Point, nb_dir: Point) -> bool:
        # highest xy is NOT achieved if B is the same type as pos and A isn't, as then ? would be another fence
        # nb | pos
        # A  ? B    

        # check in perpendicular direction
        check_dir = Point(0 if abs(nb_dir.x) > 0 else 1, 0 if abs(nb_dir.y) > 0 else 1)
        pos_value = self.get_value(pos)
        B = pos + check_dir
        if pos_value != self.get_value(B):
            return True
        
        # now check across from there, if A matches B and Pos we return True
        A = B + nb_dir
        if self.get_value(A) != pos_value:
            return False
        return True

    # so for part 2 all I need to do is tag just 1 fence per straight!
    # I can do this by that I'm the part in the chain with the highest x or y value
    def count_neighbors_with_same_value(self, start_pos: Point, part1: bool) -> tuple[int, int]:
        tiles = 0
        fences = 0
        positions_to_check = [start_pos]

        while len(positions_to_check):
            to_check = positions_to_check.pop()
            if self.get_visited(to_check):
                continue
            tiles += 1
            self.set_visited(to_check, True)
            value = self.get_value(to_check)

            for nb_dir in NEIGHBOR_DIRS:
                nb = to_check + nb_dir
                if self.get_value(nb) != value:
                    if part1 or self.has_highest_xy_in_fence_line(to_check, nb_dir):
                        fences += 1
                    continue
                # skip plots already checked for this area
                if self.get_visited(nb):
                    continue
                positions_to_check.append(nb)

        return tiles, fences

    def get_value(self, point: Point) -> str:
        if self.out_of_bounds(point):
            return ''
        return self.grid[point.y][point.x]
    
    def get_visited(self, point: Point) -> bool:
        return self.visited[point.y][point.x]
    
    def set_visited(self, point: Point, value: bool):
        self.visited[point.y][point.x] = value