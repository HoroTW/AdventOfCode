#%%
from collections import Counter


class Node:
    def __init__(self, v, nxt=None):
        self.value = v
        self.next = nxt

    def __iter__(self):
        return NodeIterator(self)

    def __next__(self):
        if self.next is None:
            raise StopIteration
        return self.next


class NodeIterator:
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def __next__(self):
        if self.node is None:
            raise StopIteration
        node = self.node
        self.node = self.node.next
        return node.value


head = None
rules = {}


with open("input.txt", encoding="ASCII") as f:
    first_line = f.readline().rstrip()

    head = Node(first_line[0])
    cur = head
    for c in first_line[1:]:
        cur.next = Node(c)
        cur = cur.next

    next(f)  # eat empty line

    for line in map(str.rstrip, f):
        search, _chr = line.split(" -> ")
        rules[search] = _chr

# %%

for _ in range(5):
    cur = head

    while cur.next:
        nxt = cur.next
        cur_str = cur.value + nxt.value

        if cur_str in rules:
            cur.next = Node(rules[cur_str], nxt)

        cur = nxt


counts = sorted(Counter(head).values())


print("Answer 1:", counts[-1] - counts[0])
