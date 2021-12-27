from scipy.ndimage import generic_filter
import numpy as np


def tochr(x):
    return chr(int(x))


def move_right(arr):
    if tochr(arr[4]) == "." and tochr(arr[3]) == ">":
        return ord(">")
    if tochr(arr[4]) == ">" and tochr(arr[5]) == ".":
        return ord(".")
    return arr[4]


def move_down(arr):
    if tochr(arr[4]) == "." and tochr(arr[1]) == "v":
        return ord("v")
    if tochr(arr[4]) == "v" and tochr(arr[7]) == ".":
        return ord(".")
    return arr[4]


with open("input.txt", encoding="ASCII") as f:
    grid = np.array([list(map(ord, line.strip())) for line in f])

i = 1
while True:
    prev = grid.copy()
    grid = generic_filter(grid, move_right, size=3, mode="wrap")
    grid = generic_filter(grid, move_down, size=3, mode="wrap")
    if np.array_equal(prev, grid):
        print("Answer 1:", i)
        break
    i += 1

# this takes 10s ... but it works
# I guess it would become faster if I directly use ints instead of chars...
# maybe I'll do that for the second part
