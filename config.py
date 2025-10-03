# config.py

# Screen dimensions for the menu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font settings
FONT_NAME = "consolas"
FONT_SIZE_NORMAL = 32
FONT_SIZE_BIG = 72

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
CELL_SIZE = 40
MARGIN = 60

# Default values for custom game mode
INITIAL_CUSTOM_SIZE = 10  # Zmniejszony dla lepszego startu
INITIAL_CUSTOM_MINES = 15 # Gęstość ok. 15% dla 10x10

# Min/Max dla trybu niestandardowego
MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 30 # Maksymalny sensowny rozmiar dla obecnej implementacji
MIN_MINES_CUSTOM = 1

# Difficulty levels (dostosowane)
# Struktura: "Level Name": {"size": int, "mines": int}
DIFFICULTIES = {
    "Łatwy": {"size": 6, "mines": 8},      # Klasyczny "Beginner" (8x8 lub 9x9 lub 10x10 z 10 minami)
    "Średni": {"size": 10, "mines": 20},    # Klasyczny "Intermediate"
    "Trudny": {"size": 14, "mines": 30},    # Wariant "Hard"
    "Ekspert": {"size": 18, "mines": 40}, # Standardowy "Expert" (często 30x16, ale 24x24 jest kwadratowe)
}

# Scoreboard file
SCORE_FILE = "highscores.json"