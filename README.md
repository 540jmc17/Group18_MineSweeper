# Group 18 - Minesweeper

## Project Overview

This repository is for **Group 18's Software Engineering II Minesweeper Project**.

We will use this repository to collaborate on the project, manage our code, and track our progress.

---

# Features

## 10x10 Grid

* Fixed 10x10 Minesweeper grid.
* Columns labeled A-J.
* Rows numbered 1-10.

## Configurable Difficulty

* Terminal prompt allows entering 10 to 20 mines.
* Mines are randomly placed when the game begins.

## Guaranteed Safe First Click

* The first clicked cell is guaranteed to be safe.
* The 8 cells surrounding the first clicked cell are also guaranteed to be safe.
* Mines are placed dynamically after the first click.

## Recursive Flood Fill

* Zero-clue empty cells automatically uncover adjacent clear tiles.
* Recursive revealing continues until numbered boundary cells are reached.

## Flagging System

* Right-click marks suspected mine locations with red flags.
* Right-clicking a flagged cell removes the flag.
* Flagged cells cannot be clicked until the flag is removed.
* The number of flags cannot exceed the selected number of mines.

## Live HUD

* Tracks the current game state:

  * `Playing`
  * `Victory!`
  * `Game Over`
* Displays the remaining number of flags.
* Remaining flags are calculated as:

```text
Total Mines - Placed Flags
```

## Instant Reset

* The game can be restarted after a victory or loss.
* The restart process uses a non-blocking game loop.
* The game does not use recursive game calls for restarting.

## Standalone Vector Graphics

* Uses native Pygame drawing primitives.
* No external image assets are required.
* No external asset directories are required.

---

# Controls

| Action                  | Control                     |
| ----------------------- | --------------------------- |
| Uncover a cell          | Left Click                  |
| Place a flag            | Right Click                 |
| Remove a flag           | Right Click on flagged cell |
| Restart after game ends | Click                       |

---

# Technologies

* **Python 3.13**
* **Pygame**
* **Git**
* **GitHub**

---

## `main.py`

Responsible for:

* Pygame initialization
* Main game loop
* Player input
* Game state
* Win/loss handling
* Game reset
* User interface

## `settings.py`

Contains game settings and constants, including:

* Board dimensions
* Tile size
* Window dimensions
* Frame rate
* Colors
* Game title

## `sprites.py`

Contains the board and tile functionality, including:

* Tile states
* Board management
* Mine placement
* Adjacent mine calculations
* Recursive cell uncovering
* Board rendering

---

# Step-by-Step Instructions to Run

## Assumptions

* **Python Version 3.13**
* **Pygame can be installed**

## 1. Clone the Repository

Clone the repo by running:

```bash
git clone https://github.com/540jmc17/Group18_MineSweeper.git
```

## 2. Navigate to the Project

Run:

```bash
cd Group18_MineSweeper
cd src
```

## 3. Install Pygame If Needed

If Pygame is not already installed, run:

```bash
python -m pip install pygame
```

## 4. Run the Game

Run the following:

```bash
python main.py
```

## 5. Start Playing

Enter your number of mines and get started playing.

The number of mines must be between **10 and 20**.

---

# How to Play

1. Enter a number of mines between **10 and 20**.
2. The Minesweeper board will open.
3. **Left-click** a cell to uncover it.
4. The first clicked cell and its surrounding cells are guaranteed to be safe.
5. Numbers indicate the number of adjacent mines.
6. Empty cells automatically uncover surrounding safe cells.
7. **Right-click** a cell to place a flag.
8. **Right-click** a flagged cell to remove the flag.
9. Flagged cells cannot be uncovered.
10. Uncover all non-mine cells to win.
11. Uncovering a mine results in a loss.

---

# Win Condition

The player wins when all non-mine cells have been uncovered.

The game will display:

```text
Victory!
```

---

# Loss Condition

The player loses when a mine is uncovered.

After losing:

* The game ends.
* All mines are revealed.
* The game-over state is displayed.
* The player can click to restart the game.
---

# Team Details

## Team Members

### Jake

* **Phone Number:** 913-626-6356
* **Email:** [crawfordjake862@gmail.com](mailto:crawfordjake862@gmail.com)
* **Role:** Group Leader (Scrum Master), Developer

### John

* **Phone Number:** 913-942-4274
* **Email:** [jwpannell10@gmail.com](mailto:jwpannell10@gmail.com)
* **Role:** Developer and Tester

### Zema

* **Phone Number:** 913-215-3394
* **Email:** [zemasamuel@gmail.com](mailto:zemasamuel@gmail.com)
* **Role:** Developer and Tester

### Pranav

* **Phone Number:** 316-841-0242
* **Email:** [Pranavreddy12@icloud.com](mailto:Pranavreddy12@icloud.com)
* **Role:** Developer and Tester

### Cameren

* **Phone Number:** 402-591-0661
* **Email:** [greencmaeren@gmail.com](mailto:greencmaeren@gmail.com)
* **Role:** Developer and Tester

### Karim

* **Phone Number:** 913-203-7753
* **Email:** [lakhanikarim01@gmail.com](mailto:lakhanikarim01@gmail.com)
* **Role:** Developer and Tester

### Nate

* **Phone Number:** 913-244-7847
* **Email:** [natigetahun11@gmail.com](mailto:natigetahun11@gmail.com)
* **Role:** Developer and Tester

### Ahmed

* **Phone Number:** 785-840-7254
* **Email:** [Ahmed.r.gharib@gmail.com](mailto:Ahmed.r.gharib@gmail.com)
* **Role:** Developer and Tester

---

# Project Planning

Project roles, tasks, deadlines, and Sprint 1 goals will be discussed and decided as a team during our meeting.

The team will use GitHub to:

* Collaborate on code
* Manage project branches
* Integrate completed work
* Track project changes
* Maintain project documentation
