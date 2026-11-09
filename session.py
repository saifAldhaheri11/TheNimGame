# This file manages the current game
import ai
import game

DIFFICULTIES = ("Easy", "Medium", "Hard", "Extreme")

class GameSession:

    # Initialize the game
    def __init__(
        self,
        difficulty="Medium",
        first_player="Player",
        starting_objects=15
    ):
        if difficulty not in DIFFICULTIES:
            raise ValueError("Invalid difficulty")

        if first_player not in ("Player", "AI"):
            raise ValueError("Invalid starting player")

        self.difficulty = difficulty
        self.first_player = first_player
        self.current_player = first_player

        self.remaining = game.initialize_game(starting_objects)
        self.starting_objects = self.remaining

        # Give each match a number
        self.matches = list(range(self.remaining))

        self.moves_played = 0
        self.winner = None
        self.last_player = None

    # Get a move from the existing AI algorithms
    def choose_ai_move(self):
        if self.winner or self.current_player != "AI":
            raise ValueError("It is not the AI's turn")

        # The AI opening move is always random
        if self.moves_played == 0 or self.difficulty == "Easy":
            return ai.random_ai(self.remaining)

        if self.difficulty == "Medium":
            return ai.greedy_ai(self.remaining)

        if self.difficulty == "Hard":
            return ai.minimax_ai(self.remaining, depth=3)

        return ai.alpha_beta_ai(self.remaining, depth=4)

    # Remove the selected matches and switch turns
    def remove(self, match_ids, player):
        ids = list(match_ids)

        if self.winner or player != self.current_player:
            raise ValueError("It is not this player's turn")

        if (
            len(set(ids)) != len(ids)
            or not set(ids).issubset(self.matches)
        ):
            raise ValueError("Select available matches only")

        remaining = game.remove_objects(
            self.remaining,
            len(ids)
        )

        self.matches = [
            match
            for match in self.matches
            if match not in ids
        ]

        self.remaining = remaining
        self.moves_played += 1
        self.last_player = player

        if game.is_game_over(remaining):
            self.winner = game.get_winner(player)

        elif player == "Player":
            self.current_player = "AI"

        else:
            self.current_player = "Player"