with open("input.txt", encoding="ascii") as f:
    entries = [list(map(str.strip, line.split("|"))) for line in f]

segment_counter = [0] * 8

for entry in entries:
    lengths = map(len, entry[1].split())
    for length in lengths:
        segment_counter[length] += 1


print("Answer 1:", sum([segment_counter[2], segment_counter[3], segment_counter[4], segment_counter[7]]))
