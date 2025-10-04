# config.py

# Screen dimensions for the menu
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Font settings
FONT_NAME = "Segoe UI"
FONT_SIZE_NORMAL = 48
FONT_SIZE_SMALL = 24 # Dla przycisków w grze

# Colors - Nowa, spójna paleta w stylu "cyberpunk dark"
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)

# Tła i główne elementy
DARK_NAVY = (21, 28, 41)
MID_NAVY = (33, 42, 63)
LIGHT_NAVY = (50, 63, 94)

# Kolory akcentujące
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ELECTRIC_BLUE = (125, 249, 255)
GREEN_ACCENT = (0, 200, 150)
RED_ACCENT = (255, 80, 120)
YELLOW_ACCENT = (255, 220, 0)

# Kolory dla przycisków w grze
BUTTON_COLOR = LIGHT_NAVY
BUTTON_HOVER_COLOR = MID_NAVY
BUTTON_TEXT_COLOR = WHITE

# Game board settings
BOARD_AREA_PERCENTAGE = 0.80
MIN_MARGIN = 20

# Default values for custom game mode
INITIAL_CUSTOM_SIZE = 10
INITIAL_CUSTOM_MINES = 15

# Min/Max dla trybu niestandardowego
MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 30
MIN_MINES_CUSTOM = 1

# Difficulty levels
DIFFICULTIES = {
    "Łatwy": {"size": 8, "mines": 10},
    "Średni": {"size": 12, "mines": 30},
    "Trudny": {"size": 16, "mines": 60},
    "Ekspert": {"size": 20, "mines": 90},
}

# Scoreboard file
SCORE_FILE = "highscores.json"