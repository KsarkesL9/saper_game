# MineSat - A Modern Minesweeper Clone

This is a classic Minesweeper game built with Python and Pygame, but with a few modern twists. The core logic is what you'd expect, but I've added a solver assistant powered by the Z3 SMT solver, a clean UI using `pygame-menu`, and a polished, cyberpunk-inspired visual theme.

## What it does

* **Classic Minesweeper Gameplay**: Standard rules, multiple difficulty levels (Easy, Medium, Hard, Expert), and a custom mode where you can set the board size and number of mines.
* **Z3-Powered Solver**: Press F1 to activate a "cheat mode" that uses the Z3 solver to analyze the board. It calculates the probability of a mine being in any hidden cell, highlighting safe squares (0% chance), definite mines (100% chance), and uncertain areas.
* **Modern UI**: The entire interface, from the main menu to the end-game screen, is built with `pygame-menu`, making it clean and easy to navigate.
* **Customizable Experience**: A dedicated custom game menu allows you to fine-tune the board size and mine count with sliders and real-time validation to prevent impossible setups.
* **Score Tracking**: The game saves the top 5 best times for each standard difficulty level in a local `highscores.json` file.

## How it’s set up

* **`saper.py`**: The main entry point. Initializes Pygame and the main menu.
* **`config.py`**: Holds all the constants for the application — screen dimensions, colors, font settings, difficulty levels, etc.
* **`assets.py`**: Handles loading fonts and sounds.
* **`game_manager.py`**: The primary game loop. Manages game state, handles user input during a session, and orchestrates calls to other modules.
* **`board_logic.py`**: Contains the core game logic: creating the board, placing mines, revealing cells, and checking win conditions. It also includes the Z3 solver integration for probability analysis.
* **`cell.py`**: A simple class representing a single cell on the game board.
* **`drawing.py`**: Responsible for rendering the game board, cells, buttons, and all in-game visual elements onto the screen.
* **`game_ui.py`**: Defines all the menus using `pygame-menu`, including the main menu, custom game settings, scoreboard display, and post-game screens.
* **`scoreboard.py`**: Manages loading and saving player high scores to `highscores.json`.
* **`highscores.json`**: The file where best times are stored.
* **`requirements.txt`**: A list of the Python packages required to run the game.

That's pretty much it. A straightforward but feature-rich Minesweeper project designed to be both playable and a good demonstration of integrating a logic solver into a game.