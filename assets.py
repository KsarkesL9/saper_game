# assets.py
import pygame
import config

# Initialize Pygame's font and mixer systems
# These are safe to call multiple times if already initialized.
pygame.font.init()
pygame.mixer.init()

# Fonts
FONT = None
BIG_FONT = None
try:
    FONT = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
    BIG_FONT = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_BIG)
except pygame.error as e:
    print(f"Warning: Could not load system font '{config.FONT_NAME}'. Using default. Error: {e}")
    # Fallback to Pygame's default font if system font fails
    FONT = pygame.font.Font(None, config.FONT_SIZE_NORMAL + 5)
    BIG_FONT = pygame.font.Font(None, config.FONT_SIZE_BIG + 10)


# Sound
CLICK_SOUND = None


def play_click_sound():
    pass