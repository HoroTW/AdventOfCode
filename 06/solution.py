from collections import Counter, defaultdict


fish = []
with open("input.txt", encoding="ascii") as f:
    timers = map(int, f.read().split(","))
    fish = Counter(timers)  # Reuse the Counter from the previous exercise


def step(fish: dict[int, int], days_to_sim: int, new_fish_penalty: int = 2, reproduction_timer: int = 6):
    for _ in range(days_to_sim):
        new_fish = defaultdict(int)  # Creates a new key if it doesn't exist - handy!

        for timer, n_fish in fish.items():
            if timer <= 0:
                new_fish[reproduction_timer] += n_fish
                new_fish[reproduction_timer + new_fish_penalty] += n_fish
            else:
                new_fish[timer - 1] += n_fish

        fish = new_fish

    return fish


print("Answer 1:", sum(step(fish, 80).values()))
print("Answer 2:", sum(step(fish, 256).values()))
