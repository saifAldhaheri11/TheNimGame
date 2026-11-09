# This file finds the best path for the player and scores each game
from functools import lru_cache

import game


# Points for each difficulty: harder AI, bigger multiplier
DIFFICULTY_MULTIPLIER = {
    "Easy": 1.0,
    "Medium": 1.5,
    "Hard": 2.0,
    "Extreme": 3.0
}

BEST_MOVE_POINTS = 100   # move on the best path
OTHER_MOVE_POINTS = 20   # any other legal move
WIN_BONUS = 500
SPEED_BONUS = 50         # full bonus for an instant move
SPEED_LIMIT = 10         # seconds until the speed bonus reaches 0


# Best path algorithm: full-depth minimax that also counts moves.
# Returns (wins, moves_left) for the player about to move,
# assuming both sides then play perfectly.
#  - A winning player wants to win in as FEW moves as possible.
#  - A losing player wants to survive as MANY moves as possible,
#    which gives the opponent the most chances to make a mistake.
# lru_cache remembers every pile size already solved (memoization).
@lru_cache(maxsize=None)
def solve(remaining):
    # The previous player took the last match, so the mover wins
    if remaining == 0:
        return True, 0

    best = None

    for move in game.get_valid_moves(remaining):
        opponent_wins, length = solve(remaining - move)
        result = (not opponent_wins, length + 1)

        if best is None or better(result, best):
            best = result

    return best


# Is result a better than result b for the player choosing?
def better(a, b):
    a_wins, a_length = a
    b_wins, b_length = b

    if a_wins != b_wins:
        return a_wins

    if a_wins:
        return a_length < b_length  # win faster

    return a_length > b_length      # lose slower


# All moves that are on the best path from this pile size
def best_moves(remaining):
    target = solve(remaining)
    moves = []

    for move in game.get_valid_moves(remaining):
        opponent_wins, length = solve(remaining - move)

        if (not opponent_wins, length + 1) == target:
            moves.append(move)

    return moves


# The whole best path if both sides play perfectly from here
def best_path(remaining):
    path = []

    while remaining > 0:
        move = best_moves(remaining)[0]
        path.append(move)
        remaining -= move

    return path


# Score for one player move
def move_points(remaining_before, move, seconds):
    on_path = move in best_moves(remaining_before)

    points = BEST_MOVE_POINTS if on_path else OTHER_MOVE_POINTS

    speed = max(0.0, 1 - seconds / SPEED_LIMIT)
    points += round(SPEED_BONUS * speed)

    return points, on_path


class ScoreKeeper:

    def __init__(self, difficulty):
        self.multiplier = DIFFICULTY_MULTIPLIER[difficulty]
        self.move_total = 0
        self.best_count = 0
        self.player_moves = 0
        self.won = False

    def add_move(self, remaining_before, move, seconds):
        points, on_path = move_points(
            remaining_before, move, seconds
        )

        self.move_total += points
        self.player_moves += 1

        if on_path:
            self.best_count += 1

        return points, on_path

    def finish(self, player_won):
        self.won = player_won

    def total(self):
        base = self.move_total

        if self.won:
            base += WIN_BONUS

        return round(base * self.multiplier)
