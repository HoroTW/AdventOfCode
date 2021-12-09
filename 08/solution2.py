import numpy as np

with open("input.txt", encoding="ascii") as f:
    entries = [list(map(lambda x: list(map(list, x.split())), map(str.strip, line.split("|")))) for line in f]


class Letter:
    name: int = -1
    segments: list[str] = []
    cardinality: int = 0

    def __init__(self, name: int, segments: list[str]):
        self.name = name
        self.segments = segments
        self.cardinality = len(segments)

    def __str__(self):
        return f"{self.name}: cardinality={self.cardinality} segments={self.segments}"

    def __repr__(self) -> str:
        return str(self)

    def same_cardinality(self, segmentList) -> bool:
        return self.cardinality == len(segmentList)


solution_sum = 0

for entry in entries:
    e_input, e_output = entry[0], entry[1]

    found_letters = [None] * 10
    found_cardinalities = [[] for _ in range(10)]

    for unknown in e_input:
        u_len = len(unknown)
        if u_len == 2:
            found_letters[1] = Letter(1, unknown)
        elif u_len == 4:
            found_letters[4] = Letter(4, unknown)
        elif u_len == 3:
            found_letters[7] = Letter(7, unknown)
        elif u_len == 7:
            found_letters[8] = Letter(8, unknown)
        else:
            found_cardinalities[u_len].append(Letter(-1, unknown))

    a = np.setdiff1d(found_letters[7].segments, found_letters[1].segments)

    for c6 in found_cardinalities[6]:
        if c6.name != -1:
            pass
        elif not all(np.isin(found_letters[7].segments, c6.segments)):
            found_letters[6] = Letter(6, c6.segments)
            c6.name = 6
        elif all(np.isin(found_letters[4].segments, c6.segments)):
            found_letters[9] = Letter(9, c6.segments)
            c6.name = 9
        elif not all(np.isin(found_letters[4].segments, c6.segments)):
            found_letters[0] = Letter(0, c6.segments)
            c6.name = 0

    c = np.setdiff1d(found_letters[8].segments, found_letters[6].segments)
    f = np.setdiff1d(found_letters[1].segments, c)
    e = np.setdiff1d(found_letters[8].segments, found_letters[9].segments)
    d = np.setdiff1d(found_letters[6].segments, found_letters[0].segments)
    g = np.setdiff1d(found_letters[9].segments, np.concatenate([found_letters[4].segments, a]))
    b = np.setdiff1d(found_letters[8].segments, np.concatenate([a, c, d, e, f, g]))

    found_letters[2] = Letter(2, np.concatenate([a, c, d, e, g]))
    found_letters[3] = Letter(3, np.concatenate([a, c, d, f, g]))
    found_letters[5] = Letter(5, np.concatenate([a, b, d, f, g]))

    str_num = ""
    for output in e_output:
        for letter in found_letters:
            if np.array_equal(sorted(output), sorted(letter.segments)):
                str_num = f"{str_num}{letter.name}"

    solution_sum += int(str_num)

print("Answer 2:", solution_sum)
