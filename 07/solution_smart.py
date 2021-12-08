import numpy as np


def triangular_number(n):  # sum of the first n natural numbers has an explicit formula
    return n * (n + 1) // 2  # == sum(range(n + 1)) == 1 + 2 + 3 + ... + n
    # we can use the floor division operator `//` since a factor of 2 is always in n(n+1)
    # since either n or n+1 is even (so it contains an factor of 2) --> always an integer


with open("input.txt", encoding="ASCII") as f:
    positions = np.array([int(x) for x in f.read().split(",")])

mean = int(np.mean(positions))
med = int(np.median(positions))
if len(positions) % 2 == 0:
    med = int(np.median(np.append(positions, 0)))

fuel = triangular_fuel = 0

for position in positions:
    fuel += abs(position - med)
    triangular_fuel += triangular_number(abs(position - mean))

print(f"Answer 1: pos: {med}, fuel required: {fuel}")
print(f"Answer 2: pos: {mean}, fuel required: {triangular_fuel}")
