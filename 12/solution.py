# %%
from collections import deque, defaultdict
import numpy as np

# https://docs.scipy.org/doc/scipy/reference/sparse.csgraph.html
# this could be nice but the problem seems to be very simple and I already have started xD

# %%
inp: np.ndarray = np.genfromtxt("test.txt", delimiter="-", dtype=str)
graph = defaultdict(list[str])
count = 0

for edge in inp:
    a, b = edge

    if a != "start":  # ensure start is only on the left side
        graph[b].append(a)
    if b != "start":  # ensure start is only on the left side
        graph[a].append(b)

# %%
stack = deque([("start", {"start"})])

while stack:
    node, visited = stack.pop()
    if node == "end":
        count += 1  # count is enough... I don't need the paths - simplifies everything.. :see_no_evil:
        continue

    for c_node in graph[node]:
        if c_node.isupper() or c_node not in visited:
            stack.append((c_node, visited | {c_node}))  # what is this

print("Answer 1:", count)


# %%
stack = deque([("start", {"start"}, False)])
count = 0

while stack:
    c_node, visited, double_visited = stack.pop()
    if c_node == "end":
        count += 1
        continue

    for c_node in graph[c_node]:
        if c_node not in visited or c_node.isupper():
            stack.append((c_node, visited | {c_node}, double_visited))
            continue
        if double_visited:
            continue
        stack.append((c_node, visited, True))

print("Answer 2:", count)
# %%
