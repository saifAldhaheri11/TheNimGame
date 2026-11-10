# Nim Game: Player vs AI

## Project Overview

This project is an interactive Python implementation of the **Nim Game**.

The game allows a human player to compete against an AI opponent using different decision-making and search algorithms.

The game begins with a single pile containing **15 matchsticks by default**. The player can choose between **5 and 30 matches** before starting. Players take turns removing 1, 2, or 3 matches.

This project follows the **Misère Nim** variation, where the player who removes the last match **loses**.

The game features four AI difficulty levels:

1. **Easy:** Random Algorithm
2. **Medium:** Greedy Algorithm
3. **Hard:** Depth-Limited Minimax
4. **Extreme:** Minimax with Alpha-Beta Pruning

The player can select the AI difficulty and choose whether to play first or allow the AI to make the opening move.

The game also includes a points system, move history, sound effects, and saved statistics.

The project's objective is to implement and compare AI algorithms based on their decision-making strategies, effectiveness, and computational performance.

## Requirements

- Python 3 with Tkinter.
- A computer with a graphical desktop.
- The provided `.wav` files inside the `sounds` folder.

No additional Python packages are required. On Linux, WAV playback uses `aplay` when available.

## How to Play

1. Select **PLAY** from the main menu.
2. Choose the difficulty and starting player.
3. Use **+** or **−** to choose between **5 and 30 starting matches**.
4. Press **Start Game**.
5. Click any **1, 2, or 3 matches** to select them. Click again to deselect.
6. Press **Remove** to confirm your move.
7. Continue taking turns until no matches remain.

**The player who removes the last match loses.**

### Points System

The player earns points based on move quality, decision speed, the game result, and difficulty.

| Action | Points |
|---|---:|
| Best-path move | 100 |
| Other legal move | 20 |
| Speed bonus per move | Up to 50 |
| Winning the game | 500 |

The speed bonus decreases as the player takes longer to move and reaches **0 after 10 seconds**.

A best-path move follows the scoring algorithm's preferred outcome: win in fewer moves when possible, or delay losing when defeat is unavoidable under perfect play.

The final score uses the selected difficulty's multiplier:

| Difficulty | Multiplier |
|---|---:|
| Easy | ×1 |
| Medium | ×1.5 |
| Hard | ×2 |
| Extreme | ×3 |

**Final score = (total move points + win bonus) × difficulty multiplier**, rounded to a whole number.

Move points include speed bonuses. A loss receives no win bonus, but points earned during the game still count.

High scores are saved separately for each difficulty.

## Game Rules

1. The game begins with **15 matches by default** in a single pile.
2. The starting number can be changed to between **5 and 30** on the PLAY setup page.
3. The game is played between a human player and an AI opponent.
4. Each player can remove **1, 2, or 3 matches** during their turn.
5. A player cannot remove more matches than are currently available.
6. The player who removes the **last match loses the game**.
7. The game ends when no matches remain.
8. Before starting, the human player selects one of the four AI difficulty levels.
9. The human player can choose whether to make the first move or let the AI start.
10. If the AI starts first, its opening move is random, regardless of difficulty.
11. After its opening move, the AI follows the selected difficulty's algorithm.
12. The starting number of matches cannot be changed during an active game.

## User Interface

The main menu contains **PLAY**, **Settings**, **How to Play**, **Stats**, and **Quit**.

- **PLAY:** Choose the difficulty, starting player, and match count.
- **Game screen:** Select matches and view the current turn, remaining matches, live score, and move history.
- **Settings:** Turn AI animations and sound effects on or off.
- **How to Play:** View illustrated instructions.
- **Stats:** View wins, losses, win rates, and high scores for each difficulty, or reset the records.

Selected matches glow gold. The result screen displays the winner, final score, and best-move count. Statistics are saved in `scoreboard.json` between sessions.

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

When the search reaches its depth limit before reaching a terminal state, a heuristic evaluation function estimates the desirability of the resulting position.

**Algorithm Characteristics:**

- Uses adversarial search.
- Explores future states up to depth 3.
- Considers possible opponent responses.
- Uses a heuristic for nonterminal states.
- Reuses previously calculated results through memoization.

### 4. Extreme: Minimax with Alpha-Beta Pruning

The Extreme AI uses **Minimax with Alpha-Beta Pruning**.

Alpha-Beta Pruning is an optimization of the Minimax Algorithm that reduces the number of game states explored without changing the result of an equivalent Minimax search.

The algorithm maintains two values:

- **Alpha (α):** The best score the maximizing player can guarantee so far.
- **Beta (β):** The best score the minimizing player can guarantee so far.

When the algorithm determines that further exploration of a branch cannot affect the final decision, it stops searching that branch.

Unlike the Hard difficulty, Extreme searches to terminal states. Its search depth is set to the number of matches remaining.

**Algorithm Characteristics:**

- Uses adversarial search.
- Searches to terminal game states.
- Eliminates unnecessary branches through pruning.
- Uses move ordering to improve pruning.
- Stores search results to avoid repeating calculations.
- Produces the same minimax result as an equivalent full-depth search.

## Project Structure

```text
TheNimGame/
├── main.py
├── UI.py
├── session.py
├── game.py
├── player.py
├── ai.py
├── scoring.py
├── scoreboard.py
├── scoreboard.json
├── sound.py
├── sounds/
│   ├── click.wav
│   ├── select.wav
│   ├── deselect.wav
│   ├── remove.wav
│   ├── ai_move.wav
│   ├── win.wav
│   └── lose.wav
├── README.md
└── .gitignore
```

| File | Purpose |
|---|---|
| `main.py` | Starts the graphical application. |
| `UI.py` | Contains the menus, matchstick board, settings, statistics, and result screens. |
| `session.py` | Manages game state, turns, AI move selection, and move history. |
| `game.py` | Contains shared game rules and the original terminal version. |
| `player.py` | Receives and validates player input in the terminal version. |
| `ai.py` | Contains the four AI algorithms and supporting search functions. |
| `scoring.py` | Finds best-path moves and calculates move points, speed bonuses, win bonuses, and difficulty multipliers. |
| `scoreboard.py` | Loads, updates, saves, and resets statistics. |
| `scoreboard.json` | Stores wins, losses, and high scores for each difficulty. |
| `sound.py` | Plays sound effects using the operating system's audio tools. |
| `sounds/` | Contains the game's WAV sound effects. |
| `README.md` | Explains the project, rules, scoring, interface, algorithms, and file structure. |
| `.gitignore` | Excludes temporary files such as Python cache folders. |