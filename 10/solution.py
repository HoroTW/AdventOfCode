#%%
from functools import reduce
import numpy as np

with open("input.txt", encoding="ASCII") as f:
    lines = [x.strip() for x in f]

tokens = [("(", ")", 3, 1), ("[", "]", 57, 2), ("{", "}", 1197, 3), ("<", ">", 25137, 4)]
translation, e_scores, c_scores = {}, {}, {}
openings, correction_scores = [], []
err_score = 0

for t in tokens:
    openings.append(t[0])
    translation[t[0]], translation[t[1]] = t[1], t[0]
    e_scores[t[1]], c_scores[t[1]] = t[2], t[3]

for line in lines:
    stack = []
    for token in line:
        if token in openings:
            stack.append(translation[token])
        else:
            exp = stack.pop()
            if token != exp:
                err_score += e_scores[token]
                break
    else:  # == nobreak (memorize: a for loop that `break`s on hit, then `else` makes sense)
        c_score = reduce(lambda accum, it: accum * 5 + c_scores[it], reversed(stack), 0)
        correction_scores.append(c_score)

print(f"Answer 1 (error score): {err_score} ")
print(f"Answer 2 (median correction score): {np.median(correction_scores).astype(int)}")
