"""
Module: main.py

Description: 
    Controls the main Minesweeper game, including the Pygame window,
    game state, player input, and interaction with the game board.

Inputs:
    - Number of mines selected by the user (10-20)
    - Mouse input

Outputs:
    A playable Pygame Minesweeper game window

Editors: John Pannell and Jake Crawford

Creation Date: 09/19/26

External Sources: 
    - ChatGPT (GPT-5.6 Luna): Used for explanations and integration assistance. See AI Use Disclosure below.
    - Tech & Gaming, "How to make Minesweeper in Pygame - Step-by-Step Tutorial for beginner":
      https://www.youtube.com/watch?v=n0jZRlhLtt0
      Used as the starting point for the Minesweeper Pygame implementation.

AI Use Disclosure:

    AI Tool: ChatGPT (GPT-5.6 Luna)

    Use of AI: AI was used to assist with the integration and revision of existing 'main.py' code with other project components and
    existing functions. The AI was also used to help understand Pygame-specific syntax and how 'main.py' interacts with functions and data
    from other source files.

    Prompt: The following prompt is representative of the prompts used to assist with integration between components:
        "Given our architectural components and other source files, assist in editing the Game class to ensure integration, correct logic, 
        and reducing complexity. Any suggested changes must be explained so they can be reviewed and understood."

    Changes After AI Assistance: All suggested code changes were reviewed and understood by the editors before being used. One change that was implemented 
    was the use of 'continue' statements in the 'events()' method to reduce unnecessary nested 'if' statements. AI assistance was also used to explain Pygame
    syntax related to initializing the screen, display, title, clock, and event handling. The editors verified the logic and made final decisions about which
    changes were incorporated into the file.
"""

import sys
import pygame
from settings import *
from sprites import Board

class Game:
    """
    Manages the overall Minesweeper game.

    The Game class initializes the Pygame window, manages the game state,
    processes player input, coordinates the game board and game logic,
    and controls the main game loop to ensure efficient gameplay.

    Inputs:
        num_mines: The number of mines selected by the user, from 10 to 20
        
    Member Variables:
        - screen: The Pygame window used to display the game.
        - clock: Controls the game's frame rate.
        - font: Font used to display text in the game window.
        - num_mines: The number of mines the user selects.
        - flags_placed: The number of flags on the board currently.
        - board: The current Minesweeper board.
        - playing: Indicates whether the game is being played or not currently.
        - first_click: Indicates whether the game is waiting for the first click.
        - game_over: Indicates whether the game has ended.
        - win: Indicates if the player has won the game.

    Outputs:
        An interactive Pygame Minesweeper game.
    """

    def __init__(self, num_mines):
        """
        Initializes the Minesweeper game and the Pygame components.

        Inputs:
            num_mines: The number of mines selected by the user, 10 to 20.

        Outputs:
            None. Initializes the Game object's attributes and Pygame components.
        """

        # Combined: Syntax for Pygame initialization assistance necessary
        pygame.init() # initialize Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create the Pygame window using width/height from settings.py
        pygame.display.set_caption(TITLE) # set the title of the Pygame window
        self.clock = pygame.time.Clock() # create a clock to control frame rate
        self.font = pygame.font.SysFont("Arial", 18, bold=True) # create font used to display text

        # Combined: Initialize the member variables
        self.num_mines = num_mines
        self.flags_placed = 0
        self.board = None
        self.playing = False
        self.first_click = True
        self.game_over = False
        self.win = False

    def run(self):
        """
        Runs the main Minesweeper loop for the game to take place.

        A new game board is created, the game state is reset, player input is processed,
        the game display is updated, and the game-over screen is handled.

        Inputs:
            None.
        
        Outputs:
            None. Runs the game and manages the game and game-over loops.
        """

        # Combined: Outer loop that allows a new game to start after reset occurs
        while True:
            self.board = Board()
            self.playing = True
            self.first_click = True
            self.game_over = False
            self.win = False
            self.flags_placed = 0

            # The main gameplay loop that keeps the game running while the player is still in progress
            while self.playing:
                self.events() # process inputs and game events
                self.draw() # update the display of the game
                self.clock.tick(FPS) # Combined: syntax to control the game loop speed necessary

            # Game-over loop that displays the end screen until restart
            while self.game_over:
                self.end_screen() # display the game-over or victory screen and wait for input
                self.clock.tick(FPS) # Combined: syntax to control the game-over loop speed necessary       

    def events(self):
        """
        Handles game events and player inputs.

        The following method handles closing the game window, left mouse click for uncovering cells,
        and right mouse click for placing or removing flags. It also handles the first-click mine placement
        and updates the state of the game when a mine is uncovered.

        Inputs:
            None. Receives player input from Pygame event.

        Outputs:
            None. Updates the game board and game state.
        """

        # Combined: Check each event received from Pygame
        for event in pygame.event.get():

            # Handle the window close to shut down Pygame
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Ignore events that are not mouse button presses
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            mouse_x, mouse_y = pygame.mouse.get_pos() # get the mouse position in pixels

            # Confirm the mouse click is within the board area
            if mouse_x < MARGIN_LEFT or mouse_y < MARGIN_TOP:
                continue

            col = (mouse_x - MARGIN_LEFT) // TILESIZE # convert the x coordinate to a board column
            row = (mouse_y - MARGIN_TOP) // TILESIZE # convert the y coordinate to a board row
        
            # Confirm the resulting column and row is one of the 10x10 cells
            if not (0 <= col < COLS and 0 <= row < ROWS):
                continue

            tile = self.board.board_list[col][row] # get the tile clicked

            # Reveal the tile with a left click on a non-flagged tile
            if event.button == 1 and not tile.flagged:

                # Set up the mines after the first click
                if self.first_click:

                    # Randomly place mines keeping the first click safe
                    self.board.place_mines(col, row, self.num_mines)

                    # Calculate the adjacent mine count for each tile
                    self.board.place_clues()

                    self.first_click = False # the first click has now happened

                # Check to see if there is a mine
                safe = self.board.dig(col, row)

                # If a mine is uncovered, end the game and reveal all mines
                if not safe:
                    self.playing = False
                    self.game_over = True
                    self.reveal_all_mines()

                self.check_win() # check if player has won the game

            # For a right click on a non-revealed flag, we must add or remove a flag
            elif event.button == 3 and not tile.revealed:

                # If the tile is already flagged, we must remove it
                if tile.flagged:
                    tile.flagged = False 
                    self.flags_placed -= 1

                # Otherwise, mark the tile as flagged
                else:
                    tile.flagged = True
                    self.flags_placed += 1