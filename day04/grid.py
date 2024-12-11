from pathlib import Path

class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def copy(self):
        return Point(self.x, self.y)
    
    def __repr__(self):
        return f'[x={self.x},y={self.y}]'


DIRS = [Point(0,1), Point(1,1), Point(1,0), Point(1,-1), Point(0,-1), Point(-1,-1), Point(-1,0), Point(-1,1)]
X_DIRS = [[Point(-1,-1), Point(1,1)], [Point(-1,1), Point(1,-1)]]

class Grid:
    grid: list[list]

    def __init__(self):
        self.grid = []

    def get(self, pos: Point) -> str:
        # check bounds
        if pos.y < 0 or pos.y > len(self.grid) - 1 or pos.x < 0 or pos.x > len(self.grid[0]) - 1:
            return str()
        return self.grid[pos.y][pos.x]

    def read_inputs(self, path: Path):
        self.grid = []
        for line in open(path, 'r'):
            grid_line = []
            for char in line.strip():
                grid_line.append(char)
            self.grid.append(grid_line)
    
    def get_word_in_dir(self, pos: Point, dir: Point, length = 4) -> str:
        work_pos = pos.copy()
        word = str()
        for i in range(length):
            letter = self.get(work_pos)
            if letter == '':
                return word
            word += letter
            work_pos += dir
        return word

    def count_XMAS_from_position(self, pos: Point) -> int:
        counter = 0
        for dir in DIRS:
            word = self.get_word_in_dir(pos, dir)
            if word == 'XMAS':
                counter += 1
        return counter

    def count_XMAS_occurances(self) -> int:
        counter = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                counter += self.count_XMAS_from_position(Point(x,y))

        return counter

    def has_X_MAS_on_position(self, pos: Point) -> int:
        if self.get(pos) != 'A':
            return 0
        for dirs in X_DIRS:
            letter1 = self.get(pos+dirs[0])
            letter2 = self.get(pos+dirs[1])
            if not ((letter1 == 'M' and letter2 == 'S') or (letter1 == 'S' and letter2 == 'M')):
                return 0
        return 1

    def count_X_MAS_occurances(self) -> int:
        counter = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                counter += self.has_X_MAS_on_position(Point(x,y))

        return counter