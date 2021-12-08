def triangular_number(n):  # sum of the first n natural numbers has an explicit formula
    return n * (n + 1) // 2  # == sum(range(n + 1)) == 1 + 2 + 3 + ... + n
    # we can use the floor division operator `//` since a factor of 2 is always in n(n+1)
    # since either n or n+1 is even (so it contains an factor of 2) --> always an integer


with open("input.txt", encoding="ASCII") as f:
    positions = [int(x) for x in f.read().split(",")]

max_position = max(positions) + 1
fuel = [0] * max_position
triangular_fuel = [0] * max_position
for i in range(max_position):
    for position in positions:
        distance = abs(position - i)
        fuel[i] += distance
        triangular_fuel[i] += triangular_number(distance)

print(f"Answer 1: pos: {fuel.index(min(fuel))}, fuel required: {min(fuel)}")
print(f"Answer 2: pos: {triangular_fuel.index(min(triangular_fuel))}, fuel required: {min(triangular_fuel)}")
