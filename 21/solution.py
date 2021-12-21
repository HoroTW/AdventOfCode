# %%
from itertools import cycle, product
from functools import lru_cache, reduce

PLAYER1, PLAYER2 = 0, 1


def get_dice(min_side_val, max_side_val):
    iterable = range(min_side_val, max_side_val + 1)
    for roll in cycle(iterable):
        yield roll


def change_player(player_id):
    return player_id ^ 1  # bitwise XOR


def play(p1_pos, p2_pos, dice, score_limit):
    rolls, player_id, player_scores = 0, 0, [0, 0]
    player_pos = [p1_pos, p2_pos]

    while all(s < score_limit for s in player_scores):
        player_pos[player_id] = (player_pos[player_id] + sum(next(dice) for _ in range(3)) - 1) % 10 + 1
        player_scores[player_id] += player_pos[player_id]
        rolls += 3
        player_id = change_player(player_id)

    return rolls, player_scores


rolls, player_scores = play(4, 8, get_dice(1, 100), 1000)
print("Answer 1", min(player_scores) * rolls)

# %%
# 27^21 = 1.14E30
# if scores and positions and current player are the same .... then I can group them together
# there are only 10 positions and 21 scores but for each player... and also 2 posibilities for the curent player
# so the posible states are 10*10*21*21*2 = 88_200

# STATE = (player_pos, player_score, player_id)
# I could also store the player id implicit by the position of the arguments
# STATE = (cur_player_pos, cur_player_score, other_player_pos, other_player_score)

# A function should return the number of wins for each player

# ALL_POSSIBLE_DICE_SUMS = list(map(sum, product([1, 2, 3], repeat=3)))
# ALL_POSSIBLE_DICE_SUMS = list(map(sum, product(range(1, 4), repeat=3)))
# ALL_POSSIBLE_DICE_SUMS = list(map(sum, product([1, 2, 3], [1, 2, 3], [1, 2, 3])))

# print(ALL_POSSIBLE_DICE_SUMS)
# [3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9] len == 27

# since performance matters I should use tuple instead of list where I can
# and I should also check if `product` slows me down too much... (it's slow)

# Pre calc ALL possible dice sums because it's faster that way
ALL_POSSIBLE_DICE_SUMS = tuple(map(sum, product([1, 2, 3], repeat=3)))


FUNC_DICT = {}
HIT_MISS_COUNT = [0, 0]

def dim_play(positions, scores, player_id):
    if (positions, scores, player_id) in FUNC_DICT:
        HIT_MISS_COUNT[0] += 1
        return FUNC_DICT[(positions, scores, player_id)]
    HIT_MISS_COUNT[1] += 1

    if scores[PLAYER1] >= 21:  # base cases
        return (1, 0)  # one win for PLAYER1
    if scores[PLAYER2] >= 21:
        return (0, 1)  # one win for PLAYER2

    wins = [0, 0]

    for roll in ALL_POSSIBLE_DICE_SUMS:
        # One turn for each roll
        iter_positions, iter_scores = list(positions), list(scores)
        # Calc the new position and score
        iter_positions[player_id] = (positions[player_id] + roll - 1) % 10 + 1
        iter_scores[player_id] = scores[player_id] + iter_positions[player_id]

        # Other players turn
        it_p1_w, it_p2_w = dim_play(tuple(iter_positions), tuple(iter_scores), change_player(player_id))

        # Update the wins for the players:
        wins = [wins[PLAYER1] + it_p1_w, wins[PLAYER2] + it_p2_w]

    FUNC_DICT[(positions, scores, player_id)] = wins
    return wins


wins = dim_play((4, 10), (0, 0), PLAYER1)
print("Answer 2:", max(wins))
print()
print(f"Hit count: {HIT_MISS_COUNT[0]} Miss count: {HIT_MISS_COUNT[1]}")
print(f"Hit rate: {HIT_MISS_COUNT[0] / (HIT_MISS_COUNT[0] + HIT_MISS_COUNT[1]) * 100 :0.2f}%")
print(f"Entrys in the function call dictionary: {len(FUNC_DICT)}")
print(f"Games that were cached by using dynamic programming {sum(map(sum, FUNC_DICT.values()))}")
