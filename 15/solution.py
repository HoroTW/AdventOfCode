# %%
import numpy as np
from networkx import grid_2d_graph, shortest_path_length, DiGraph
from itertools import product

grid: np.ndarray = np.genfromtxt("input.txt", delimiter=1, dtype=int)

n = len(grid)
graph = grid_2d_graph(n, n, create_using=DiGraph)

for u, v in graph.edges:
    graph[u][v]["weight"] = grid[v[1]][v[0]]
print("Answer 1:", shortest_path_length(graph, (0, 0), (n - 1, n - 1), "weight"))

big_grid = np.zeros((n * 5, n * 5), dtype=int)

for row, col in product(range(n * 5), range(n * 5)):
    big_grid[col][row] = grid[col % n][row % n] + (row // n) + (col // n)

big_grid[big_grid > 9] -= 9

n = len(big_grid)
graph = grid_2d_graph(n, n, create_using=DiGraph)

for u, v in graph.edges:
    graph[u][v]["weight"] = big_grid[v[1]][v[0]]
print("Answer 2:", shortest_path_length(graph, (0, 0), (n - 1, n - 1), "weight"))
