# assets.py
import pygame
import config

# Initialize Pygame's font and mixer systems
# These are safe to call multiple times if already initialized.
pygame.font.init()
pygame.mixer.init()

# Fonts
FONT = None
BIG_FONT = None # Pozostawiamy dla kompatybilności, ale będzie None
try:
    FONT = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
    BIG_FONT = FONT # Przypisanie tej samej czcionki, aby uniknąć AttributeError w game_manager.py
except pygame.error as e:
    print(f"Warning: Could not load system font '{config.FONT_NAME}'. Using default. Error: {e}")
    # Fallback to Pygame's default font if system font fails
    FONT = pygame.font.Font(None, config.FONT_SIZE_NORMAL + 5)
    BIG_FONT = FONT # Użycie tej samej czcionki awaryjnej

# Sound
CLICK_SOUND = None


def play_click_sound():
    pass