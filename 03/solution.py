# %% Part 1
with open("input.txt", encoding="ascii") as f:
    bin_strings = [line.strip() for line in f]

required_threshold = len(bin_strings) / 2
gamma = epsilon = ""


def count_positive_bits(string_list):
    positive_bit_counter = [0] * len(string_list[0])
    for bin_number_str in string_list:
        for pos, char in enumerate(bin_number_str):
            positive_bit_counter[pos] += 1 if char == "1" else 0
    return positive_bit_counter


positive_bit_counter = count_positive_bits(bin_strings)

for i in positive_bit_counter:
    gamma += "1" if i > required_threshold else "0"
    epsilon += "1" if i < required_threshold else "0"

print(f"Answer 1: {int(gamma, 2) * int(epsilon, 2)}")

# %% Part 2 - Computationally complexity could be reduced significantly but... currently I'm lazy xD


def filter_diagnostic_report(strings, oxygen: bool = True):
    current_mask = ""
    pos, neg = ("1", "0") if oxygen else ("0", "1")

    while len(strings) > 1:
        required_threshold = len(strings) / 2
        current_mask += pos if count_positive_bits(strings)[len(current_mask)] >= required_threshold else neg
        strings = [x for x in strings if x.startswith(current_mask)]
    return strings[0]


ox, co2 = map(lambda x: filter_diagnostic_report(bin_strings, x), (True, False))
print(f"Answer 2: {int(ox, 2) * int(co2, 2)}")
