# %%
with open("input.txt", encoding="ascii") as f:
    map2d = [list(map(int, list(x))) for x in f.read().splitlines()]


def neighbors_pos(row_pos, col_pos, map2d):
    for row_step, col_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n_row, n_col = (row_pos + row_step, col_pos + col_step)
        if 0 <= n_row < len(map2d) and 0 <= n_col < len(map2d[0]):
            yield (n_row, n_col)


map_height, map_width = len(map2d), len(map2d[0])
local_minimas = []

for i_r, row in enumerate(map2d):
    for i_c, cell in enumerate(row):
        if all(map2d[n_row][n_col] > cell for n_row, n_col in neighbors_pos(i_r, i_c, map2d)):
            local_minimas.append((i_r, i_c))

risk = [map2d[minima[0]][minima[1]] + 1 for minima in local_minimas]
print("Answer 1:", sum(risk))
# %%
