import pygame
import config
import math


def _lerp(a, b, t):
    return a + (b - a) * max(0.0, min(1.0, t))

def _lerp_color(c1, c2, t):
    return (
        int(_lerp(c1[0], c2[0], t)),
        int(_lerp(c1[1], c2[1], t)),
        int(_lerp(c1[2], c2[2], t)),
    )

def _draw_linear_gradient(surf, rect, c_top, c_bottom):
    x, y, w, h = rect
    if h <= 0:
        return
    for i in range(h):
        t = i / max(1, h - 1)
        color = _lerp_color(c_top, c_bottom, t)
        pygame.draw.line(surf, color, (x, y + i), (x + w, y + i))

def _glass_card(surf, rect, fill_rgba=(255, 255, 255, 18), outline=(255, 255, 255), radius=10):
    x, y, w, h = rect
    glass = pygame.Surface((w, h), pygame.SRCALPHA)
    glass.fill(fill_rgba)
    surf.blit(glass, (x, y))
    pygame.draw.rect(surf, outline, rect, 1, border_radius=radius)

NUM_COLORS = {
    1: (80, 200, 255),
    2: (120, 220, 160),
    3: (255, 170, 120),
    4: (140, 140, 255),
    5: (255, 120, 150),
    6: (100, 220, 220),
    7: (250, 240, 140),
    8: (180, 180, 180),
}

DARK = getattr(config, "DARK_NAVY", (21, 28, 41))
MID = getattr(config, "MID_NAVY", (33, 42, 63))
LIGHT = getattr(config, "LIGHT_NAVY", (50, 63, 94))
ELECTRIC = getattr(config, "ELECTRIC_BLUE", (125, 249, 255))
GREEN = getattr(config, "GREEN_ACCENT", (0, 200, 150))
MAGENTA = getattr(config, "MAGENTA", (255, 0, 255))
YELLOW = getattr(config, "YELLOW_ACCENT", (255, 220, 0))
WHITE = getattr(config, "WHITE", (240, 240, 240))
BLACK = getattr(config, "BLACK", (10, 10, 10))


def draw_top_bar(screen, title_text, elapsed_seconds, cheat_on):
    width = screen.get_width()
    height = 72
    bar_rect = pygame.Rect(0, 0, width, height)

    c1 = (12, 16, 28)
    c2 = (18, 26, 44)
    _draw_linear_gradient(screen, bar_rect, c1, c2)

    glow_rect = pygame.Rect(0, height-6, width, 6)
    _draw_linear_gradient(screen, glow_rect, (0,0,0), (0,80,120))

    try:
        title_font = pygame.font.SysFont(getattr(config, "FONT_NAME", "Segoe UI"), 28, bold=True)
    except pygame.error:
        title_font = pygame.font.Font(None, 28)

    title_surface = title_font.render(title_text, True, ELECTRIC)
    screen.blit(title_surface, (20, bar_rect.centery - title_surface.get_height()//2))

    try:
        timer_font = pygame.font.SysFont(getattr(config, "FONT_NAME", "Segoe UI"), 22)
    except pygame.error:
        timer_font = pygame.font.Font(None, 22)

    timer_surface = timer_font.render(f"Czas: {int(elapsed_seconds)} s", True, WHITE)
    screen.blit(timer_surface, (width//2 - timer_surface.get_width()//2, bar_rect.centery - timer_surface.get_height()//2))

    led_color = GREEN if cheat_on else (120, 120, 140)
    label = timer_font.render("Asystent (F1)", True, WHITE)
    lx = width - 20 - label.get_width() - 24
    ly = bar_rect.centery - label.get_height()//2
    pygame.draw.circle(screen, BLACK, (lx, ly + label.get_height()//2), 10)
    pygame.draw.circle(screen, led_color, (lx, ly + label.get_height()//2), 8)
    screen.blit(label, (lx + 18, ly))


def _prob_to_color(p):
    if p is None or p < 0:
        return None
    if p <= 0.5:
        t = p / 0.5
        return _lerp_color(GREEN, YELLOW, t)
    else:
        t = (p - 0.5) / 0.5
        return _lerp_color(YELLOW, MAGENTA, t)


def draw_game_board(screen, board, cheat_on, offset_x, offset_y, cell_size):
    size = len(board)
    font_size_for_numbers = max(14, int(cell_size * 0.56))

    try:
        numbers_font = pygame.font.SysFont(getattr(config, "FONT_NAME", "Segoe UI"), font_size_for_numbers, bold=True)
    except pygame.error:
        numbers_font = pygame.font.Font(None, font_size_for_numbers)

    mouse_pos = pygame.mouse.get_pos()

    for r in range(size):
        for c in range(size):
            cell_obj = board[r][c]
            rect = pygame.Rect(
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size,
                cell_size
            )

            shadow_rect = rect.copy(); shadow_rect.x += 3; shadow_rect.y += 3
            pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=10)

            if cell_obj.revealed:
                top, bottom = (42, 54, 82), (32, 42, 64)
            else:
                top, bottom = (58, 74, 108), (44, 56, 86)
            _draw_linear_gradient(screen, rect, top, bottom)
            _glass_card(screen, rect, fill_rgba=(255,255,255,12), radius=10)
            pygame.draw.rect(screen, MID, rect, 2, border_radius=10)

            if cheat_on and (not cell_obj.revealed) and getattr(cell_obj, "probability", None) is not None:
                col = _prob_to_color(cell_obj.probability)
                if col is not None:
                    overlay = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    overlay.fill((*col, 70))
                    screen.blit(overlay, (rect.x, rect.y))

            if cell_obj.revealed:
                if getattr(cell_obj, "has_mine", False):
                    center = rect.center
                    radius = int(cell_size * 0.25)
                    pygame.draw.circle(screen, (255, 70, 120), center, radius)
                    pygame.draw.line(screen, WHITE, (center[0], center[1] - radius), (center[0], center[1] - radius - 5), 3)
                elif getattr(cell_obj, "adjacent_mines", 0) > 0:
                    num = cell_obj.adjacent_mines
                    color = NUM_COLORS.get(num, WHITE)
                    text_surface = numbers_font.render(str(num), True, color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
            elif getattr(cell_obj, "flagged", False):
                pole = [
                    (rect.centerx - cell_size * 0.18, rect.centery - cell_size * 0.22),
                    (rect.centerx + cell_size * 0.22, rect.centery - cell_size * 0.05),
                    (rect.centerx - cell_size * 0.18, rect.centery + cell_size * 0.12)
                ]
                pygame.draw.polygon(screen, (0, 240, 255), pole)
                pygame.draw.line(screen, MID, rect.midbottom, (rect.centerx, rect.centery - cell_size * 0.26), 3)

            if rect.collidepoint(mouse_pos):
                hover = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                hover.fill((255, 255, 255, 18))
                screen.blit(hover, (rect.x, rect.y))


def draw_ingame_buttons(screen, reset_button_rect, exit_button_rect):
    mouse_pos = pygame.mouse.get_pos()

    try:
        button_font = pygame.font.SysFont(getattr(config, "FONT_NAME", "Segoe UI"), getattr(config, "FONT_SIZE_SMALL", 24), bold=True)
    except pygame.error:
        button_font = pygame.font.Font(None, 24)

    def _draw_button(rect, label):
        is_hover = rect.collidepoint(mouse_pos)
        base_top, base_bot = ((58, 74, 108), (44, 56, 86)) if not is_hover else ((72, 96, 138), (56, 74, 110))
        _draw_linear_gradient(screen, rect, base_top, base_bot)
        _glass_card(screen, rect, fill_rgba=(255,255,255,18), radius=10)
        pygame.draw.rect(screen, MID, rect, 2, border_radius=10)

        text_surf = button_font.render(label, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    _draw_button(reset_button_rect, "Reset")
    _draw_button(exit_button_rect, "Wyjście")