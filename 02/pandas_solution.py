# %%
import pandas as pd
import numpy as np

df: pd.DataFrame = pd.read_csv("input.txt", header=None, names=["direction", "dist"], sep=" ")

sums = df.groupby("direction").sum()

depth = sums.dist["down"] - sums.dist["up"]
hPos = sums.dist["forward"]

print("Answer 1: ", depth * hPos)
# %%
