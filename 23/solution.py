import time
from dataclasses import dataclass
from typing import Tuple
from math import inf


cost_dict = {"A": 1, "B": 10, "C": 100, "D": 1000}
play_dict_cache = {}


class Edge:
    def __init__(self, source: "Node", target: "Node", cost: int = -1):
        self.source = source
        self.target = target
        self.cost = cost

    def __repr__(self):
        return f"{self.source.name} -> {self.target.name}"

    def __eq__(self, other):
        return (
            self.source == other.source
            and self.target == other.target
            or self.source == other.target
            and self.target == other.source
        )


class Node:
    def __init__(self, name):
        self.name: str = name
        self.type: str = name[0]
        self.order = int(name[1])
        self.edges: list[Edge] = []
        self.occupation = None
        self.is_room = self.type in ["A", "B", "C", "D"]
        self.is_hallway = self.type == "H"
        self.is_top_room = self.order == 4 and self.is_room

    def connect(self, node, cost):
        self.edges.append(Edge(self, node, cost))
        node.edges.append(Edge(node, self, cost))

    def disconnect(self, node):
        self.edges.remove(Edge(self, node))
        node.edges.remove(Edge(node, self))

    def occupy(self, name):
        cost = cost_dict[name]
        self.occupation = (name, cost)

    def get_occupier_type(self):
        if self.occupation is not None:
            return self.occupation[0][0]
        return " "

    def get_occupier_cost_multiplier(self):
        if self.occupation is not None:
            return self.occupation[1]
        raise Exception("Node is not occupied")

    def is_occupied(self):
        return self.occupation is not None

    def is_filled_with_matching_type(self):
        return self.get_occupier_type() == self.type

    def move(self, target: "Node"):
        assert self.is_occupied(), "Self needs to be occupied"
        assert target.is_occupied() is False, "Target needs to be unoccupied"
        target.occupation = self.occupation
        self.occupation = None

    def __repr__(self):
        return f"name: {self.name}, occupation: {self.occupation}, \tedges: {self.edges}"

    def __hash__(self):
        return hash((self.name, self.occupation))

    def __eq__(self, __o: object) -> bool:
        return self.occupation == __o.occupation and self.name == __o.name

    def __ne__(self, other):
        return not (self == other)


@dataclass
class Move:
    origin: Node
    target: Node
    cost: int


# fmt: off
# Create Rooms
A1 = Node("A1") ; B1 = Node("B1") ; C1 = Node("C1") ; D1 = Node("D1")
A2 = Node("A2") ; B2 = Node("B2") ; C2 = Node("C2") ; D2 = Node("D2")
A3 = Node("A3") ; B3 = Node("B3") ; C3 = Node("C3") ; D3 = Node("D3")
A4 = Node("A4") ; B4 = Node("B4") ; C4 = Node("C4") ; D4 = Node("D4")

# Create Hallways
H1 = Node("H1") ; H2 = Node("H2") ; H3 = Node("H3") ; H4 = Node("H4") ; H5 = Node("H5") ; H6 = Node("H6") ; H7 = Node("H7")

# Connect the Rooms themselves # 1 is the cost
A1.connect(A2, 1) ; B1.connect(B2, 1) ; C1.connect(C2, 1) ; D1.connect(D2, 1)
A2.connect(A3, 1) ; B2.connect(B3, 1) ; C2.connect(C3, 1) ; D2.connect(D3, 1)
A3.connect(A4, 1) ; B3.connect(B4, 1) ; C3.connect(C4, 1) ; D3.connect(D4, 1)

# Connect the Hallways
H1.connect(H2, 1) ; H2.connect(H3, 2) ; H3.connect(H4, 2) ; H4.connect(H5, 2) ; H5.connect(H6, 2) ; H6.connect(H7, 1)
# Connect the Hallways to the Rooms
A4.connect(H2, 2) ; A4.connect(H3, 2) ; B4.connect(H3, 2) ; B4.connect(H4, 2) ; C4.connect(H4, 2) ; C4.connect(H5, 2) ; D4.connect(H5, 2) ; D4.connect(H6, 2)

# occupy the rooms
#default_occupation
A2.occupy("A") ; B2.occupy("B") ; C2.occupy("C") ; D2.occupy("D")
A1.occupy("A") ; B1.occupy("B") ; C1.occupy("C") ; D1.occupy("D")

# A4.occupy("D") ; B4.occupy("B") ; C4.occupy("C") ; D4.occupy("C")
# A3.occupy("D") ; B3.occupy("C") ; C3.occupy("B") ; D3.occupy("A")
# A2.occupy("D") ; B2.occupy("B") ; C2.occupy("A") ; D2.occupy("C")
# A1.occupy("D") ; B1.occupy("A") ; C1.occupy("B") ; D1.occupy("A")

A4.occupy("B") ; B4.occupy("C") ; C4.occupy("B") ; D4.occupy("D")
A3.occupy("A") ; B3.occupy("D") ; C3.occupy("C") ; D3.occupy("A")

# Add all the nodes to a list (game_map)
game_map = (A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, D4, H1, H2, H3, H4, H5, H6, H7)
# fmt: on


def get_connected_nodes_of_same_type(node: Node) -> list[Node]:
    nodes = []
    nodes_tocheck = [node]

    while nodes_tocheck:
        n = nodes_tocheck.pop()

        for edge in n.edges:
            nxt_node = edge.target
            if nxt_node in nodes:
                continue

            if nxt_node.type == node.type:
                nodes.append(nxt_node)
                nodes_tocheck.append(nxt_node)
    return nodes


def is_this_home_clear(home: Node):
    """
    returns true if the home is clear OR IF IT IS CALLED ON A HALLWAY
    """
    if home.type == "H":
        return True

    home_nodes = get_connected_nodes_of_same_type(home)
    for node in home_nodes:
        if node.is_occupied():
            if node.get_occupier_type() != home.type:
                return False

    return True


def is_hallway_clear(game_map: list[Node]):
    """
    returns true if the hallway is clear
    """
    for node in game_map:
        if node.type == "H":
            if node.is_occupied():
                return False

    return True


def is_won(game_map: list[Node]):
    """
    returns true if the game is won
    """
    return all(is_this_home_clear(node) for node in game_map) and is_hallway_clear(game_map)


def print_map(game_map: list[Node]):
    Hh, Ah, Bh, Ch, Dh = [], [], [], [], []

    for node in game_map:
        if node.type == "H":
            Hh.append(node.get_occupier_type())
        if node.type == "A":
            Ah.append(node.get_occupier_type())
        if node.type == "B":
            Bh.append(node.get_occupier_type())
        if node.type == "C":
            Ch.append(node.get_occupier_type())
        if node.type == "D":
            Dh.append(node.get_occupier_type())

    print(f"{'#'* 13}\n#{Hh[0]}{Hh[1]} {Hh[2]} {Hh[3]} {Hh[4]} {Hh[5]}{Hh[6]}#")
    print(f"###{Ah[3]}#{Bh[3]}#{Ch[3]}#{Dh[3]}###")
    for i in range(len(Ah) - 1, 0, -1):
        print(f"  #{Ah[i]}#{Bh[i]}#{Ch[i]}#{Dh[i]}#")
    print(f"  {'#'*9}  \n")


def is_home_bellow_node_clear(node: Node):
    """
    returns true if all home nodes below the current home node are clear or
    allready filled with a home node
    """
    assert node.is_room
    siblings = get_connected_nodes_of_same_type(node)
    for sibling in siblings:
        if sibling.order >= node.order:
            continue  # we only check the siblings below the current node

        if sibling.is_filled_with_matching_type() is False:
            return False

    return True


def can_move_to_home_spot(node: Node, home_node: Node):
    assert home_node.is_room

    if home_node.type != node.get_occupier_type():
        return False  # not your home

    siblings = get_connected_nodes_of_same_type(home_node)
    for lower_node in siblings:
        if lower_node.order >= home_node.order:
            continue  # so this is not a lower node - skip it

        if lower_node.is_occupied() is False:
            return False  # we can't move to a spot if a spot below is not filled
        if lower_node.is_filled_with_matching_type() is False:
            return False  # so the lower nodes are not jet done we cant move on top of them

    return True


def distance(x: int, y: int):
    return abs(abs(x) - abs(y))


def get_path_to_top_room(node: Node) -> Tuple[list[Node], int]:
    """
    returns a list of nodes which are the path to the top room excluding the current node
    Also returns the cost of the path
    """
    assert node.is_room

    path = []
    cost = 0
    while node.is_top_room is False:
        for edge in node.edges:
            if edge.target.order > node.order:
                path.append(edge.target)
                cost += edge.cost
                node = edge.target

    return path, cost


def get_path_to_target_hallway_node(node: Node, dst_order: int) -> Tuple[list[Node], int]:
    """
    returns a list of nodes which are the path to the target hallway node excluding the current node
    Also returns the cost of the path
    """
    path = []
    cost = 0

    while node.order != dst_order or node.is_room:
        next_hallway_nodes = []

        for edge in node.edges:
            if edge.target.is_room:
                continue  # wrong direction we dont wan't to go back to the room
            next_hallway_nodes.append((edge.target, edge.cost))

        assert len(next_hallway_nodes) == 2

        n1, n2 = next_hallway_nodes[0][0], next_hallway_nodes[1][0]

        if distance(n1.order, dst_order) < distance(n2.order, dst_order):
            path.append(n1)  # go to n1
            cost += next_hallway_nodes[0][1]
            node = n1
        else:
            path.append(n2)  # go to n2
            cost += next_hallway_nodes[1][1]
            node = n2

    return path, cost


def can_move_to(origin: Node, destination: Node) -> Tuple[bool, int]:
    """
    returns true if the origin node can move to the destination node
    Also returns the cost of the move
    """
    assert (origin.is_room and destination.is_room) is False, "oO1"
    assert (origin.is_hallway and destination.is_hallway) is False, "oO2"
    assert origin.is_occupied(), "oO3"
    assert destination.is_occupied() is False, "oO4"

    reverse_order = origin.is_hallway  # the logic is allways for room -> hallway
    path: list[Node] = []
    costs = 0

    if reverse_order is False:  # room -> hallway
        c_node = origin
        target_order = destination.order
    else:  # hallway -> room  - trick: build the reverse path
        c_node = destination
        target_order = origin.order
        reverse_order = True

    path.append(c_node)
    path_to_top, costs_to_top = get_path_to_top_room(c_node)
    path.extend(path_to_top)
    costs += costs_to_top
    c_node = path[-1]
    assert c_node.is_top_room, "the top room should be the last node in the path"

    path_to_target, costs_to_target = get_path_to_target_hallway_node(c_node, target_order)
    path.extend(path_to_target)
    costs += costs_to_target

    if reverse_order:
        path.reverse()  # [A1, A2, .. H3] -> [H3, A4, .. A1] # cost stays the same

    c_node = path[-1]
    assert c_node.name is destination.name, "the last node in the path should be the destination"

    # path complete - now checking if the path is clear
    path.pop(0)  # remove the origin (since it should always be occupied)
    blocked = any(node.is_occupied() for node in path)
    if blocked:
        return False, costs
    return True, costs


def possible_moves(node: Node, game_map: list[Node]):
    moves: list[Move] = []

    if node.is_occupied() is False:  # here is nothing that can be moved so all of this is sensless
        return moves

    for target in game_map:
        # 1. allowed are only moves from room<->hallway
        #    (to move into another room it will allways cross the hallway)
        if node.is_hallway and target.is_hallway or node.is_room and target.is_room:
            continue

        # 2. don't move somewhere where someone is already in
        if target.is_occupied():
            continue

        # 3. if room is done you can't move away from it
        #    done: if the occupaiers bellow are home and you are home too
        if node.is_room and node.type == node.get_occupier_type() and is_home_bellow_node_clear(node):
            continue

        # 4. if a lower spot in the room is free you cant move to a higher spot
        #    also if some other "wrong" types are in the home bellow you cant move to the room
        if target.is_room and can_move_to_home_spot(node, target) is False:
            continue

        # 5. don't pass through an occupied node
        # this is the hardest part ... maybe we can look at the map as somewhat linear? - should be easy...
        # but I already did the graph thingy .... uff..
        ok, cost = can_move_to(node, target)
        if not ok:
            continue

        # all rules are passed so we can add this move to the list
        moves.append(Move(node, target, cost))

    return moves


def play(game_map: Tuple[Node]):
    """
    Returns the minimum cost to complete the game from the provided state in game_map
    """
    input_hash = hash(game_map)  # find entry in the dict and return it's cost
    if input_hash in play_dict_cache:
        return play_dict_cache[input_hash]

    if is_won(game_map):  # base case (cost from this state is 0)
        return 0

    min_cost = inf

    for node in game_map:
        moves = possible_moves(node, game_map)
        for move in moves:  # for the current game_map
            cost = move.cost * node.get_occupier_cost_multiplier()

            # make the move
            node.move(move.target)

            cost += play(game_map)
            if cost < min_cost:
                min_cost = cost

            move.target.move(node)

    play_dict_cache[input_hash] = min_cost
    return min_cost


start = time.time()
results = play(game_map)

print("Answer 2:", results)
end = time.time()
print(f"took {end - start:.3}s")
