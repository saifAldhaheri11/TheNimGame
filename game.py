# This file contains the game rules and terminal version
from player import get_player_move
import ai


# Starting object limits
INITIAL_OBJECTS = 15
MIN_OBJECTS = 5
MAX_OBJECTS = 30


# Initialize the game
def initialize_game(starting_objects=INITIAL_OBJECTS):
    if (
        type(starting_objects) is not int
        or not MIN_OBJECTS <= starting_objects <= MAX_OBJECTS
    ):
        raise ValueError("Choose between 5 and 30 matches")

    return starting_objects


# Main menu for the terminal version
def start_game():
    starting_objects = INITIAL_OBJECTS

    while True:
        print("\nWelcome to the Nim Game!")
        print("1. Start Game")
        print("2. Game Rules")
        print("3. Settings")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nSelect Difficulty Level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            print("4. Extreme")

            levels = {
                "1": "Easy",
                "2": "Medium",
                "3": "Hard",
                "4": "Extreme"
            }

            while True:
                difficulty = input("Enter your choice: ")

                if difficulty in levels:
                    print(
                        f"You have chosen "
                        f"{levels[difficulty]} level."
                    )
                    break

                print("Invalid difficulty. Choose 1, 2, 3, or 4.")

            remaining_objects = initialize_game(starting_objects)

            print(
                f"Starting game with {remaining_objects} objects."
            )

            first_player = select_first_player()

            play_game(
                remaining_objects,
                first_player,
                difficulty
            )

        elif choice == "2":
            print("\nGame Rules:")
            print("1. The starting number is 15.")
            print("2. Choose 5 to 30 objects in Settings.")
            print("3. Players remove 1, 2, or 3 objects per turn.")
            print("4. You cannot remove more objects than remain.")
            print("5. Whoever removes the last object loses.")

        elif choice == "3":
            starting_objects = settings(starting_objects)

        elif choice == "4":
            print("Exiting the game. Goodbye!")
            break

        else:
            print("Invalid choice. Choose 1, 2, 3, or 4.")


# Settings for the terminal version
def settings(starting_objects):
    while True:
        print("\nSettings")
        print(f"Current number of objects: {starting_objects}")
        print("1. Change number of objects")
        print("2. Reset to 15")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                user_input = input(
                    "Enter the number of objects (5-30): "
                )

                try:
                    new_objects = int(user_input)
                    starting_objects = initialize_game(new_objects)

                    print(
                        f"Number of objects changed to "
                        f"{starting_objects}."
                    )
                    break

                except ValueError:
                    print("Enter a whole number from 5 to 30.")

        elif choice == "2":
            starting_objects = INITIAL_OBJECTS
            print("Number of objects reset to 15.")

        elif choice == "3":
            return starting_objects

        else:
            print("Invalid choice. Choose 1, 2, or 3.")


# Select who plays first
def select_first_player():
    while True:
        print("\nWho should play first?")
        print("1. Player")
        print("2. AI")

        choice = input("Enter your choice: ")

        if choice == "1":
            return "Player"

        elif choice == "2":
            return "AI"

        else:
            print("Invalid choice. Choose 1 or 2.")


# Get valid moves
def get_valid_moves(remaining_objects):
    valid_moves = []

    for move in range(1, 4):
        if move <= remaining_objects:
            valid_moves.append(move)

    return valid_moves


# Remove objects
def remove_objects(remaining_objects, move):
    if move not in get_valid_moves(remaining_objects):
        raise ValueError("Invalid move")

    return remaining_objects - move


# Check whether the game has ended
def is_game_over(remaining_objects):
    return remaining_objects == 0


# Determine the winner
def get_winner(last_player):
    if last_player == "Player":
        return "AI"

    elif last_player == "AI":
        return "Player"

    else:
        raise ValueError("Invalid player")


# Main game loop for the terminal version
def play_game(remaining_objects, first_player, difficulty):
    current_player = first_player
    first_move = True

    while not is_game_over(remaining_objects):
        print(f"\nObjects remaining: {remaining_objects}")

        if current_player == "Player":
            move = get_player_move(remaining_objects)
            print(f"Player removed {move} object(s).")

        else:
            # The AI opening move is random
            if first_move:
                move = ai.random_ai(remaining_objects)

            elif difficulty == "1":
                move = ai.random_ai(remaining_objects)

            elif difficulty == "2":
                move = ai.greedy_ai(remaining_objects)

            elif difficulty == "3":
                move = ai.minimax_ai(
                    remaining_objects,
                    depth=3
                )

            elif difficulty == "4":
                move = ai.alpha_beta_ai(
                    remaining_objects,
                    depth=4
                )

            else:
                print("Invalid difficulty.")
                return

            print(f"AI removed {move} object(s).")

        remaining_objects = remove_objects(
            remaining_objects,
            move
        )

        first_move = False

        if is_game_over(remaining_objects):
            winner = get_winner(current_player)

            print("\nGame Over!")
            print(f"{current_player} removed the last object.")
            print(f"Winner: {winner}")
            break

        # Switch players
        if current_player == "Player":
            current_player = "AI"
        else:
            current_player = "Player"


# Run the terminal version
if __name__ == "__main__":
    start_game()