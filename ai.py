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



#extreme level algorithm
#AI uses alpha-beta pruning algorithm.