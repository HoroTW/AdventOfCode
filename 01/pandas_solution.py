# %%
import pandas as pd

df: pd.DataFrame = pd.read_csv("input.txt", header=None, names=["A"])
print("Answer 1: ", df.diff().query("A > 0").dropna().count()[0])
print("Answer 2: ", df.rolling(window=3).sum().diff().query("A > 0").dropna().count()[0])

# Even better solution since we don't really need a rolling window for the diff:
print("Smarter Answer 2: ", df.diff(3).query("A > 0").dropna().count()[0])
