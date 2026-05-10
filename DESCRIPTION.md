# Project Description

## 1. Project Overview

* **Project Name:** Grid Escape: A Time-Constrained Puzzle Game
* **Developer:** Kantanut Utamapongchai
* **Programming Language:** Python
* **Libraries Used:** Pygame, CSV, JSON, Collections

### Brief Description

Grid Escape is a grid-based puzzle game developed using Python and Pygame. Players must navigate through puzzle levels and reach the goal before the time limit expires.

Each level contains various mechanics such as ice tiles, spikes, lava, teleporters, breakable glass, barriers, and switches. These mechanics require players to think strategically and plan their movement carefully.

The project also includes a statistical system that records gameplay data, including completion time, number of steps, deaths, and attempts. These data are visualized in a statistics screen using summary tables and win-rate graphs.

### Problem Statement

Many puzzle games focus only on gameplay and do not provide meaningful data analysis. This project combines puzzle game mechanics with statistical analysis to better understand player performance and evaluate level difficulty.

### Target Users

* Students learning Python and object-oriented programming
* Casual players who enjoy puzzle and strategy games
* Developers interested in combining games with data analysis

### Key Features

* 10 puzzle levels with randomized variants
* Grid-based movement system
* Ice tiles with sliding mechanics
* Spike traps and lava hazards
* Teleporters
* Breakable glass tiles
* Barriers and switches
* Time-limited gameplay
* Player performance tracking
* Statistical summary table
* Win-rate visualization graph

---

## 2. Concept

### 2.1 Background

This project was inspired by classic puzzle games that require logical thinking and movement planning. By introducing time constraints and special mechanics such as ice tiles and teleporters, the game becomes more challenging and engaging.

The project also emphasizes the importance of collecting gameplay data to analyze player performance and improve level design.

### 2.2 Objectives

* Develop a fully functional puzzle game using Python and Pygame.
* Apply object-oriented programming principles.
* Design levels with increasing difficulty.
* Record and analyze player performance.
* Visualize gameplay data using tables and charts.

---

## 3. UML Class Diagram

The UML Class Diagram illustrates the relationships between all major components of the project, including:

* Main game controller (`game.py`)
* Level loading system
* Player and level classes
* Gameplay mechanics
* Save and statistics systems
* UI components

The UML class diagram is included in the repository as:

[UML_Class_Diagram.pdf](UML_Class_Diagram.pdf)

---

## 4. Object-Oriented Programming Implementation

The project is organized using object-oriented programming principles. Each class is responsible for a specific part of the system.

### Core Classes

* **LevelManager**: Loads level JSON files and randomly selects unused variants.
* **Level**: Stores map layout, collision data, and all interactive objects.
* **Player**: Manages movement, animation, and player state.
* **Mechanics**: Processes interactions such as ice, teleporters, traps, and goal detection.

### Data Management Classes

* **SaveData**: Records gameplay results to `stats.csv` and calculates attempt numbers and first-pass success.
* **StatScreen**: Loads and visualizes statistical data.

### UI Classes

* **Button**: Reusable button component for menus.

### Main Module

* **game.py**: Controls game states, event handling, rendering, and overall program flow.

---

## 5. Statistical Data

### 5.1 Data Recording Method

Player data is stored in a CSV file named `stats.csv`. Each record contains:

* Player name
* Level number
* Variant number
* Attempt number
* Number of steps
* Time used
* Death count
* Result (`win` or `lose`)
* First-pass success (`True` or `False`)

### 5.2 Statistical Features

The statistics system calculates and displays:

* Average completion time per level variant
* Minimum and maximum completion time
* Average number of deaths
* Total wins and losses
* First-pass win rate for each level

### 5.3 Data Visualization

The game includes a statistics screen with two pages:

1. **Summary Table** – Displays aggregated metrics for each level variant.
2. **Win Rate Graph** – Shows first-pass success percentages for each level.

These visualizations help analyze level difficulty and player performance.

---

## 6. Changed Proposed Features (Optional)

Several features were adjusted during development:

* Laser traps were replaced with lava tiles.
* The number of levels was reduced from 20 to 10.
* The statistical visualization layout was improved.
* Several level designs were adjusted for better playability.

---

## 7. External Sources

* Pygame library ([https://www.pygame.org/](https://www.pygame.org/))
* Python Standard Library (`csv`, `json`, `random`, `collections`, `os`)
* Some game assets and icons were created by the author or generated using ChatGPT.

---

## 8. Project Files

### Source Code

* `game.py`
* `loader.py`
* `level.py`
* `player.py`
* `mechanics.py`
* `button.py`
* `save_data.py`
* `stat_screen.py`

### Data Files

* `stats.csv`
* `levels/level1.json` to `levels/level10.json`

### Documentation

* `README.md`
* `DESCRIPTION.md`
* `UML_Class_Diagram.pdf`
* `Proposal.pdf`

---

## 9. Demonstration Video

The presentation video is available at:

**YouTube Link:** *[(https://youtu.be/VxZlVI1gA40?si=CnckbmI3Zf8yyxS5)]*
