"""
Module: sprites.py
Description: Holds the Tile and Board classes. This file handles the board,
             mines, clue numbers, recursive uncovering, and drawing the grid.
Inputs: Tile coordinates, number of mines, a Pygame surface and font, and the
        constants from settings.py.
Outputs: Updated tile/board data and the board drawn in the game window.
Implementation author: Cameren Green
Documentation author: Pranav Reddy
Creation dates: September 15, 2026 (Tile, Board, and their constructors) September 16, 2026 (place_mines and methods below it)

External sources:
- Pygame draw API: https://www.pygame.org/docs/ref/draw.html
  Referenced for drawing rectangles, circles, polygons, and lines.
- OpenAI GPT-5.6: helped with conceptual part for def dig() and implementation guide for def draw().
"""

import random
import pygame
from settings import *


class Tile:
    """
    Class: Tile
    Description: Stores the location and game state for one square.
    Inputs: Column, row, and the starting tile type.
    Outputs: One Tile object for the board to use.
    Implementation author: Cameren Green
    Documentation author: Pranav Reddy
    Creation date: September 15, 2026
    Source: Original.
    """

    def __init__(self, x, y, type_val):
        """
        Function: Tile.__init__
        Description: Saves the tile location, type, and starting state.
        Inputs: x column, y row, and type_val ('.', 'X', or 'C').
        Outputs: Sets the Tile fields and returns None.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 15, 2026
        Source: Original.
        """

        # Save tile position in the grid
        self.x = x
        self.y = y

        # Tile types: '.' is empty, 'X' is a mine, and 'C' is a clue
        self.type = type_val

        # Tiles start covered with no flag or clue number
        self.revealed = False
        self.flagged = False
        self.clue_num = 0


class Board:
    """
    Class: Board
    Description: Stores the 10x10 grid and handles its main operations.
    Inputs: Constants from settings.py and the inputs for each method.
    Outputs: Updated tiles and the board drawn on a Pygame surface.
    Implementation author: Cameren Green
    Documentation author: Pranav Reddy
    Creation date: September 15, 2026
    Source: Original with GPT-5.6 assistance on dig() conceptually and draw()
    """

    def __init__(self):
        """
        Function: Board.__init__
        Description: Creates the tile grid and the set used during recursion.
        Inputs: ROWS and COLS from settings.py.
        Outputs: Sets board_list and dug and returns None.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 15, 2026
        Source: Original.
        """

        # First index is x, second index is y
        self.board_list = [[Tile(col, row, '.') for row in range(ROWS)] for col in range(COLS)]

        # Track tiles already visited during recursion
        self.dug = set()

    def place_mines(self, safe_x, safe_y, num_mines):
        """
        Function: Board.place_mines
        Description: Places random mines away from the first clicked area.
        Inputs: Safe x/y coordinates and the number of mines.
        Outputs: Changes the selected tile types to 'X' and returns None.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 16, 2026
        Source: Original.
        """
        # Make the first clicked tile and the eight tiles around it safe.
        safe_zone = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                safe_zone.add((safe_x + dx, safe_y + dy))

        # Build a list of every position where a mine is allowed.
        available = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in safe_zone]
        
        # Use random.sample for unique positions so mines cannot overlap.
        mine_spots = random.sample(available, num_mines)
        for x, y in mine_spots:
            self.board_list[x][y].type = 'X'

    def place_clues(self):
        """
        Function: Board.place_clues
        Description: Adds clue types and numbers after the mines are placed.
        Inputs: The current board.
        Outputs: Updates tile types and clue numbers and returns None.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 16, 2026
        Source: Original.
        """

        # Go through the board but skip mines
        for x in range(COLS):
            for y in range(ROWS):
                if self.board_list[x][y].type != 'X':
                    total_mines = self.check_neighbors(x, y)

                    # Leave zero tiles empty and turn positive counts into clues.
                    if total_mines > 0:
                        self.board_list[x][y].type = 'C'
                        self.board_list[x][y].clue_num = total_mines
    def check_neighbors(self, x, y):
        """
        Function: Board.check_neighbors
        Description: Counts the mines touching one tile.
        Inputs: The x and y coordinates of the tile.
        Outputs: The number of nearby mines from 0 through 8.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 16, 2026
        Source: Original.
        """
        total = 0

        # These offsets check the 3x3 area centered on the tile.
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy

                # Only check coordinates inside the board
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if self.board_list[nx][ny].type == 'X':
                        total += 1

        return total

    def dig(self, x, y):
        """
        Function: Board.dig
        Description: Reveals a tile and recursively opens blank areas.
        Inputs: The x and y coordinates being uncovered.
        Outputs: False for a mine and True for a safe tile.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 16, 2026
        Source: GPT-5.6 assisted, conceptual idea was helped by ChatGPT. Implmentation done by Cameren.
        """
        tile = self.board_list[x][y]

        # Bug fix, to prevent digging from revealing a flagged safe tile. Authored by Pranav and GPT-5.6
        if tile.flagged:
            return True

        # Mark this tile as visited so the recursion does not loop back to it.
        self.dug.add((x, y))

        # Reveal a mine and tell main.py that the player lost.
        if tile.type == 'X':
            tile.revealed = True
            return False

        # Reveal a clue, but stop the recursion in this direction.
        if tile.type == 'C':
            tile.revealed = True
            return True

        # Blank tiles are safe, so the uncovering can continue around them.
        tile.revealed = True

        # Stay inside the board while checking the surrounding tiles.
        for row in range(max(0, x - 1), min(COLS - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(ROWS - 1, y + 1) + 1):
                # Skip tiles that this recursive search already visited.
                if (row, col) not in self.dug:
                    self.dig(row, col)
        # The uncover was safe if the method reaches this return.
        return True

    def draw(self, surface, font):
        """
        Function: Board.draw
        Description: Draws every tile based on its current state.
        Inputs: The Pygame surface and font used by the game.
        Outputs: Updates the surface and returns None.
        Implementation author: Cameren Green
        Documentation author: Pranav Reddy
        Creation date: September 16, 2026
        Source: Pygame documentation and GPT-5.6 assistance (Help with how to draw)
        """

        # Draw every tile once per frame
        for x in range(COLS):
            for y in range(ROWS):
                tile = self.board_list[x][y]

                # Convert grid position to screen position
                pos_x = MARGIN_LEFT + (x * TILESIZE)
                pos_y = MARGIN_TOP + (y * TILESIZE)
                rect = pygame.Rect(pos_x, pos_y, TILESIZE, TILESIZE)

                # A revealed tile can show a mine, a clue, or nothing.
                if tile.revealed:
                    pygame.draw.rect(surface, TILE_REVEALED, rect)
                    
                    if tile.type == 'X':
                        # Draw the mine as a black circle in the center.
                        center = (pos_x + TILESIZE // 2, pos_y + TILESIZE // 2)
                        pygame.draw.circle(surface, MINE_COLOR, center, 10)
                    elif tile.type == 'C':
                        # Pick the standard color for this clue number.
                        color = NUM_COLORS.get(tile.clue_num, TEXT_COLOR)
                        text = font.render(str(tile.clue_num), True, color)
                        surface.blit(text, (pos_x + 13, pos_y + 8))
                else:
                    # Covered tiles all use the same color to hide their type.
                    pygame.draw.rect(surface, TILE_UNREVEALED, rect)
                    
                    if tile.flagged:
                        # Make the flag from a red triangle and a dark pole.
                        flag_points = [
                            (pos_x + 10, pos_y + 10),
                            (pos_x + 25, pos_y + 15),
                            (pos_x + 10, pos_y + 20)
                        ]
                        pygame.draw.polygon(surface, FLAG_COLOR, flag_points)
                        pygame.draw.line(surface, TEXT_COLOR, (pos_x + 10, pos_y + 10), (pos_x + 10, pos_y + 30), 2)

                # Draw a thin border around each tile
                pygame.draw.rect(surface, GRID_COLOR, rect, 1)
