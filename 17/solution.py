# x and y are independent of each other so I could check them separately but brute force it is
# (for now - maybe this will actually help at the second puzzle)

# %%
from itertools import product


def target_is_hit(sx, sy, target, mpos=(0, 0)):
    tminx, tmaxx, tminy, tmaxy = target
    pos_x, pos_y = mpos
    while pos_x <= tmaxx and pos_y >= tminy:
        pos_x, pos_y, sx, sy = pos_x + sx, pos_y + sy, max(0, sx - 1), sy - 1
        if tminx <= pos_x <= tmaxx and tminy <= pos_y <= tmaxy:
            return True
    return False


def max_height(y):
    return (y + 1) * y // 2


test_target = 20, 30, -10, -5
input_target = 143, 177, -106, -71
s_range = 1500
target = input_target
velocities = []

for sx, sy in product(range(s_range), range(-s_range, s_range)):
    if target_is_hit(sx, sy, target):
        print(sy)
        velocities.append(sy)

max_y_velocity = max(velocities)
print("Answer 1:", max_height(max_y_velocity), "with  max_y_velocity", max_y_velocity)

# I knew it *lach* - now it is helful that I check all values and dont go for the best one immediately
print("Answer 2:", len(velocities))
