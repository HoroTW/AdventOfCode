# %%
from functools import reduce
import io
from icecream import ic

LIT_VALUE = 4

TID_SUM = 0
TID_PRODUCT = 1
TID_MINIMUM = 2
TID_MAXIMUM = 3
TID_GREATER_THAN = 5
TID_LESS_THAN = 6
TID_EQUAL_TO = 7


class Binary_Stream:
    def __init__(self, file):
        raw_hex_data = file.read()
        raw_bytes = bytes.fromhex(raw_hex_data)
        self.pos = 0
        self.bits = "".join([f"{x:08b}" for x in raw_bytes])

    def decode_int(self, n_bits):
        start = self.pos
        end = start + n_bits
        as_int = int(self.bits[start:end], 2)

        self.pos = end
        return as_int

    def decode_packet_data(self, tid):
        if tid == LIT_VALUE:
            return self.decode_value_data()
        return self.decode_operator_data()

    def reset(self):
        self.pos = 0
        return self

    def decode_value_data(self):
        value = 0
        group = 0b1_0000
        four_lsb_filter = 0b0_1111
        shift_dist = 4

        while group & 0b1_0000:  # filter for 5th bit
            group = self.decode_int(5)
            value <<= shift_dist  # e.g. 4 bits
            value += group & four_lsb_filter  # filter group and add to value
        return value

    def decode_operator_data(self):
        ltid = self.decode_int(1)

        if ltid == 1:
            return list(self.decode_packets(self.decode_int(11)))

        return self.decode_len_packets(self.decode_int(15))

    def decode_packet(self):
        version = self.decode_int(3)  # first 3 bits
        tid = self.decode_int(3)  # next 3 bits
        data = self.decode_packet_data(tid)  # next bits
        return (version, tid, data)

    def decode_packets(self, count):
        for _ in range(count):
            yield self.decode_packet()

    def decode_len_packets(self, length):
        end = self.pos + length
        pkts = []

        while self.pos < end:
            pkts.append(self.decode_packet())

        return pkts


def sum_versions(packet):
    version, tid, data = packet

    if tid == 4:
        return version

    return version + sum(map(sum_versions, data))


with open("input.txt", encoding="ASCII") as f:
    bs = Binary_Stream(f)

pkt = bs.decode_packet()
print("Answer 1:", sum_versions(pkt))


def compute(pkt):
    _, tid, data = pkt

    if tid == 4:
        return data

    values = map(compute, data)

    if tid == TID_SUM:
        return reduce(lambda x, y: x + y, values)
    if tid == TID_PRODUCT:
        return reduce(lambda x, y: x * y, values)
    if tid == TID_MINIMUM:
        return reduce(lambda x, y: x if x < y else y, values)
    if tid == TID_MAXIMUM:
        return reduce(lambda x, y: x if x > y else y, values)
    if tid == TID_GREATER_THAN:
        return reduce(lambda x, y: x > y, values)
    if tid == TID_LESS_THAN:
        return reduce(lambda x, y: x < y, values)
    if tid == TID_EQUAL_TO:
        return reduce(lambda x, y: x == y, values)

    raise f"Unknown operator for tid {tid}"


print("Answer 2:", compute(pkt))


#%% Tests

TST_DATA = {
    "D2FE28": {
        "bin_str": "110100101111111000101000",
        "version": 6,
        "tid": 4,
        "sum": 6,
        "computed": 2021,
    },
    "38006F45291200": {
        "bin_str": "00111000000000000110111101000101001010010001001000000000",
        "version": 1,
        "tid": 6,
        "sum": 9,
        "computed": 1,
    },
    "EE00D40C823060": {
        "bin_str": "11101110000000001101010000001100100000100011000001100000",
        "version": 7,
        "tid": 3,
        "sum": 14,
        "computed": 3,
    },
    "8A004A801A8002F478": {
        "version": 4,
        "bin_str": "100010100000000001001010100000000001101010000000000000101111010001111000",
        "tid": 2,
        "sum": 16,
        "computed": 15,
    },
    "620080001611562C8802118E34": {
        "version": 3,
        "bin_str": "01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100",
        "tid": 0,
        "sum": 12,
        "computed": 46,
    },
    "C0015000016115A2E0802F182340": {
        "version": 6,
        "bin_str": "1100000000000001010100000000000000000001011000010001010110100010111000001000000000101111000110000010001101000000",
        "tid": 0,
        "sum": 23,
        "computed": 46,
    },
    "A0016C880162017C3686B18A3D4780": {
        "version": 5,
        "bin_str": "101000000000000101101100100010000000000101100010000000010111110000110110100001101011000110001010001111010100011110000000",
        "tid": 0,
        "sum": 31,
        "computed": 54,
    },
}

print(f"\n[{'#'*20}### TESTS ###{'#'*20}]")
for inp, outputs in TST_DATA.items():
    bs = Binary_Stream(io.StringIO(inp))
    assert bs.bits == outputs["bin_str"]
    version, tid, _ = bs.decode_packet()
    assert version == outputs["version"]
    assert tid == outputs["tid"]

    bs.reset()  # because the operations changed the pos already
    assert sum_versions(bs.decode_packet()) == outputs["sum"]

    bs.reset()
    assert compute(bs.decode_packet()) == outputs["computed"]

    print("Tests OK for input:", inp)

print("\nAll tests PASSED")
