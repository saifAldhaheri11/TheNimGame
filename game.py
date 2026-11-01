
# This is the game file
from player import get_player_move
import ai


INITIAL_OBJECTS = 15


# Initialize the game
def initialize_game(starting_objects=INITIAL_OBJECTS):
    return starting_objects


# Main menu
def start_game():
    starting_objects = INITIAL_OBJECTS

    while True:
        print("\nWelcome to the Nim Game!")
        print("1. Start Game")
        print("2. Game Rules")
        print("3. Settings")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nSelect Difficulty Level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            print("4. Extreme")

            levels = {
                '1': 'Easy',
                '2': 'Medium',
                '3': 'Hard',
                '4': 'Extreme'
            }

            while True:
                difficulty = input("Enter your choice: ")

                if difficulty in levels:
                    print(f"You have chosen {levels[difficulty]} level.")
                    break
                else:
                    print("Invalid difficulty. Please choose 1, 2, 3, or 4.")

            remaining_objects = initialize_game(starting_objects)
            print(f"Starting game with {remaining_objects} objects.")

            # Starting player selection and game loop
            first_player = select_first_player()
            print(f"First player: {first_player}")
            play_game(remaining_objects, first_player, difficulty)
            # will be implemented later.

        elif choice == '2':
            print("\nGame Rules:")
            print("1. The game starts with 15 objects by default.")
            print("2. The number of objects can be changed in Settings.")
            print("3. Players take turns removing 1, 2, or 3 objects.")
            print("4. A player cannot remove more objects than remain.")
            print("5. The player who removes the last object loses.")

        elif choice == '3':
            starting_objects = settings(starting_objects)

        elif choice == '4':
            print("Exiting the game. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose 1, 2, 3, or 4.")


# Settings menu
def settings(starting_objects):
    while True:
        print("\nSettings")
        print(f"Current number of objects: {starting_objects}")
        print("1. Change number of objects")
        print("2. Reset to default (15)")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                user_input = input("Enter the new number of objects: ")

                try:
                    new_objects = int(user_input)

                    if new_objects > 0:
                        starting_objects = new_objects
                        print(f"Number of objects changed to {starting_objects}.")
                        break
                    else:
                        print("Please enter a positive number.")

                except ValueError:
                    print("Invalid input. Please enter a whole number.")

        elif choice == '2':
            starting_objects = INITIAL_OBJECTS
            print("Number of objects reset to 15.")

        elif choice == '3':
            return starting_objects

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


# Select who plays first
def select_first_player():
    while True:
        print("\nWho should play first?")
        print("1. Player")
        print("2. AI")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("You will play first.")
            return "Player"

        elif choice == '2':
            print("The AI will play first.")
            return "Player"

        else:
            print("Invalid choice. Please choose 1 or 2.")

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


# Main game loop
def play_game(remaining_objects, first_player, difficulty):
    current_player = first_player
    first_move = True

    while not is_game_over(remaining_objects):
        print(f"\nObjects remaining: {remaining_objects}")

        if current_player == "Player":
            move = get_player_move(remaining_objects)
            print(f"Player removed {move} object(s).")

        else:
            if first_move:
                # AI's first move is random if AI starts
                move = ai.random_ai(remaining_objects)

            elif difficulty == '1':
                # Easy: Random
                move = ai.random_ai(remaining_objects)

            elif difficulty == '2':
                # Medium: Greedy
                move = ai.greedy_ai(remaining_objects)

            else:
                # Hard and Extreme are not implemented yet
                print("This difficulty is not available yet.")
                return

            print(f"AI removed {move} object(s).")

        remaining_objects = remove_objects(remaining_objects, move)
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

# Run the program
if __name__ == "__main__":
    start_game()
