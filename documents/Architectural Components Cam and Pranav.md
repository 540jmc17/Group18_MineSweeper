# Architectural Components

## Pranav — Input Handler and User Interface

### Input Handler

The Input Handler receives and validates user input, then translates it into game actions. It is primarily implemented in `main.py`.

- Accepts the mine count from the terminal and ensures it is between 10 and 20.
- Detects left-clicks to uncover cells.
- Detects right-clicks to place or remove flags.
- Converts mouse coordinates into grid positions and ignores clicks outside the grid.
- Prevents flagged cells from being uncovered and revealed cells from being flagged.
- Handles window-close and post-game restart input.

### User Interface

The User Interface presents the current game state to the player. The main screen layout is managed in `main.py`, while individual cells are drawn by `sprites.py` using values from `settings.py`.

The screen displays:

- A 10-by-10 Minesweeper grid.
- Column labels **A–J** and row labels **1–10**.
- Covered, uncovered, and flagged cells.
- Number clues on uncovered cells, showing adjacent mines.
- Revealed mines after a loss.
- The number of flags remaining.
- The current game status: **Playing**, **Victory**, or **Game Over**.

The interface refreshes after each action so the grid, flag count, and game status always reflect the current state.

## Cam — Board Manager and Game Logic

### Board Manager

The Board Manager stores and maintains the game board. It is primarily implemented by the `Board` and `Tile` classes in `sprites.py`.

- Creates and stores the 10-by-10 board.
- Stores each cell's row and column position.
- Tracks whether each cell is covered, uncovered, or flagged.
- Stores whether a cell is empty, a numbered clue, or a mine.
- Stores the adjacent-mine number for clue cells.
- Provides the current board state to the User Interface for display.

### Game Logic

The Game Logic controls the rules and progression of Minesweeper. It is implemented across `sprites.py` and `main.py`.

- Places mines randomly after the first click while keeping the first-click area safe.
- Calculates the number of adjacent mines for each non-mine cell.
- Uncovers selected cells and stops when a numbered clue is reached.
- Recursively reveals connected empty cells and their bordering clues.
- Places and removes flags while tracking the remaining flag count.
- Detects a loss when the player uncovers a mine.
- Detects a win when every non-mine cell has been uncovered.
