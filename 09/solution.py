# %%
with open("input.txt", encoding="ascii") as f:
    map2d = [list(map(int, list(x))) for x in f.read().splitlines()]

# %%


def neighbor_positions(row_pos, col_pos, max_w, max_h):
    ret_list = []
    for row_step, col_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n_row, n_col = (row_pos + row_step, col_pos + col_step)
        if 0 <= n_row < max_w and 0 <= n_col < max_h:
            ret_list.append((n_row, n_col))
    return ret_list



# %%
