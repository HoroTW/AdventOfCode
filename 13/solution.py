# %%
import numpy as np
from matplotlib import pyplot as plt
import ipywidgets as widgets

grid = set()


def fold(sheet, axis, vertical=False):
    folded = set()
    for x, y in sheet:
        if vertical:
            if x > axis:
                x = axis - (x - axis)
        elif y > axis:
            y = axis - (y - axis)

        folded.add((x, y))
    return folded


def display(grid):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    arr = np.zeros((max_y + 1, max_x + 1))

    for x, y in grid:
        arr[y, x] = 1
    plt.imshow(arr, interpolation="nearest")
    plt.show()


with open("input.txt", encoding="ASCII") as f:
    for line in f:
        if line == "\n":
            break
        grid.add(tuple(map(int, line.split(","))))

    line = f.readline() 
    axis = int(line.split("=")[1])
    grid    = fold(grid, axis, 'x' in line)
    print("Answer 1:", len(grid))

    for line in f:
        fold_axis = int(line.split("=")[1])
        grid = fold(grid, fold_axis, "x" in line)
    print("Answer 2: See image", )
    display(grid)

# %%
