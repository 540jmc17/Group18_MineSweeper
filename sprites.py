"""
Module: sprites.py
Description: Tile and Board classes to manage the grid state, mine placement,
             number clues, and recursive uncovering.
"""

import random
import pygame
from settings import *


class Tile:
    # Basic data container for individual tile states
    def __init__(self, x, y, type_val):
        self.x = x
        self.y = y
        self.type = type_val  # '.' = empty, 'X' = mine, 'C' = clue number
        self.revealed = False
        self.flagged = False
        self.clue_num = 0


class Board:
    def __init__(self):
        # 10x10 grid of tile objects
        self.board_list = [[Tile(col, row, '.') for row in range(ROWS)] for col in range(COLS)]
        # Track revealed tiles during recursion using a set for fast lookups
        self.dug = set()

    def place_mines(self, safe_x, safe_y, num_mines):
        # Safe first click: exclude the clicked cell and its 8 neighbors from mine pool
        safe_zone = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                safe_zone.add((safe_x + dx, safe_y + dy))

        # Get all coordinates on the board that are outside the safe zone
        available = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in safe_zone]
        
        # Pick random distinct locations for the mines
        mine_spots = random.sample(available, num_mines)
        for x, y in mine_spots:
            self.board_list[x][y].type = 'X'

    def place_clues(self):
        # Calculate adjacent mine counts for every non-mine tile
        for x in range(COLS):
            for y in range(ROWS):
                if self.board_list[x][y].type != 'X':
                    total_mines = self.check_neighbors(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].type = 'C'
                        self.board_list[x][y].clue_num = total_mines

    def check_neighbors(self, x, y):
        # Check all 8 surrounding cells and count mines
        total = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if self.board_list[nx][ny].type == 'X':
                        total += 1
        return total

    def dig(self, x, y):
        # Recursive flood fill reveal
        self.dug.add((x, y))
        tile = self.board_list[x][y]

        # Stepped on a mine -> game over
        if tile.type == 'X':
            tile.revealed = True
            return False

        # Hit a numbered clue -> reveal and stop recursing in this direction
        if tile.type == 'C':
            tile.revealed = True
            return True

        # Blank tile: reveal and recursively check adjacent neighbors
        tile.revealed = True

        for row in range(max(0, x - 1), min(COLS - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(ROWS - 1, y + 1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)

        return True

    def draw(self, surface, font):
        # Render tiles using pygame drawing primitives instead of external image files
        for x in range(COLS):
            for y in range(ROWS):
                tile = self.board_list[x][y]
                pos_x = MARGIN_LEFT + (x * TILESIZE)
                pos_y = MARGIN_TOP + (y * TILESIZE)
                rect = pygame.Rect(pos_x, pos_y, TILESIZE, TILESIZE)

                if tile.revealed:
                    pygame.draw.rect(surface, TILE_REVEALED, rect)
                    
                    if tile.type == 'X':
                        # Draw mine as a circle
                        center = (pos_x + TILESIZE // 2, pos_y + TILESIZE // 2)
                        pygame.draw.circle(surface, MINE_COLOR, center, 10)
                    elif tile.type == 'C':
                        # Render adjacent mine number text
                        color = NUM_COLORS.get(tile.clue_num, TEXT_COLOR)
                        text = font.render(str(tile.clue_num), True, color)
                        surface.blit(text, (pos_x + 13, pos_y + 8))
                else:
                    pygame.draw.rect(surface, TILE_UNREVEALED, rect)
                    
                    if tile.flagged:
                        # Draw flag: flagpole line and red triangle
                        flag_points = [
                            (pos_x + 10, pos_y + 10),
                            (pos_x + 25, pos_y + 15),
                            (pos_x + 10, pos_y + 20)
                        ]
                        pygame.draw.polygon(surface, FLAG_COLOR, flag_points)
                        pygame.draw.line(surface, TEXT_COLOR, (pos_x + 10, pos_y + 10), (pos_x + 10, pos_y + 30), 2)

                # Grid outline around the tile
                pygame.draw.rect(surface, GRID_COLOR, rect, 1)
