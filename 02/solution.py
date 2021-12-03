# %%
with open("input.txt") as f:
    data = [(dir, int(val)) for dir, val in [line.split() for line in f]]
# %%
aim = horiz = depth1 = depth2 = 0

for dir, val in data:
    if dir == "down":
        depth1 += val
        aim += val
    elif dir == "up":
        depth1 -= val
        aim -= val
    else:  # "forward"
        horiz += val
        depth2 += aim * val

print("Answer 1: ", horiz * depth1)
print("Answer 2: ", horiz * depth2)
