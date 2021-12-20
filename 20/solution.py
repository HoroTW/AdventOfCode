# %%
import numpy as np
from scipy.ndimage import generic_filter
from matplotlib import pyplot as plt

#%%
with open("input.txt", encoding="ASCII") as f:
    alg, img = f.read().split("\n\n")

alg = list(map(lambda x: int(x == "#"), alg))
img = np.array([[int(c == "#") for c in r] for r in img.strip().split("\n")], dtype=np.int8)
img = np.pad(img, (55, 55))

for i in range(50):
    img = generic_filter(
        img,
        lambda x: alg[sum(d * 2 ** j for j, d in enumerate(x.astype(int)[::-1]))],
        size=3,
    )
    if i + 1 in (2, 50):
        print(np.count_nonzero(img))

plt.imshow(img)
