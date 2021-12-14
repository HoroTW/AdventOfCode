#%%
from collections import Counter, defaultdict


def blow(components, rules, n, last):
    for _ in range(n):
        n_components = defaultdict(int)

        for pair in components:
            products = rules.get(pair)
            if products:
                n = components[pair]
                n_components[products[0]] += n
                n_components[products[1]] += n
            else:
                n_components[pair] = components[pair]
        components = n_components
    return components


rules = {}

with open("input.txt", encoding="ASCII") as f:
    first_line = f.readline().rstrip()
    next(f)  # eat empty line

    for line in map(str.rstrip, f):
        (a, b), _chr = line.split(" -> ")
        rules[a, b] = ((a, _chr), (_chr, b))


components = Counter(zip(first_line, first_line[1:]))
components = blow(components, rules, 40, first_line[-1])
counts = defaultdict(int, {first_line[-1]: 1})

for (a, _), n in components.items():
    counts[a] += n

print("Answer 2:", max(counts.values()) - min(counts.values()))
