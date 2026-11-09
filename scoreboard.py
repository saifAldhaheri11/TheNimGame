# This file keeps the win/loss record and high score for each difficulty
import json
import os

from session import DIFFICULTIES

# Saved next to the code so the record survives restarts
SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "scoreboard.json"
)


class Scoreboard:

    def __init__(self, path=SCORE_FILE):
        self.path = path
        self.scores = self.empty()
        self.load()

    def empty(self):
        return {
            level: {"wins": 0, "losses": 0, "best": 0}
            for level in DIFFICULTIES
        }

    # Read the saved record, or start fresh if there is none
    def load(self):
        try:
            with open(self.path) as file:
                saved = json.load(file)

            for level in DIFFICULTIES:
                record = saved.get(level, {})

                for field in ("wins", "losses", "best"):
                    self.scores[level][field] = int(
                        record.get(field, 0)
                    )

        except (OSError, ValueError, AttributeError):
            self.scores = self.empty()

    def save(self):
        try:
            with open(self.path, "w") as file:
                json.dump(self.scores, file, indent=2)

        except OSError:
            pass  # The game still works if the file cannot be written

    # Record a finished game from the player's point of view.
    # Returns True when the score is a new high score.
    def record(self, difficulty, winner, score=0):
        record = self.scores[difficulty]

        if winner == "Player":
            record["wins"] += 1
        else:
            record["losses"] += 1

        new_best = score > record["best"]

        if new_best:
            record["best"] = score

        self.save()
        return new_best

    def reset(self):
        self.scores = self.empty()
        self.save()

    def totals(self):
        wins = sum(record["wins"] for record in self.scores.values())
        losses = sum(record["losses"] for record in self.scores.values())
        return wins, losses

    def best_overall(self):
        return max(record["best"] for record in self.scores.values())
