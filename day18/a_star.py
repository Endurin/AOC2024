from __future__ import annotations
from dataclasses import dataclass
from functools import cmp_to_key


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

NEIGHBOR_DIRS = [LEFT, RIGHT, DOWN, UP]

INF=9999999

# cost estimation to go from a to the goal
def h(a: Point, goal: Point) -> int:
    return a.manhattan_distance(goal)

def reconstruct_path(came_from: dict, current) -> list:
    total_path = []
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def out_of_bounds(pos: Point, size: int) -> bool:
    return pos.y < 0 or pos.y >= size or pos.x < 0 or pos.x >= size

def get_neighbors(current: Point, size: int, walls: set[Point]):
    nbs = []
    for nb_dir in NEIGHBOR_DIRS:
        nb = current + nb_dir
        if out_of_bounds(nb, size):
            continue
        if nb in walls:
            continue
        nbs.append(nb)
    return nbs


def a_star(goal: Point, size: int, walls: set[Point]) -> list:
    start = Point(0,0)
    came_from = {}
    g_score = {start: 0}
    f_score = {start:  h(start, goal)}
    open_set = [start]

    # sort by f_score of node
    def compare(node1, node2):
        return f_score.get(node1, INF) - f_score.get(node2, INF)

    while len(open_set):
        open_set.sort(key=cmp_to_key(compare))
        current = open_set.pop(0)

        if current == goal:
            return reconstruct_path(came_from, current)
        
        for nb in get_neighbors(current, size, walls):
            score = g_score[current] + 1
            if score < g_score.get(nb, INF):
                came_from[nb] = current
                g_score[nb] = score
                f_score[nb] = score + h(nb, goal)
                if nb not in open_set:
                    open_set.append(nb)

    raise ValueError('NO PATH?!')