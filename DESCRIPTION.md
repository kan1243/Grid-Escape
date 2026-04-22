# Project Description

## 1. Project Overview

- **Project Name:** Grid Escape: A Time-Constrained Puzzle Game

- **Brief Description:**  
Grid Escape is a grid-based puzzle game developed using Python and Pygame.  
Players must navigate through different levels while avoiding traps, managing time constraints, and interacting with various mechanics such as ice tiles, teleporters, and barriers.

The game also includes a statistical system that records player performance, including time usage, number of deaths, and attempts. These statistics are visualized through tables and charts to provide insights into player behavior and difficulty of each level.

- **Problem Statement:**  
Many puzzle games lack meaningful data tracking and analysis. This project aims to combine gameplay with statistical analysis to better understand player performance and level difficulty.

- **Target Users:**  
- Students learning programming and game development  
- Casual players who enjoy puzzle games  
- Developers interested in combining games with data analysis  

- **Key Features:**  
- Multiple levels with randomized variants  
- Grid-based movement system  
- Special mechanics (ice, spikes, teleporters, barriers)  
- Time-limited gameplay  
- Player performance tracking  
- Statistical table and win-rate visualization  

---

## 2. Concept

### 2.1 Background

This project was inspired by classic puzzle games that require logical thinking and movement planning.  
The addition of time constraints and mechanics like ice tiles increases the challenge and complexity.

The project also highlights the importance of collecting gameplay data to analyze player performance and improve game design.

### 2.2 Objectives

- Develop a fully functional puzzle game using Python and Pygame  
- Apply object-oriented programming principles  
- Collect and analyze gameplay data  
- Visualize player performance using tables and charts  
- Design levels with increasing difficulty  

---

## 3. UML Class Diagram

The UML Class Diagram illustrates the structure of the system, including:
- Game control logic  
- Player behavior  
- Level data  
- Mechanics processing  

📎 (Attach UML diagram PDF here in your repository)

---

## 4. Object-Oriented Programming Implementation

- **Game (main loop)**: Controls game states, input handling, and rendering  
- **Player**: Manages movement, position, and animation  
- **Level**: Stores grid layout, obstacles, and interactive elements  
- **Mechanics**: Handles interactions such as ice, teleporters, traps, and lava  
- **Button**: UI component for menus and navigation  
- **Stat Screen**: Displays statistical data and visualization  

---

## 5. Statistical Data

### 5.1 Data Recording Method
Player data is stored in a CSV file (`stats.csv`) including:
- Player name  
- Level and variant  
- Time used  
- Number of steps  
- Death count  
- Result (win/lose)  
- First-pass success  

### 5.2 Data Features
- Average time per level  
- Minimum and maximum completion time  
- Average number of deaths  
- Win rate per level  

---

## 6. Changed Proposed Features (Optional)

Some mechanics and UI features were adjusted during development:
- Replaced scrolling table with pagination system  
- Improved stat visualization layout  
- Adjusted level design for better playability  

---

## 7. External Sources

- Pygame library (game development framework)  
- Icons and assets (self-created or free resources)  
- Python standard libraries (csv, collections)