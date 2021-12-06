from collections import Counter

lines = []
with open("input.txt", encoding="ascii") as f:
    for line in f:
        start, end = line.split(" -> ")
        lines.append((tuple(map(int, start.split(","))), tuple(map(int, end.split(",")))))


def get_points(
    line: tuple[tuple[int, int], tuple[int, int]], only_horizontal: bool = True
) -> list[tuple[int, int]]:
    points = []
    s_x, s_y, e_x, e_y = line[0][0], line[0][1], line[1][0], line[1][1]
    step = [0, 0]
    step[0] = 1 if e_x > s_x else -1 if e_x < s_x else 0
    step[1] = 1 if e_y > s_y else -1 if e_y < s_y else 0

    if s_x != e_x and s_y != e_y and only_horizontal:
        return points

    while (s_x, s_y) != (e_x, e_y):
        points.append((s_x, s_y))
        s_x += step[0]
        s_y += step[1]
    points.append((e_x, e_y))
    return points


def get_counts_of_overlapping_points(points: list) -> int:
    counted = Counter(points)
    overlapped_line_points = [k for k, v in counted.items() if v >= 2]
    return len(overlapped_line_points)


global_points = []
_ = [list(map(global_points.append, x)) for x in [get_points(line) for line in lines]]
print(f"Answer 1: {get_counts_of_overlapping_points(global_points)}")

global_points = []
_ = [list(map(global_points.append, x)) for x in [get_points(line, only_horizontal=False) for line in lines]]
print(f"Answer 2: {get_counts_of_overlapping_points(global_points)}")
