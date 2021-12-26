# %%
# #############
# #...........#
# ###D#B#C#C###
#   #D#C#B#A#
#   #D#B#A#C#
#   #D#A#B#A#
#   #########


# %% Indexing
# #############
# #01.6.3.4.56#
# ###2#7#9#a###
#   #3#8#d#e#
#   #4#9#h#i#
#   #5#a#l#m#
#   #########


# Idea - model the map as a graph
#      - each node is a space on which a amphipod can stay
#      - each edge is a connection between two nodes
#      - each node has a list of edges
#      - each edge has a cost (multiplier)
#      - each node has an occupacion status which consists of a name an a cost
#      - Connections are bidirectional
#      - A node has a move function which puts the occupacion status of the node
#        to the occupacion status of the next node and clears it's
#        own occupacion status and returns the cost of the move

from icecream import ic
from dataclasses import dataclass
from typing import List, Tuple
from functools import lru_cache
import copy

ic("")


class Edge:
    def __init__(self, source: "Node", target: "Node", cost: int = -1):
        self.source = source
        self.target = target
        self.cost = cost

    def __repr__(self):
        return f"{self.source.name} -> {self.target.name}"

    # equal checks for lists
    def __eq__(self, other):
        return (
            self.source == other.source
            and self.target == other.target
            or self.source == other.target
            and self.target == other.source
        )


cost_dict = {"A": 1, "B": 10, "C": 100, "D": 1000}


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


def check_win(game_map: list[Node]):
    for node in game_map:
        if node.name.startswith("H"):
            if node.occupation is not None:
                return False  # hallways have to be clear

        roomtype = node.name[0]  # A, B, C, D
        if node.occupation is None:
            return False  # rooms have to be filled

        occupiertype = node.occupation[0]  # A, B, C, D
        if roomtype != occupiertype:
            return False  # rooms have to be filled with the same type

    return True  # all rooms are filled with the corresponding type


# fmt: off
# Create Rooms
# A1 = Node("A1") ; B1 = Node("B1") ; C1 = Node("C1") ; D1 = Node("D1")
# A2 = Node("A2") ; B2 = Node("B2") ; C2 = Node("C2") ; D2 = Node("D2")
A3 = Node("A3") ; B3 = Node("B3") ; C3 = Node("C3") ; D3 = Node("D3")
A4 = Node("A4") ; B4 = Node("B4") ; C4 = Node("C4") ; D4 = Node("D4")

# Create Hallways
H1 = Node("H1") ; H2 = Node("H2") ; H3 = Node("H3") ; H4 = Node("H4") ; H5 = Node("H5") ; H6 = Node("H6") ; H7 = Node("H7")

# Connect the Rooms themselves # 1 is the cost
# A1.connect(A2, 1) ; B1.connect(B2, 1) ; C1.connect(C2, 1) ; D1.connect(D2, 1)
# A2.connect(A3, 1) ; B2.connect(B3, 1) ; C2.connect(C3, 1) ; D2.connect(D3, 1)
A3.connect(A4, 1) ; B3.connect(B4, 1) ; C3.connect(C4, 1) ; D3.connect(D4, 1)

# Connect the Hallways
H1.connect(H2, 1) ; H2.connect(H3, 2) ;H3.connect(H4, 2); H4.connect(H5, 2) ;H5.connect(H6, 2); H6.connect(H7, 1)
# Connect the Hallways to the Rooms
A4.connect(H2, 2) ; A4.connect(H3, 2) ; B4.connect(H3, 2) ; B4.connect(H4, 2) ; C4.connect(H4, 2) ; C4.connect(H5, 2) ; D4.connect(H5, 2) ; D4.connect(H6, 2)

# fill the nodes with their occupacion status
# A4.occupy("D") ; B4.occupy("B") ; C4.occupy("C") ; D4.occupy("C")
# A3.occupy("D") ; B3.occupy("C") ; C3.occupy("B") ; D3.occupy("A")
# A2.occupy("D") ; B2.occupy("B") ; C2.occupy("A") ; D2.occupy("C")
# A1.occupy("D") ; B1.occupy("A") ; C1.occupy("B") ; D1.occupy("A")

A4.occupy("B") ; B4.occupy("C") ; C4.occupy("B") ; D4.occupy("D")
A3.occupy("A") ; B3.occupy("D") ; C3.occupy("C") ; D3.occupy("A")
# A2.occupy("A") ; B2.occupy("B") ; C2.occupy("C") ; D2.occupy("D")
# A1.occupy("A") ; B1.occupy("B") ; C1.occupy("C") ; D1.occupy("D")

# A4.occupy("D") ; B4.occupy("B") ; C4.occupy("A") ; D4.occupy("C")
# A3.occupy("D") ; B3.occupy("C") ; C3.occupy("B") ; D3.occupy("A")
# A2.occupy("D") ; B2.occupy("B") ; C2.occupy("A") ; D2.occupy("C")
# A1.occupy("A") ; B1.occupy("B") ; C1.occupy("C") ; D1.occupy("D")

# fmt: on

# Add all the nodes to a list (game_map)
# game_map = [A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, D4, H1, H2, H3, H4, H5, H6, H7]
game_map = [A3, A4, B3, B4, C3, C4, D3, D4, H1, H2, H3, H4, H5, H6, H7]

# for all nodes try all possible moves
# for all possible games (all possible moves) try to find the best move

# to play all games
# we need to find all moves for the current game status
# then we save the game status and the moves
# then we play the moves resulting in the next game statuses
# part of the game status is the total cost
# then we repeat the process until we have no moves left or a win is found


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

    # print(
    #     f"{'#'* 13}\n"
    #     f"#{Hh[0]}{Hh[1]} {Hh[2]} {Hh[3]} {Hh[4]} {Hh[5]}{Hh[6]}#\n"
    #     f"###{Ah[3]}#{Bh[3]}#{Ch[3]}#{Dh[3]}###\n"
    #     f"  #{Ah[2]}#{Bh[2]}#{Ch[2]}#{Dh[2]}#  \n"
    #     f"  #{Ah[1]}#{Bh[1]}#{Ch[1]}#{Dh[1]}#  \n"
    #     f"  #{Ah[0]}#{Bh[0]}#{Ch[0]}#{Dh[0]}#  \n"
    #     f"  {'#'*9}  \n"
    # )

    print(
        f"{'#'* 13}\n"
        f"#{Hh[0]}{Hh[1]} {Hh[2]} {Hh[3]} {Hh[4]} {Hh[5]}{Hh[6]}#\n"
        f"###{Ah[1]}#{Bh[1]}#{Ch[1]}#{Dh[1]}###\n"
        f"  #{Ah[0]}#{Bh[0]}#{Ch[0]}#{Dh[0]}#  \n"
        f"  {'#'*9}  \n"
    )


# %% Test get_connected_nodes_of_same_type
assert set(get_connected_nodes_of_same_type(A1)) == {A1, A2, A3, A4}
assert set(get_connected_nodes_of_same_type(A2)) == {A1, A2, A3, A4}
assert set(get_connected_nodes_of_same_type(A3)) == {A1, A2, A3, A4}
assert set(get_connected_nodes_of_same_type(A4)) == {A1, A2, A3, A4}

assert set(get_connected_nodes_of_same_type(B1)) == {B1, B2, B3, B4}
assert set(get_connected_nodes_of_same_type(B2)) == {B1, B2, B3, B4}
assert set(get_connected_nodes_of_same_type(B3)) == {B1, B2, B3, B4}
assert set(get_connected_nodes_of_same_type(B4)) == {B1, B2, B3, B4}

assert set(get_connected_nodes_of_same_type(C1)) == {C1, C2, C3, C4}
assert set(get_connected_nodes_of_same_type(C2)) == {C1, C2, C3, C4}
assert set(get_connected_nodes_of_same_type(C3)) == {C1, C2, C3, C4}
assert set(get_connected_nodes_of_same_type(C4)) == {C1, C2, C3, C4}

assert set(get_connected_nodes_of_same_type(D1)) == {D1, D2, D3, D4}
assert set(get_connected_nodes_of_same_type(D2)) == {D1, D2, D3, D4}
assert set(get_connected_nodes_of_same_type(D3)) == {D1, D2, D3, D4}
assert set(get_connected_nodes_of_same_type(D4)) == {D1, D2, D3, D4}

assert set(get_connected_nodes_of_same_type(H1)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H2)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H3)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H4)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H5)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H6)) == {H1, H2, H3, H4, H5, H6, H7}
assert set(get_connected_nodes_of_same_type(H7)) == {H1, H2, H3, H4, H5, H6, H7}


# Test is_won (also uses connect and disconnect... :/ )
temp_home = [Node("X1"), Node("X2"), Node("X3"), Node("X4")]
temp_home[0].connect(temp_home[1], 1)
temp_home[1].connect(temp_home[2], 1)
temp_home[2].connect(temp_home[3], 1)
temp_home[2].connect(H2, 2)
assert is_won([H1, H2, H3, H4, H5, H6, H7, temp_home[2]]) is True
temp_home[2].disconnect(H2)

assert Edge(temp_home[2], H2) not in H2.edges

# Test is_hallway_clear
temp_hallway = [Node("H1"), Node("H2"), Node("H3"), Node("H4")]
temp_hallway[0].connect(temp_hallway[1], 1)
temp_hallway[1].connect(temp_hallway[2], 1)
temp_hallway[2].connect(temp_hallway[3], 1)

assert is_hallway_clear(temp_hallway) is True

# sanity checks
# game is not allready won?
assert is_won(game_map) is False

# hallway should be clear
assert is_hallway_clear(game_map) is True

# not all homes should be clear
assert not all(is_this_home_clear(node) for node in game_map)
# %%

# Print the map
print_map(game_map)

# dataclass for move which is a tuple of (target_node:Node, start_node:Node)
@dataclass
class Move:
    origin: Node
    target: Node
    cost: int


# the game state is the current cost and the current graph with all its nodes
# save the state as some kind of dict or something with state as key and cost as value
# or something like that


def is_home_bellow_node_clear(node: Node):
    """
    returns true if all home nodes below the current home node are clear or
    allready filled with a home node
    """
    assert node.is_room
    siblings = get_connected_nodes_of_same_type(node)
    for sibling in siblings:
        if sibling.order > node.order:
            continue  # we only check the siblings below the current node

        assert sibling.is_occupied()
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
        path.reverse()  # [A1, A2, .. H3] -> [H3, A4, .. A1] # cost shoud be the same

    c_node = path[-1]
    assert c_node.name is destination.name, "the last node in the path should be the destination"

    ###################################
    # path complete
    # now checking if the path is clear
    # remove the origin since this is where we started, so it is always occupied
    path.pop(0)  # remove the origin (we are there so it is always occupied)
    blocked = any(node.is_occupied() for node in path)
    if blocked:
        return False, costs
    return True, costs


# TODO does the lru_cache help? - not sure if here same states are encountered
# I think there are no same states in the game - so it should not help
# (it should even worsen the performance) - but we should test it
def possible_moves(node: Node, game_map: list[Node]):  # returns a list of all possible moves from a node
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
        if node.is_room and is_home_bellow_node_clear(node):
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


## %%
print_map(game_map)

## %%
# find the cheapest winning game:
# try to play for all nodes all possible moves
# and for the resulting game state (after the move is made) repeat unitl no moves are possible
# for the games that result in a winning state we can save the cost
# and the lowest cost is the Solution

# %%
# game_map_backup[1].edges[0].target.occupation
# game_map_backup[1].edges[0].target.occupation = None
# game_map[1].edges[0].target.occupation

game_depth = 0

# the move into the house does not work


def play(game_map: list[Node], cost: int = 0) -> list[Tuple[int, bool]]:
    global game_depth
    game_depth += 1

    if is_won(game_map):  # Base case
        # print("Won", cost)
        game_depth -= 1
        return [(cost, True)]

    game_map_backup = copy.deepcopy(game_map)  # TODO does this work? - It could cause problems...
    results = []

    if game_depth >= 30:
        game_depth -= 1
        ic("Too deep")
        return results

    # node_count = len(game_map)
    game_map_length = len(game_map)

    if game_depth <= 2:
        print_map(game_map)

    for i in range(game_map_length):  # for each node
        # for node in game_map_backup:
        node = game_map[i]

        moves = possible_moves(node, game_map)  # hier kommt eine falsche referenz zurück
        for move in moves:  # for the current game_map

            # make the move
            # HACK to find the target in the game_map
            target_from_game_map = next((x for x in game_map if x.name == move.target.name), None)
            move.target = target_from_game_map

            node.move(target_from_game_map)
            cost += move.cost * target_from_game_map.get_occupier_cost_multiplier()
            results.extend(play(game_map, cost))
            # undo the move (maybe really only undo the move and not the whole game)
            # so that the next move can be made on the original game_map

            # TODO: maybe restore costs aswell?
            game_map = copy.deepcopy(game_map_backup)  # --> game_map ist nur nichtmehr gleich der node
            node = game_map[i]  # damit bleibt die ref erhalten aber das C in der target node ist verschwunden

    # ich will mir die moves ansehen und schauen ob die alle passen
    # beim ersten wieder aus der recursion zurückkommen passiert etwas schlechtes
    # da moves plötzlich nicht mehr die richtigen enthält und node.move dann auch nichtmehr die gamemap referenz
    # hat.. (der move ändert nichts an der game_map)
    game_depth -= 1
    # ic("Dead end")
    return results


results = play(game_map)
print(results)


# # %%

# can_move_to(origin=B4, destination=H1)

# # %%
# possible_moves(node=B4, game_map=game_map)


# # %%

# # A4.occupation = None
# H1.occupy("A")
# can_move_to(origin=H1, destination=A4)

# # %%
# can_move_to(origin=H1, destination=A3)
# # A3.occupation = None

# %%
