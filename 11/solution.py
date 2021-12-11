import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter

grid: np.ndarray = np.genfromtxt("input.txt", delimiter=1, dtype=np.int8)

# calls to apply_adj from generic_filer are always with the unmodified grid
def apply_adj(arr: np.ndarray):
    if arr[4] != -1:
        neighbor_flashes = sum(cell > 9.0 for cell in np.concatenate((arr[:4], arr[5:])))
        return arr[4] + neighbor_flashes
    return arr[4]


count = 0
total_steps = 100
first_sync = True

for step in range(total_steps):
    if np.count_nonzero(grid == 0) == 100 and first_sync:
        print(f"Answer 2: Synced after {step} steps")
        first_sync = False
    grid += 1
    while True:
        flashers = grid > 9
        after_adj_flashers = generic_filter(grid, apply_adj, size=3, mode="constant")
        after_adj_flashers[flashers] = -1
        if (grid == after_adj_flashers).all():  # no changes so no one flashed
            all_that_flashed = grid == -1
            count += np.count_nonzero(all_that_flashed)
            grid[all_that_flashed] = 0
            break
        grid = after_adj_flashers
if first_sync:
    print(f"Answer 2: No sync occurred in the first {total_steps} steps")

print(f"Answer 1: They flashed {count} times")
