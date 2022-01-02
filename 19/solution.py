def permute(coords):
    x, y, z = coords
    return [
        (x, y, z), # all possible orientations normal
        (y, z, x),
        (z, x, y),
        #
        (-z, -y, -x), # all flipped
        (-y, -x, -z),
        (-x, -z, -y),
        #
        (z, y, -x), # only x flipped
        (y, -x, z),
        (-x, z, y),
        #
        (z, -y, x), # only y flipped
        (-y, x, z),
        (x, z, -y),
        #
        (-z, y, x), # only z flipped
        (y, x, -z),
        (x, -z, y),
        #
        (-x, -y, z), # only x and y flipped
        (-y, z, -x),
        (z, -x, -y),
        #
        (-x, y, -z), # only x and z flipped
        (y, -z, -x),
        (-z, -x, y),
        #
        (x, -y, -z), # only y and z flipped
        (-y, -z, x),
        (-z, x, -y),

    ]


def all_possible_orientations(beacon):
    return zip(*(permute(c) for c in beacon))


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