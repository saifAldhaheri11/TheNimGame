# Nim Game: Player vs AI

## Project Overview

This project is an interactive Python implementation of the **Nim Game**.

The game allows a human player to compete against an AI opponent using different decision-making and search algorithms.

The game begins with a single pile containing **15 matchsticks by default**. The player can change the starting number to between **5 and 30** in Settings. Players take turns removing 1, 2, or 3 matches from the pile.

This project follows the **Misère Nim** variation, where the player who removes the last match **loses**.

The game features four AI difficulty levels:

1. **Easy:** Random Algorithm
2. **Medium:** Greedy Algorithm
3. **Hard:** Depth-Limited Minimax
4. **Extreme:** Minimax with Alpha-Beta Pruning

The player can select the AI difficulty and choose whether to play first or allow the AI to make the opening move.

The project's objective is to implement and compare AI algorithms based on their decision-making strategies, effectiveness, and computational performance.

## Requirements

- Python 3
- Tkinter
- A computer with a graphical desktop

No additional Python packages or image files are required.

## How to Play

1. Select one of the four difficulty levels.
2. Choose whether you or the AI starts.
3. To change the starting number of matches, open **Settings**, use **+** or **−**, and press **Done**.
4. Press **Start Game**.
5. Click any **1, 2, or 3 matches** to select them. Click again to deselect.
6. Press **Remove** to confirm your move.
7. Continue taking turns until no matches remain.

**The player who removes the last match loses.**

## Game Rules

1. The game begins with **15 matches by default** in a single pile.
2. The starting number can be changed to between **5 and 30** before starting.
3. The game is played between a human player and an AI opponent.
4. Each player can remove **1, 2, or 3 matches** during their turn.
5. A player cannot remove more matches than are currently available.
6. The player who removes the **last match loses the game**.
7. The game ends when no matches remain.
8. Before starting, the human player selects one of the four AI difficulty levels.
9. The human player can choose whether to make the first move or let the AI start.
10. If the AI starts first, its opening move is randomly selected from the available valid moves, regardless of difficulty.
11. After its opening move, the AI follows the algorithm associated with the selected difficulty level.
12. The starting number of matches cannot be changed during an active game.

## User Interface

The graphical interface allows the player to:

- Select the difficulty and starting player.
- Click matches to select them and confirm their removal.
- View the current turn and remaining matches.
- Open **How to Play** and **Settings** from the top bar.
- Restart the game, return to setup, or play again after the result.

Selected matches are highlighted in gold. Settings includes the starting-match count, AI animations, and selection sound.

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

The implementation selects the move that removes the maximum number of matches currently allowed, without searching through future moves.

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
- Uses a heuristic function for evaluating nonterminal states.

### 4. Extreme: Minimax with Alpha-Beta Pruning

The Extreme AI uses **Minimax with Alpha-Beta Pruning**.

Alpha-Beta Pruning is an optimization of the Minimax Algorithm that reduces the number of game states explored without changing the result of an equivalent Minimax search.

The algorithm maintains two values:

- **Alpha (α):** The best score the maximizing player can guarantee so far.
- **Beta (β):** The best score the minimizing player can guarantee so far.

When the algorithm determines that further exploration of a branch cannot affect the final decision, it stops searching that branch.

The current game uses a search depth of **4** for Extreme difficulty. If the depth limit is reached before a terminal state, the heuristic evaluation function estimates the position.

**Algorithm Characteristics:**

- Uses adversarial search.
- Uses a fixed search depth of 4 in the current game.
- Eliminates unnecessary branches through pruning.
- Produces the same minimax result as an equivalent search without pruning.
- Can reduce the number of explored states compared with Minimax without pruning.

## Project Structure

The project is organized into the following files:

```text
TheNimGame/
├── main.py
├── UI.py
├── session.py
├── game.py
├── player.py
├── ai.py
├── README.md
└── .gitignore
```

### main.py

Serves as the entry point of the application.

It is responsible for starting the program and opening the graphical interface.

### UI.py

Contains the graphical user interface, including:

- Difficulty and starting-player selection.
- Displaying and selecting matchsticks.
- Displaying the game rules and settings.
- Showing the current turn, remaining matches, and result.
- Restarting the game and returning to setup.

### session.py

Connects the graphical interface to the game rules and AI algorithms.

It manages the game state, player turns, remaining matches, AI move selection, and winner.

### game.py

Contains the main game rules, including:

- Initializing the starting number of matches.
- Checking valid moves.
- Removing matches.
- Checking game-ending conditions.
- Determining the winner according to Misère Nim rules.

It also contains the original terminal menus and game loop.

### player.py

Handles the human player's interactions in the terminal version, including:

- Receiving the player's move.
- Validating player input.
- Ensuring that the number of removed matches is valid.

### ai.py

Contains the AI decision-making logic for all four difficulty levels:

- Random Algorithm for Easy difficulty.
- Greedy Algorithm for Medium difficulty.
- Depth-Limited Minimax for Hard difficulty.
- Minimax with Alpha-Beta Pruning for Extreme difficulty.

### README.md

Provides the project overview, requirements, game rules, interface information, explanations of the AI algorithms, and project structure.

### .gitignore

Excludes temporary files such as Python cache folders and bytecode files.