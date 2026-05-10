# Grid Escape

## Project Description

* **Project by:** Kantanut Utamapongchai
* **Game Genre:** Puzzle / Strategy

Grid Escape is a grid-based puzzle game developed using Python and Pygame.
Players must navigate through puzzle levels and reach the goal before the time limit expires.

Each level contains different mechanics such as ice tiles, spikes, lava, teleporters, breakable glass, barriers, and switches. These mechanics require players to plan their movement carefully and solve each puzzle efficiently.

The game also records gameplay statistics, including completion time, steps taken, number of deaths, and attempt counts. These data are visualized in a statistical screen using summary tables and a win-rate graph.

---

## Installation

To clone this project:

```sh
git clone https://github.com/kan1243/Grid-Escape.git
cd Grid-Escape
```

### Windows

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Mac

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide

After activating the Python environment, run the game using the following command.

### Windows

```bat
python game.py
```

### Mac

```sh
python3 game.py
```

---

## Tutorial / Usage

1. Enter your player name.
2. Select a level from the level selection screen.
3. Use the arrow keys to move the character.
4. Reach the goal before the time limit runs out.
5. Avoid traps such as spikes and lava.
6. Use switches to remove barriers.
7. Step on teleporters to move to linked locations.
8. Open the **STAT** screen from the menu to view gameplay statistics.
9. Press **ESC** to return to the previous menu.

---

## Game Features

* 10 puzzle levels with increasing difficulty
* Randomized level variants
* Grid-based movement system
* Time-limited gameplay
* Ice tiles with sliding mechanics
* Spike traps and lava hazards
* Teleporters
* Breakable glass tiles
* Barriers and switches
* Player performance tracking
* Statistical summary table
* Win-rate visualization graph

---

## Known Bugs

* Player names currently support English letters and numbers only.
* On ice tiles, the player may slide into the goal before the sprite visually reaches it.
* Level 10 is larger than the visible screen area, but it remains fully playable.

---

## Unfinished Works

* Additional sound effects and animations.
* More advanced data visualizations.
* UI improvements and visual polish.
* The current dataset contains fewer than 100 gameplay records.

---

