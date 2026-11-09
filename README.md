# Nim Game: Player vs AI

## Project Overview


This project is an interactive Python implementation of the **Nim Game**

The game allows a human player to compete against an AI opponent using different decision-making and search algorithms.

The game begins with a single pile containing **15 objects**. Players take turns removing 1, 2, or 3 objects from the pile.

This project follows the **Misère Nim** variation, where the player who removes the last object **loses**.

The game features four AI difficulty levels:

1. **Easy:** Random Algorithm
2. **Medium:** Greedy Algorithm
3. **Hard:** Depth-Limited Minimax
4. **Extreme:** Minimax with Alpha-Beta Pruning

The player can select the AI difficulty and choose whether to play first or allow the AI to make the opening move.

The project's objective is to implement and compare AI algorithms based on their decision-making strategies, effectiveness, and computational performance.

---

## Game Rules

1. The game begins with **15 objects** in a single pile.
2. The game is played between a human player and an AI opponent.
3. Each player can remove **1, 2, or 3 objects** during their turn.
4. A player cannot remove more objects than are currently available.
5. The player who removes the **last object loses the game**.
6. The game ends when no objects remain.
7. Before starting, the human player selects one of the four AI difficulty levels.
8. The human player can choose whether to make the first move or let the AI start.
9. If the AI starts first, its opening move is randomly selected from the available valid moves, regardless of difficulty.
10. After its opening move, the AI follows the algorithm associated with the selected difficulty level.

---

## AI Difficulty Levels and Algorithms

The game features four difficulty levels, each demonstrating a different approach to AI decision-making.

### 1. Easy: Random Algorithm

The Easy AI uses **Random Selection** to choose its moves.

The algorithm identifies the available valid moves and randomly selects one without evaluating future game states.

The AI does not consider the consequences of its decisions or attempt to find an optimal strategy.

**Algorithm Characteristics:**
- Randomly selects a valid move.
- Does not explore future game states.
- Does not use a heuristic evaluation function.
- Requires minimal computational resources.

### 2. Medium: Greedy Algorithm

The Medium AI uses a **Greedy Algorithm**, which focuses on making decisions based on the current game state.

The planned implementation selects the move that removes the maximum number of objects currently allowed, without searching through future moves.

Unlike adversarial search algorithms, this approach does not consider how the human player might respond.

**Algorithm Characteristics:**
- Chooses the locally preferred move.
- Does not explore a game tree.
- Does not account for future opponent responses.
- Has low computational complexity.

Because a locally preferred move is not necessarily the best long-term decision, the Greedy Algorithm does not guarantee victory.

### 3. Hard: Depth-Limited Minimax Algorithm

The Hard AI uses the **Minimax Algorithm** with a fixed search depth of **3**.

Minimax is an adversarial search algorithm designed for two-player games. It evaluates possible moves while assuming that both players attempt to make decisions that benefit themselves.

The algorithm constructs a game tree representing possible future states and alternates between maximizing the AI's outcome and minimizing it through the opponent's responses.

Unlike full-depth Minimax, this implementation limits the search to three levels to reduce computational cost.

When the search reaches its depth limit before reaching a terminal state, a heuristic evaluation function estimates the desirability of the resulting position.

**Algorithm Characteristics:**
- Uses adversarial search.
- Explores possible future moves.
- Uses a fixed search depth of 3.
- Considers possible opponent responses.
- Requires a heuristic function for evaluating nonterminal states.

The heuristic evaluation function will be finalized during implementation.

### 4. Extreme: Minimax with Alpha-Beta Pruning

The Extreme AI uses **Minimax with Alpha-Beta Pruning**.

Alpha-Beta Pruning is an optimization of the Minimax Algorithm that reduces the number of game states explored without changing the optimal result of a completed search.

The algorithm maintains two values:

- **Alpha (α):** The best score the maximizing player can guarantee so far.
- **Beta (β):** The best score the minimizing player can guarantee so far.

When the algorithm determines that further exploration of a branch cannot affect the final decision, it stops searching that branch.

Unlike the Hard difficulty, the Extreme AI is designed to search the game tree until terminal states are reached.

**Algorithm Characteristics:**
- Uses adversarial search.
- Searches to terminal game states.
- Eliminates unnecessary branches through pruning.
- Produces the same optimal minimax result as an equivalent full-depth search.
- Can reduce the number of explored states compared with Minimax without pruning.

---

## Algorithm Comparison

| Difficulty | Algorithm | Search Strategy |
|---|---|---|
| Easy | Random Selection | Selects a random valid move |
| Medium | Greedy | Chooses the maximum legal removal |
| Hard | Depth-Limited Minimax | Explores future states up to depth 3 |
| Extreme | Minimax with Alpha-Beta Pruning | Searches to terminal states with branch pruning |

The algorithms differ in their decision-making methods, search depth, computational requirements, and ability to anticipate future moves.

---

## Project Structure

The project is organized into the following files:

```text
TheNimGame/
├── main.py
├── game.py
├── player.py
├── ai.py
├── README.md
└── .gitignore
```

### `main.py`

Serves as the entry point of the application.

It is responsible for starting the program and connecting the different components of the game.

### `game.py`

Contains the main game logic and user interface, including:

- Displaying the main menu.
- Allowing the player to select the difficulty level.
- Displaying the game rules.
- Managing the game state and player turns.
- Checking valid moves and game-ending conditions.
- Determining the winner according to Misère Nim rules.

### `player.py`

Handles the human player's interactions, including:

- Receiving the player's move.
- Validating player input.
- Ensuring that the number of removed objects is valid.

### `ai.py`

Contains the AI decision-making logic for all four difficulty levels:

- Random Algorithm for Easy difficulty.
- Greedy Algorithm for Medium difficulty.
- Depth-Limited Minimax for Hard difficulty.
- Minimax with Alpha-Beta Pruning for Extreme difficulty.

It also handles selecting an AI move based on the chosen difficulty level.

### `README.md`

Provides the project overview, game rules, explanations of the AI algorithms, project structure, and group information.

