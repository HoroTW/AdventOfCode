import timeit


def clear_right(numbers: list, pos: int, clear_value: int) -> list:
    for i in range(pos, len(numbers)):
        numbers[i] = clear_value


def input_func(w, z, v_1, v_2, v_3):
    x = z % 26
    z //= v_1
    x += v_2
    x = int(x != w)
    y = 25 * x + 1
    z *= y
    y = (w + v_3) * x
    z += y

    return z


def solve(limits: list, start_number_as_list: list, increment: int):
    n = start_number_as_list
    counter = 0

    v_1 = [1, 1, 1, 26, 26, 1, 26, 26, 1, 1, 26, 1, 26, 26]
    v_2 = [12, 13, 13, -2, -10, 13, -14, -5, 15, 15, -14, 10, -14, -5]
    v_3 = [7, 8, 10, 4, 4, 6, 11, 13, 1, 8, 4, 13, 4, 14]

    while True:
        while 0 in n or 10 in n:
            assert n[0] != 0, "did not find any matching number"
            assert n[0] != 10, "did not find any matching number"
            for i, element in enumerate(n):
                if element == 0:
                    n[i - 1] += increment
                    clear_right(n, i, 9)
                if element == 10:
                    n[i - 1] += increment
                    clear_right(n, i, 1)

        counter += 1
        z = 0

        for block in range(14):
            z = input_func(n[block], z, v_1[block], v_2[block], v_3[block])
            if z > limits[block]:
                n[block] = n[block] + increment
                break
        else:
            print("found fitting number in", counter, "steps")
            return "".join(map(str, n))


limits = [81, 2081, 54106, 2080, 79, 2054, 78, 2, 28, 728, 27, 702, 26, 0]
start_list9, start_list1 = list(map(int, "9" * 14)), list(map(int, "1" * 14))
print("Answer 1:", solve(limits, start_list9, increment=-1))
print("Answer 2:", solve(limits, start_list1, increment=1))
print(timeit.timeit(solve(limits, start_list9, increment=-1), number=10000) / 10000 * 10 ** 9, "ns")
print(timeit.timeit(solve(limits, start_list1, increment=1), number=10000) / 10000 * 10 ** 9, "ns")
