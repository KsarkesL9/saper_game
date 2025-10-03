# config.py

# Screen dimensions for the menu (fixed size 1200x900 from previous step)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Font settings
FONT_NAME = "consolas"
FONT_SIZE_NORMAL = 48  # Wystarczająca dla tekstu i timera

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Game board settings
# CELL_SIZE i MARGIN będą teraz obliczane dynamicznie
BOARD_AREA_PERCENTAGE = 0.80 # Plansza ma zajmować ok. 80% mniejszego wymiaru okna
MIN_MARGIN = 20 # Minimalny margines bezpieczeństwa

# Default values for custom game mode
INITIAL_CUSTOM_SIZE = 10
INITIAL_CUSTOM_MINES = 15

# Min/Max dla trybu niestandardowego
MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 30
MIN_MINES_CUSTOM = 1

# Difficulty levels (dostosowane)
# Struktura: "Level Name": {"size": int, "mines": int}
DIFFICULTIES = {
    "Łatwy": {"size": 6, "mines": 8},
    "Średni": {"size": 10, "mines": 20},
    "Trudny": {"size": 14, "mines": 30},
    "Ekspert": {"size": 18, "mines": 40},
}

# Scoreboard file
SCORE_FILE = "highscores.json"