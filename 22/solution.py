# %%
import re
import numpy as np


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_instructions(filename="input.txt"):
    pattern = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    with open(filename, encoding="ASCII") as f:
        instructions = re.findall(pattern, f.read())
        instructions = [(inst[0], *(int(x) for x in inst[1:])) for inst in instructions]
        instructions = [(1 if inst[0] == "on" else 0, *inst[1:]) for inst in instructions]
    return instructions


instructions = get_instructions("input.txt")
grid: np.ndarray = np.zeros((101, 101, 101), dtype=np.int8)

for inst in instructions:
    setting, x1, x2, y1, y2, z1, z2 = inst
    x1, y1, z1 = map(lambda x: clamp(x + 50, 0, 101), (x1, y1, z1))
    x2, y2, z2 = map(lambda x: clamp(x + 51, 0, 101), (x2, y2, z2))
    grid[x1:x2, y1:y2, z1:z2] = setting
print("Answer 1:", np.sum(grid))

# oh no 2758514936282235 cubes are too much xD - that will not fit in memory
# ok so I'll need to do it smarter....
# maybe I could just add the volume of an on cube to a total volume...
# and subtract the volume of an off cube from the total volume
# and to do that in a way that would work I would need to calculate the intersection of the cubes
# .... but... I'm not sure how to do that... xD
# ok lets try it step by step
# first I need to get the volume of an on cube.... and then I will neeed a subtract method
# ... but a cube will then contain cubes .... but this should be easy enough (for the computer)
# for me... yeah we will see about that xD


class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.limits = ((x1, x2), (y1, y2), (z1, z2))
        self.cubes = []

    def subtract(self, x1, x2, y1, y2, z1, z2):
        x1, x2, y1, y2, z1, z2 = crop(x1, x2, y1, y2, z1, z2, self.limits)
        if empty(x1, x2, y1, y2, z1, z2):
            return
        cube = Cube(x1, x2, y1, y2, z1, z2)
        for inner in self.cubes:
            inner.subtract(x1, x2, y1, y2, z1, z2)
        self.cubes.append(cube)

    def volume(self):
        tot = 1
        for (a, b) in self.limits:
            tot *= b - a
        return tot - sum(cube.volume() for cube in self.cubes)


def empty(x1, x2, y1, y2, z1, z2):
    return (x1, x2) == (0, 0) or (y1, y2) == (0, 0) or (z1, z2) == (0, 0)


def crop(x1, x2, y1, y2, z1, z2, limits):
    s0, s1 = limits[0]
    c0, c1 = max(x1, s0), min(x2, s1)
    x1, x2 = (c0, c1) if c0 < c1 else (0, 0)

    s0, s1 = limits[1]
    c0, c1 = max(y1, s0), min(y2, s1)
    y1, y2 = (c0, c1) if c0 < c1 else (0, 0)

    s0, s1 = limits[2]
    c0, c1 = max(z1, s0), min(z2, s1)
    z1, z2 = (c0, c1) if c0 < c1 else (0, 0)

    return x1, x2, y1, y2, z1, z2


def solve(instructions):
    cubes = []
    for (setting, x1, x2, y1, y2, z1, z2) in instructions:
        x2, y2, z2 = x2 + 1, y2 + 1, z2 + 1

        if empty(x1, x2, y1, y2, z1, z2):  # this should not happen
            print("empty")  # and it doesn't - but just in case
            continue

        for another in cubes:
            another.subtract(x1, x2, y1, y2, z1, z2)  # remove cube from all other cubes

        if setting:  # on --> readd the cube volume
            cubes.append(Cube(x1, x2, y1, y2, z1, z2))

    return sum(cube.volume() for cube in cubes)


instructions = get_instructions("input.txt")
print("Answer 2:", solve(instructions))
# this became a bit uglier than I thought ^^ --- but it works!... for now that is enough for me
