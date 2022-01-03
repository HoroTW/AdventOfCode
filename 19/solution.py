from itertools import chain
import itertools


def permute(coords):
    x, y, z = coords
    return [
        (x, y, z),  # all possible orientations normal
        (y, z, x),
        (z, x, y),
        #
        (-z, -y, -x),  # all flipped
        (-y, -x, -z),
        (-x, -z, -y),
        #
        (z, y, -x),  # only x flipped
        (y, -x, z),
        (-x, z, y),
        #
        (z, -y, x),  # only y flipped
        (-y, x, z),
        (x, z, -y),
        #
        (-z, y, x),  # only z flipped
        (y, x, -z),
        (x, -z, y),
        #
        (-x, -y, z),  # only x and y flipped
        (-y, z, -x),
        (z, -x, -y),
        #
        (-x, y, -z),  # only x and z flipped
        (y, -z, -x),
        (-z, -x, y),
        #
        (x, -y, -z),  # only y and z flipped
        (-y, -z, x),
        (-z, x, -y),
    ]


def all_possible_orientations(beacon):
    return zip(*(permute(c) for c in beacon))


multi_sum = lambda tuple1, tuple2: tuple(a + b for a, b in zip(tuple1, tuple2))
multi_dif = lambda tuple1, tuple2: tuple(a - b for a, b in zip(tuple1, tuple2))


def match(coords_a, beacon, max_in_common_threshold=12):
    for beacon_coords in all_possible_orientations(beacon):
        for i, coord_a in enumerate(coords_a):
            for beacon_coord in beacon_coords[i:]:
                delta = multi_dif(coord_a, beacon_coord)
                if commons(coords_a, beacon_coords, delta) >= max_in_common_threshold:  # found a match
                    delta_array = []
                    for beacon_coord in beacon_coords:
                        delta_array.append(multi_sum(beacon_coord, delta))
                    return delta_array, delta
    return None


def commons(a, b, delta):
    s = set()
    for i in a:
        s.add(i)
    for i in b:
        s.add(multi_sum(i, delta))
    return len(a) + len(b) - len(s)


def find_matches(scanners):
    detected = [scanners.pop()]
    deltas = []

    while scanners:
        print(len(scanners))
        for i, s2 in enumerate(scanners):
            for s1 in detected:
                vals = match(s1, s2)
                if vals is not None:
                    matched, delta = vals
                    detected.append(matched)
                    deltas.append(delta)
                    scanners.pop(i)
                    break
            else:  # no break - continue only when no value was found
                continue
            break
    return detected, deltas


def manhatten_distance(tuple1, tuple2):
    return sum(abs(a - b) for a, b in zip(tuple1, tuple2))


with open("input.txt", encoding="ASCII") as f:
    scanners = []
    for single_scanner_readings in f.read().split("\n\n"):
        scanner = []
        for sc_line in single_scanner_readings.split("\n")[1:]:  # skip scanner id
            scanner.append(tuple(int(val) for val in sc_line.split(",")))
        scanners.append(scanner)

detected, deltas = find_matches(scanners)
print("Answer 1:", len(set(chain.from_iterable(detected))))

deltas.append((0, 0, 0))  # insert the first scanner position (it's the relative map origin)
all_possible_scanner_combinations = itertools.combinations(deltas, 2)
max_manhatten_distance = -1

for d1, d2 in all_possible_scanner_combinations:
    max_manhatten_distance = max(max_manhatten_distance, manhatten_distance(d1, d2))

assert max_manhatten_distance > -1, "no distance could be found. No matches?"
print("Answer 2:", max_manhatten_distance)
