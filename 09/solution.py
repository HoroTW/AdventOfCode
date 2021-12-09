import numpy as np
from scipy.ndimage import generic_filter, label

map2d: np.ndarray = np.genfromtxt("input.txt", delimiter=1, dtype=int)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.generic_filter.html
mask: np.ndarray = generic_filter(
    map2d,
    lambda x: min(x[:2]) > x[2] < min(x[3:]),
    footprint=[  # shape of the window
        [0, 1, 0],  # indexes are   [., 0, .],
        [1, 1, 1],  #               [1, 2, 3],
        [0, 1, 0],  #               [., 4, .],
    ],
    mode="constant",  # means that at the edges the cval value is used to pad around the input
    cval=9,
)
print("Answer 1:", ((map2d + 1) * mask).sum())
