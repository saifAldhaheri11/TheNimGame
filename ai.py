#this is the ai player file
import random

#easy level algorithm 
#AI chooses randomly 1,2, or 3 objects
def random_ai(remaining_objects):
    valid_moves = list(range(1, min(3, remaining_objects) + 1))
    return random.choice(valid_moves)



#medium level algorith
#AI uses greedy algorithm, takes maximum number of objects possible from the pile
def greedy_ai(remaining_objects):
    if remaining_objects <= 0:
        raise ValueError("No objects remaining.")
    return min(3, remaining_objects)


#hard level algorithm
#AI uses minimax with limited depth search

# Counts how many game states the last search visited.
# Useful for comparing the algorithms in the report.
nodes_explored = 0


def get_moves(remaining_objects):
    return list(range(1, min(3, remaining_objects) + 1))


def evaluate(remaining_objects, maximizing):
    if remaining_objects % 4 == 1:
        return -1 if maximizing else 1

    return 1 if maximizing else -1


# Optimization 1: memoization (transposition table)
# The same pile size is reached through many different move orders
# (for example 15 -> 12 by taking 1+2, 2+1 or 3). Instead of searching
# that state again, we remember its score the first time.
# Once depth >= remaining objects, the depth limit can never be reached,
# so every such search gives the same exact result and can share one key.
def cache_key(remaining_objects, depth, maximizing):
    return (remaining_objects, min(depth, remaining_objects), maximizing)


minimax_cache = {}


def minimax(remaining_objects, depth, maximizing):
    global nodes_explored
    nodes_explored += 1

    # Check if the game is over
    if remaining_objects == 0:
        return 1 if maximizing else -1

    # Check if depth limit is reached
    if depth == 0:
        return evaluate(remaining_objects, maximizing)

    # Reuse the score if this state was already searched
    key = cache_key(remaining_objects, depth, maximizing)
    if key in minimax_cache:
        return minimax_cache[key]

    # AI's turn (MAX)
    if maximizing:
        best_score = float('-inf')

        for move in get_moves(remaining_objects):
            score = minimax(
                remaining_objects - move,
                depth - 1,
                False
            )

            best_score = max(best_score, score)

    # Human's turn (MIN)
    else:
        best_score = float('inf')

        for move in get_moves(remaining_objects):
            score = minimax(
                remaining_objects - move,
                depth - 1,
                True
            )

            best_score = min(best_score, score)

    minimax_cache[key] = best_score
    return best_score


def minimax_ai(remaining_objects, depth=3):
    global nodes_explored
    nodes_explored = 0

    best_score = float('-inf')
    best_move = 1

    for move in get_moves(remaining_objects):
        score = minimax(
            remaining_objects - move,
            depth - 1,
            False
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


#extreme level algorithm
#AI uses alpha-beta pruning algorithm.
#It searches the whole game tree every turn: the depth is set to the
#number of objects left, which is the longest the game can still last.

# Optimization 2: move ordering
# Alpha-beta prunes the most when the best move is tried first.
# We try first the moves that leave the opponent in a losing position
# according to the heuristic (a pile where remaining % 4 == 1).
def ordered_moves(remaining_objects):
    moves = get_moves(remaining_objects)

    def looks_good(move):
        left = remaining_objects - move
        return left > 0 and left % 4 == 1

    return sorted(moves, key=looks_good, reverse=True)


# Optimization 1 again: a transposition table for alpha-beta.
# A pruned search only proves a bound, not an exact score, so we store
# a flag saying whether the saved score is EXACT, a LOWER bound or an
# UPPER bound, and only reuse it where that is safe.
EXACT = "exact"
LOWER = "lower"
UPPER = "upper"

alpha_beta_cache = {}


def alpha_beta(remaining_objects, depth, alpha, beta, maximizing):
    global nodes_explored
    nodes_explored += 1

    # Check if the game is over
    if remaining_objects == 0:
        return 1 if maximizing else -1

    # Check if depth limit is reached
    if depth == 0:
        return evaluate(remaining_objects, maximizing)

    # Look up the state in the table
    key = cache_key(remaining_objects, depth, maximizing)
    if key in alpha_beta_cache:
        saved_score, flag = alpha_beta_cache[key]

        if flag == EXACT:
            return saved_score
        if flag == LOWER:
            alpha = max(alpha, saved_score)
        else:
            beta = min(beta, saved_score)

        if alpha >= beta:
            return saved_score

    original_alpha = alpha
    original_beta = beta

    # AI's turn (MAX)
    if maximizing:
        best_score = float('-inf')

        for move in ordered_moves(remaining_objects):
            score = alpha_beta(
                remaining_objects - move,
                depth - 1,
                alpha,
                beta,
                False
            )

            best_score = max(best_score, score)

            # Update alpha
            alpha = max(alpha, best_score)

            # Prune if alpha >= beta
            if alpha >= beta:
                break

    # Human's turn (MIN)
    else:
        best_score = float('inf')

        for move in ordered_moves(remaining_objects):
            score = alpha_beta(
                remaining_objects - move,
                depth - 1,
                alpha,
                beta,
                True
            )

            best_score = min(best_score, score)

            # Update beta
            beta = min(beta, best_score)

            # Prune if alpha >= beta
            if alpha >= beta:
                break

    # Save the score with what kind of result it is
    if best_score <= original_alpha:
        flag = UPPER
    elif best_score >= original_beta:
        flag = LOWER
    else:
        flag = EXACT

    alpha_beta_cache[key] = (best_score, flag)
    return best_score


def alpha_beta_ai(remaining_objects, depth=None):
    global nodes_explored
    nodes_explored = 0

    # Full search: the game cannot last more moves than objects left
    if depth is None:
        depth = remaining_objects

    best_score = float('-inf')
    best_move = 1

    alpha = float('-inf')
    beta = float('inf')

    for move in ordered_moves(remaining_objects):
        score = alpha_beta(
            remaining_objects - move,
            depth - 1,
            alpha,
            beta,
            False
        )

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)

    return best_move


# Empty the tables, for example to measure a search from scratch
def clear_caches():
    minimax_cache.clear()
    alpha_beta_cache.clear()
