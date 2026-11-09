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
def evaluate(remaining_objects, maximizing):
    if remaining_objects % 4 == 1:
        return -1 if maximizing else 1

    return 1 if maximizing else -1

def minimax(remaining_objects, depth, maximizing):

    # Check if the game is over
    if remaining_objects == 0:
        return 1 if maximizing else -1

    # Check if depth limit is reached
    if depth == 0:
        return evaluate(remaining_objects, maximizing)

    # AI's turn (MAX)
    if maximizing:
        best_score = float('-inf')

        for move in range(1, min(3, remaining_objects) + 1):
            score = minimax(
                remaining_objects - move,
                depth - 1,
                False
            )

            best_score = max(best_score, score)

        return best_score

    # Human's turn (MIN)
    else:
        best_score = float('inf')

        for move in range(1, min(3, remaining_objects) + 1):
            score = minimax(
                remaining_objects - move,
                depth - 1,
                True
            )

            best_score = min(best_score, score)

        return best_score

def minimax_ai(remaining_objects, depth=3):
    best_score = float('-inf')
    best_move = 1

    for move in range(1, min(3, remaining_objects) + 1):
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

def alpha_beta(remaining_objects, depth, alpha, beta, maximizing):

    # Check if the game is over
    if remaining_objects == 0:
        return 1 if maximizing else -1

    # Check if depth limit is reached
    if depth == 0:
        return evaluate(remaining_objects, maximizing)

    # AI's turn (MAX)
    if maximizing:
        best_score = float('-inf')

        for move in range(1, min(3, remaining_objects) + 1):
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

        return best_score

    # Human's turn (MIN)
    else:
        best_score = float('inf')

        for move in range(1, min(3, remaining_objects) + 1):
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

        return best_score


def alpha_beta_ai(remaining_objects, depth=6):
    best_score = float('-inf')
    best_move = 1

    alpha = float('-inf')
    beta = float('inf')

    for move in range(1, min(3, remaining_objects) + 1):
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
