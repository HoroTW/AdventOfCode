# %%
import re
import numpy as np
import time


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


pattern = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
with open("input.txt", encoding="ASCII") as f:
    instructions = re.findall(pattern, f.read())
    instructions = [(inst[0], *(int(x) for x in inst[1:])) for inst in instructions]
    instructions = [(1 if inst[0] == "on" else 0, *inst[1:]) for inst in instructions]

grid: np.ndarray = np.zeros((101, 101, 101), dtype=np.int8)

for inst in instructions:
    setting, x1, x2, y1, y2, z1, z2 = inst
    x1, y1, z1 = map(lambda x: clamp(x + 50, 0, 101), (x1, y1, z1))
    x2, y2, z2 = map(lambda x: clamp(x + 51, 0, 101), (x2, y2, z2))
    grid[x1:x2, y1:y2, z1:z2] = setting
print("Answer 1:", np.sum(grid))

# oh no 2758514936282235 cubes are too much xD - that will not fit in memory
# ok so I'll need to do it smarter....
