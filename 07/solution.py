positions = []
with open("input.txt", encoding="ASCII") as f:
    positions = [int(x) for x in f.read().split(",")]


def triangular_number(n): # the sum of the first n natural numbers has an cool explicit formula so we can use that :)
    return n * (n + 1) // 2  # == sum(range(n + 1)) == 1 + 2 + 3 + ... + n
    # we can use the floor division operator `//` since a factor of 2 is always in n(n+1)
    # since either n or n+1 is even (so it contains an factor of 2) --> by /2 we will get an Integer anyway


fuel = [0] * len(positions)
triangular_fuel = [0] * len(positions)
for i in range(len(positions)):
    for position in positions:
        distance = abs(position - i)
        fuel[i] += distance
        triangular_fuel[i] += triangular_number(distance)

print(f"Answer 1: pos: {fuel.index(min(fuel))}, fuel required: {min(fuel)}")
print(f"Answer 2: pos: {triangular_fuel.index(min(triangular_fuel))}, fuel required: {min(triangular_fuel)}")
