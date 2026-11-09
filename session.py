# This file manages the current game
import ai
import game


DIFFICULTIES = ("Easy", "Medium", "Hard", "Extreme")


class GameSession:

    # Initialize the game settings
    def __init__(self, difficulty="Medium", first_player="Player"):
        if difficulty not in DIFFICULTIES:
            raise ValueError("Invalid difficulty")

        if first_player not in ("Player", "AI"):
            raise ValueError("Invalid starting player")

        self.difficulty = difficulty
        self.first_player = first_player
        self.current_player = first_player

        self.remaining = game.initialize_game()

        # Give each match a number so it can be selected
        self.matches = list(range(self.remaining))

        self.moves_played = 0
        self.winner = None
        self.last_player = None

    # Get the AI move using the existing algorithms
    def choose_ai_move(self):
        if self.winner or self.current_player != "AI":
            raise ValueError("It is not the AI's turn")

        # The AI opening move is always random
        if self.moves_played == 0:
            return ai.random_ai(self.remaining)

        if self.difficulty == "Easy":
            return ai.random_ai(self.remaining)

        elif self.difficulty == "Medium":
            return ai.greedy_ai(self.remaining)

        elif self.difficulty == "Hard":
            return ai.minimax_ai(self.remaining, depth=3)

        elif self.difficulty == "Extreme":
            return ai.alpha_beta_ai(self.remaining, depth=4)

    # Remove the selected matches
    def remove(self, match_ids, player):
        selected_matches = list(match_ids)

        if self.winner or player != self.current_player:
            raise ValueError("It is not this player's turn")

        # Prevent duplicate or unavailable matches
        if len(set(selected_matches)) != len(selected_matches):
            raise ValueError("A match cannot be selected twice")

        if not set(selected_matches).issubset(self.matches):
            raise ValueError("Select available matches only")

        # Use the existing move validation
        remaining = game.remove_objects(
            self.remaining,
            len(selected_matches)
        )

        self.matches = [
            match
            for match in self.matches
            if match not in selected_matches
        ]

        self.remaining = remaining
        self.moves_played += 1
        self.last_player = player

        # Check the winner using the existing game rules
        if game.is_game_over(self.remaining):
            self.winner = game.get_winner(player)

        # Switch players
        elif player == "Player":
            self.current_player = "AI"

        else:
            self.current_player = "Player"