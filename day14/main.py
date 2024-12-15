#%%
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

from grid import LoopingGrid, GridWalker


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path, grid: LoopingGrid) -> list[GridWalker]:
    walkers = []
    for line in open(path, 'r'):
        walkers.append(GridWalker(line, grid))

    return walkers

def draw(grid: LoopingGrid):
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [0,1,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(np.array(grid.grid), cmap=cmap, norm=norm)
    plt.show()

def part1(path: Path, wide: int, tall: int, seconds: int) -> int:
    grid = LoopingGrid(wide, tall)
    walkers = read_input(path, grid)
    grid.walkers = walkers
    for _ in range(seconds):
        for walker in walkers:
            walker.move()

    draw(grid)
    return grid.get_quadrant_score(walkers)

def get_walker_hash(walkers: list[GridWalker]) -> int:
    return hash(tuple(walkers))

def part2(path: Path, wide: int, tall: int) -> int:
    grid = LoopingGrid(wide, tall)
    walkers = read_input(path, grid)
    grid.walkers = walkers

    counter = 0
    while True:
        if counter%50 ==0:
            print(f'Step: {counter}')
        counter += 1
        for walker in walkers:
            walker.move()
        if grid.has_picture_maybe():
            draw(grid)
            return counter

assert(part1(VERIFICATION, 11, 7, 100) == 12)
print(part1(INPUT, 101, 103, 100))        

#%%

print(part2(INPUT, 101, 103))
