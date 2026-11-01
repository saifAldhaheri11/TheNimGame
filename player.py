#this is the human player file

def get_player_move(remaining_objects):
    while True:
        print(f"\nObjects remaining: {remaining_objects}")

        choice = input("How many objects do you want to remove (1, 2, or 3)? ")

        try:
            move = int(choice)

            if 1 <= move <= min(3, remaining_objects):
                return move

            print("Invalid move. Choose a valid number of objects.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")
