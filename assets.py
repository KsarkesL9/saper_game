import pygame
import config

pygame.font.init()
pygame.mixer.init()

FONT = None
BIG_FONT = None
try:
    FONT = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
    BIG_FONT = FONT
except pygame.error as e:
    print(f"Warning: Could not load system font '{config.FONT_NAME}'. Using default. Error: {e}")
    FONT = pygame.font.Font(None, config.FONT_SIZE_NORMAL + 5)
    BIG_FONT = FONT

CLICK_SOUND = None

def play_click_sound():
    pass