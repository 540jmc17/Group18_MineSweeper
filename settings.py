"""
Module: settings.py
Description: Stores the constants used throughout the game, including the board
             size, window layout, frame rate, window title, and colors for the
             tiles, flags, mines, and clue numbers.
Inputs: None. This file only defines constants.
Outputs: Constants imported by main.py and sprites.py.
Implementation author: [Full Name]
Documentation author: [Full Name]
Creation date: [Month Day, 2026]

External sources:
- None. The number colors follow the standard colors used in classic
  Minesweeper (1 = blue, 2 = green, 3 = red, etc.).
"""

# Board dimensions (project requires a fixed 10x10 grid)
TILESIZE = 40   # size of each tile in pixels
ROWS = 10       # rows labeled 1-10
COLS = 10       # columns labeled A-J

# Extra space around the board for the HUD and row/column labels
MARGIN_TOP = 80    # room for mine counter, status text, and column letters
MARGIN_LEFT = 40   # room for row numbers

# Window size is based on the board size plus margins.
# The extra 30 px adds padding on the right and bottom edges.
WIDTH = (TILESIZE * COLS) + MARGIN_LEFT + 30
HEIGHT = (TILESIZE * ROWS) + MARGIN_TOP + 30
FPS = 60                            # frame rate cap for the game loop
TITLE = "EECS 581 - Minesweeper"    # window title

# UI and tile colors (RGB)
BG_COLOR = (230, 230, 230)          # window background
TILE_UNREVEALED = (180, 180, 180)   # covered tile
TILE_REVEALED = (215, 215, 215)     # uncovered tile (lighter so it stands out)
GRID_COLOR = (100, 100, 100)        # grid lines
TEXT_COLOR = (20, 20, 20)           # labels, HUD, and status text
FLAG_COLOR = (220, 50, 50)          # flags
MINE_COLOR = (30, 30, 30)           # mines shown when the player loses

# Colors for clue numbers 1-8, using classic Minesweeper colors.
# 0 is not included because tiles with no adjacent mines are drawn blank.
NUM_COLORS = {
    1: (0, 0, 255),       # blue
    2: (0, 128, 0),       # green
    3: (255, 0, 0),       # red
    4: (0, 0, 128),       # dark blue
    5: (128, 0, 0),       # dark red
    6: (0, 128, 128),     # teal
    7: (0, 0, 0),         # black
    8: (128, 128, 128)    # gray
}
