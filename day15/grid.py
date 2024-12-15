from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Point:
    x: int = 0
    y: int = 0

    def copy(self) -> Point:
        return Point(self.x, self.y)
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Point):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

LEFT = Point(-1,0)
RIGHT = Point(1,0)
DOWN = Point(0,1)
UP = Point(0,-1)

MOVE = {
   '>': RIGHT,
   '<': LEFT,
   '^': UP,
   'v': DOWN,
}

WALKER = '@'
WALL = '#'
BOX = 'O'
NOTHING = '.'

class GridWalker:
    grid: Grid
    pos: Point

    def __init__(self, grid: Grid, pos: Point):
        self.grid = grid
        self.pos = pos

    def __repr__(self):
        return f'{self.pos}'
    
    def do(self, instruction):
        self.pos = self.grid.try_move(self.pos, MOVE[instruction])


class Grid:
    grid: list[list]

    def __init__(self):
        self.grid = []
    
    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pt = Point(x,y)
                yield pt, self.get(pt)

    def read_inputs(self, path: Path) -> tuple[GridWalker, list]:
        self.grid = []
        instructions = ''
        walker = None
        reading_instructions = False
        for line in open(path, 'r'):
            line = line.strip()
            if len(line) == 0:
                reading_instructions = True
                continue
            if not reading_instructions:
                grid_line = []
                for char in line:
                    if char == WALKER:
                        walker = GridWalker(self, Point(len(grid_line), len(self.grid)))
                        grid_line.append('.')
                    else:
                        grid_line.append(char)
                self.grid.append(grid_line)
            else:
                instructions += line
        
        return walker, instructions
    
    def get_gps_score(self) -> int:
        score = 0
        for pos, value in self:
            if value is not BOX:
                continue
            score += pos.y * 100 + pos.x
        return score
    
    def resolve_box(self, pos: Point, dir: Point) -> bool:
        value = self.get(pos)
        pos_past_end_of_boxes = pos
        while value == BOX:
            pos_past_end_of_boxes += dir
            value = self.get(pos_past_end_of_boxes)
        if value == WALL:
            return False
        # shift array of boxes by 1
        self.set(pos, NOTHING)
        self.set(pos_past_end_of_boxes, BOX)
        return True

    def try_move(self, pos: Point, dir: Point) -> Point:
        new_pos = pos + dir
        val = self.get(new_pos)
        if val == WALL:
            return pos
        if val == BOX:
            if not self.resolve_box(new_pos, dir):
                return pos
        return new_pos

    def set(self, pos: Point, char):
        self.grid[pos.y][pos.x] = char

    def get(self, point: Point) -> int:
        return self.grid[point.y][point.x]
    

BOX_LEFT = '['
BOX_RIGHT = ']'

HORIZONTAL_DIRS = [LEFT, RIGHT]

class Grid2:
    grid: list[list]

    def __init__(self):
        self.grid = []
    
    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pt = Point(x,y)
                yield pt, self.get(pt)

    def read_inputs(self, path: Path) -> tuple[GridWalker, list]:
        self.grid = []
        instructions = ''
        walker = None
        reading_instructions = False
        for line in open(path, 'r'):
            line = line.strip()
            if len(line) == 0:
                reading_instructions = True
                continue
            if not reading_instructions:
                grid_line = []
                for char in line:
                    if char == WALKER:
                        walker = GridWalker(self, Point(len(grid_line), len(self.grid)))
                        grid_line.append('.')
                        grid_line.append('.')
                    elif char == BOX:
                        grid_line.append(BOX_LEFT)
                        grid_line.append(BOX_RIGHT)
                    else:
                        grid_line.append(char)
                        grid_line.append(char)
                self.grid.append(grid_line)
            else:
                instructions += line
        
        return walker, instructions
    
    def get_gps_score(self) -> int:
        score = 0
        for pos, value in self:
            if value is not BOX_LEFT:
                continue
            score += pos.y * 100 + pos.x
        return score
    
    def resolve_box_horizontal(self, pos: Point, dir: Point) -> bool:
        value = self.get(pos)
        pos_past_end_of_boxes = pos.copy()
        while value == BOX_LEFT or value == BOX_RIGHT:
            pos_past_end_of_boxes += dir
            value = self.get(pos_past_end_of_boxes)
        if value == WALL:
            return False
        # shift array of boxes [] by 1
        work_pos = pos.copy()
        self.set(work_pos, NOTHING)
        while work_pos != pos_past_end_of_boxes:
            work_pos += dir
            if self.get(work_pos) == BOX_RIGHT:
                self.set(work_pos, BOX_LEFT)
            elif self.get(work_pos) == BOX_LEFT:
                self.set(work_pos, BOX_RIGHT)
            else:
                if self.get(work_pos - dir) == BOX_LEFT:
                    self.set(work_pos, BOX_RIGHT)
                else:
                    self.set(work_pos, BOX_LEFT)

        return True

    def resolve_box_vertical(self, pos: Point, dir: Point) -> bool:
        to_check = [pos]
        if self.get(pos) == BOX_LEFT: # get other half of box
            to_check.append(pos+RIGHT)
        else:
            to_check.append(pos+LEFT)
        checked = []
        
        while len(to_check):
            check = to_check.pop(0)
            checked.append(check)
            following = check + dir
            following_value = self.get(following)
            if following_value == WALL:
                return False
            if following_value == NOTHING:
                continue
            # now it must be another box, append it to to_check if it isn't in there already
            if following in to_check:
                continue
            to_check.append(following)
            if following_value == BOX_LEFT:
                to_check.append(following + RIGHT)
            else:
                assert(following_value == BOX_RIGHT)
                to_check.append(following + LEFT)

        # if we got here, we can move all boxes. We added them to checked, and
        # can walk back through that to set the values by swapping the 
        # value with the one in dir

        for c in reversed(checked):
            self.swap(c, c+dir)
        return True

    def resolve_box(self, pos: Point, dir: Point) -> bool:
        if dir in HORIZONTAL_DIRS:
            return self.resolve_box_horizontal(pos, dir)
        return self.resolve_box_vertical(pos, dir)

    def try_move(self, pos: Point, dir: Point) -> Point:
        new_pos = pos + dir
        val = self.get(new_pos)
        if val == WALL:
            return pos
        if val == BOX_LEFT or val == BOX_RIGHT:
            if not self.resolve_box(new_pos, dir):
                return pos
        return new_pos

    def set(self, pos: Point, char):
        self.grid[pos.y][pos.x] = char

    def get(self, point: Point) -> int:
        return self.grid[point.y][point.x]
    
    def swap(self, point1: Point, point2: Point):
        self.grid[point1.y][point1.x], self.grid[point2.y][point2.x] = self.grid[point2.y][point2.x], self.grid[point1.y][point1.x]