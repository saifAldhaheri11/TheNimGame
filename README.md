# Nim Game: Player vs AI

## Project Overview

This project is a digital implementation of the **Nim Game**, where a human player competes against an AI opponent.

The game starts with a single pile containing **15 objects**. The player and AI take turns removing objects from the pile. On each turn, a player may remove **1, 2, or 3 objects**.

The goal is to be the player who removes the **last object from the pile**.

The game includes three AI difficulty levels, each using a different algorithm.

---

## Game Rules

1. The game starts with **15 objects** in one pile.
2. The human player and AI take turns.
3. On each turn, the current player may remove:

   * 1 object
   * 2 objects
   * 3 objects
4. A player cannot remove more objects than are currently available.
5. The player who removes the **last object wins the game**.
6. The game ends when the number of remaining objects reaches `0`.

### Example

The game may progress as follows:

```text
Starting objects: 15

Player removes 2
Remaining objects: 13

AI removes 1
Remaining objects: 12

Player removes 3
Remaining objects: 9

AI removes 1
Remaining objects: 8

...
```

The game continues until one player removes the final object.

---

## AI Difficulty Levels

The game contains three AI difficulty levels:

### Easy: Random Algorithm

The Easy AI selects a valid move randomly.

It chooses between removing:

```text
1, 2, or 3 objects
```

as long as the selected number does not exceed the number of objects remaining.

The Easy AI does not analyze future moves or use a strategy to guarantee a win.

#### Algorithm

```text
Find all valid moves
        ↓
Randomly select one
        ↓
Remove the selected number of objects
```

---

### Medium: Minimax Algorithm

The Medium AI uses the **Minimax algorithm**.

Minimax analyzes possible future moves by constructing a game tree. The AI considers its possible actions and the possible responses of the human player.

Game states are evaluated based on whether they eventually result in an AI win or a player win.

For example:

```text
AI Win      = +1
Player Win  = -1
```

A simplified game tree may look like:

```text
              Current State
             /      |      \
         Take 1   Take 2   Take 3
           /         |         \
      Future      Future      Future
       States      States      States
```

The AI examines the possible outcomes and chooses the move that gives it the best result.

To keep the Medium difficulty less predictable than the Hard difficulty, the implementation may limit the Minimax search or occasionally allow the AI to select a non-optimal move.

---

### Hard: Optimal Mathematical Algorithm

The Hard AI uses the mathematical strategy for this version of Nim.

Since a player can remove between **1 and 3 objects**, the important number is:

```text
3 + 1 = 4
```

The AI attempts to leave the human player with a number of objects that is a **multiple of 4**.

The important positions are:

```text
4
8
12
```

The AI calculates:

```text
move = remaining_objects % 4
```

For example:

```text
15 objects remaining

15 % 4 = 3

AI removes 3

12 objects remain
```

Another example:

```text
10 objects remaining

10 % 4 = 2

AI removes 2

8 objects remain
```

If the AI continuously leaves the opponent with a multiple of 4, it can force a win when starting from a winning position.

If:

```text
remaining_objects % 4 == 0
```

there is no move that guarantees victory against a perfect opponent. In this situation, the AI can choose one of the available valid moves.

---

## Algorithm Comparison

| Difficulty | Algorithm                      | Strategy                             |
| ---------- | ------------------------------ | ------------------------------------ |
| Easy       | Random Selection               | Selects a random valid move          |
| Medium     | Minimax                        | Searches possible future game states |
| Hard       | Mathematical / Modulo Strategy | Attempts to leave multiples of 4     |

---

## Project Structure

The project can be organized as follows:

```text
nim_game/
│
├── main.py
├── game.py
├── player.py
├── ai.py
└── README.md
```

### `main.py`

Controls the overall execution of the game, including:

* Starting the game
* Managing player and AI turns
* Checking when the game ends
* Displaying the winner

### `game.py`

Contains the main game logic, including:

* Number of remaining objects
* Validating moves
* Removing objects
* Checking whether the game has ended

### `player.py`

Handles the human player's input and move selection.

### `ai.py`

Contains the AI algorithms used by the three difficulty levels:

* Random algorithm
* Minimax algorithm
* Optimal mathematical algorithm

---

## Game Flow

```text
Start Game
    ↓
Select AI Difficulty
    ↓
Initialize 15 Objects
    ↓
Player Turn
    ↓
Validate Move
    ↓
Remove Objects
    ↓
Are There 0 Objects?
    ↓
Yes → Player Wins
    ↓ No
AI Turn
    ↓
AI Selects Move
    ↓
Remove Objects
    ↓
Are There 0 Objects?
    ↓
Yes → AI Wins
    ↓ No
Return to Player Turn
```

---

## Technologies

The initial version of the project is developed using:

* Python
* Object-Oriented Programming
* Minimax search
* Mathematical game strategy

The game may later be implemented with a graphical or web-based interface.

---

## Group Members

Saif Salem Aldhaheri 100063183,
Sultan Mohammed Aljaberi 100063074,
Saeed Khalifa Alkaabi 100063100,
Suhail Saeed Al Hammadi 100063443
---

## Instructor

**Instructor Name:** Naoufel Werghi

---

## Authors

Developed as a group project for **Intro to Atrificial Intelligence COSC 330**.
