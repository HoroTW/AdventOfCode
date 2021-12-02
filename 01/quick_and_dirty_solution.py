# %% PART 1
import sys


def read_input(filename):
    """
    Reads the input file and returns a list of integers.
    """
    with open(filename) as f:
        return [int(line) for line in f]


def count_increments(list_of_ints):
    last = sys.maxsize
    count = 0
    for i in list_of_ints:
        if i > last:
            count += 1
        last = i
    return count


lines = read_input("input.txt")
print("Answer 1: ", count_increments(lines))


# %% PART 2
def sum_window(lst, window):
    return [sum(lst[i : i + window]) for i in range(len(lst) - window + 1)]


print("Answer 2: ", count_increments(sum_window(lines, 3)))
