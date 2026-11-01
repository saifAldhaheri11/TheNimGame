#this is the game file

def start_game():
    print("Welcome to the Game!")
    print("Select")
    print("1. Start Game")
    print("2. Game Rules")
    print("3. Exit")
    
    if input("Enter the number corresponding to your choice: ") == '1':
        print("Select Difficulty Level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Extreme")
        difficulty = input("Enter the number corresponding to your choice: ")
        if difficulty == '1':
            print("You have chosen Easy level.")
            # Call the easy level AI function here
        elif difficulty == '2':
            print("You have chosen Medium level.")
            # Call the medium level AI function here
        elif difficulty == '3':
            print("You have chosen Hard level.")
            # Call the hard level AI function here
        elif difficulty == '4':
            print("You have chosen Extreme level.")
            # Call the extreme level AI function here
        else:
            print("Invalid choice. Please choose a valid option.")

        
    elif input("Enter the number corresponding to your choice: ") == '2':
        print("Game Rules:")
        print("1. The game is played with a pile of objects.")
        print("2. Players take turns to remove 1, 2, or 3 objects from the pile.")
        print("3. The player who removes the last object loses the game.")
    elif input("Enter the number corresponding to your choice: ") == '3':
        print("Exiting the game. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please choose a valid option.")

    