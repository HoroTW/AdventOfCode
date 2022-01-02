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
                if commons(coords_a, beacon_coords, delta) >= max_in_common_threshold:
                    # chaka this could be one
                    delta_array = []
                    for beacon_coord in beacon_coords:
                        delta_array.append(multi_sum(beacon_coord, delta))
                    return delta_array, delta
    return None


def commons(a, b, delta):
    s = set()
    for i in a:
        s.add(i)
    for j in b:
        s.add(multi_sum(j, delta))
    return len(a) + len(b) - len(s)


with open("input.txt", encoding="ASCII") as f:
    scanners = []
    for single_scanner_readings in f.read().split("\n\n"):
        scanner = []
        for sc_line in single_scanner_readings.split("\n")[1:]:
            scanner.append(tuple(int(val) for val in sc_line.split(",")))
        scanners.append(scanner)

print(scanners[:2])
print()
single_scanner = scanners[0]
print(list(all_possible_orientations(single_scanner)))

print()
single_scanner_orientations = list(all_possible_orientations(single_scanner))
print(single_scanner)
print(single_scanner_orientations)
print()

for i, scanner in enumerate(scanners[1:]):
    print(f"checking scanner {0} against scanner {i+1}")
    if match(scanners[0], scanner):
        print(f"match found for first scanner with {i + 1}. scanner")