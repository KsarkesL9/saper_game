import pygame
import config
import math


def draw_game_board(screen, board, cheat_on, offset_x, offset_y, cell_size):
    size = len(board)
    font_size_for_numbers = max(12, int(cell_size * 0.6))

    try:
        numbers_font = pygame.font.SysFont(config.FONT_NAME, font_size_for_numbers, bold=True)
    except pygame.error:
        numbers_font = pygame.font.Font(None, font_size_for_numbers)

    for r in range(size):
        for c in range(size):
            cell_obj = board[r][c]
            rect = pygame.Rect(
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size,
                cell_size
            )

            shadow_rect = rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, config.BLACK, shadow_rect, border_radius=8)

            if cell_obj.revealed:
                cell_display_color = config.MID_NAVY
            else:
                cell_display_color = config.LIGHT_NAVY

            if cheat_on and cell_obj.probability is not None and not cell_obj.revealed:
                p = cell_obj.probability
                if p == 1.0:
                    cell_display_color = config.MAGENTA
                elif p == 0.0:
                    cell_display_color = config.GREEN_ACCENT
                elif p == 0.5:
                    cell_display_color = config.YELLOW_ACCENT

            pygame.draw.rect(screen, cell_display_color, rect, border_radius=8)
            pygame.draw.rect(screen, config.DARK_NAVY, rect, 2, border_radius=8)

            if cell_obj.revealed:
                if cell_obj.has_mine:
                    center = rect.center
                    radius = cell_size * 0.25
                    pygame.draw.circle(screen, config.RED_ACCENT, center, radius)
                    pygame.draw.line(screen, config.WHITE, (center[0], center[1] - radius),
                                     (center[0], center[1] - radius - 5), 3)
                elif cell_obj.adjacent_mines > 0:
                    text_surface = numbers_font.render(str(cell_obj.adjacent_mines), True, config.WHITE)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
            elif cell_obj.flagged:
                points = [
                    (rect.centerx - cell_size * 0.2, rect.centery - cell_size * 0.25),
                    (rect.centerx + cell_size * 0.25, rect.centery),
                    (rect.centerx - cell_size * 0.2, rect.centery + cell_size * 0.25)
                ]
                pygame.draw.polygon(screen, config.CYAN, points)
                pygame.draw.line(screen, config.DARK_NAVY, rect.midbottom,
                                 (rect.centerx, rect.centery - cell_size * 0.25), 3)


def draw_ingame_buttons(screen, reset_button_rect, exit_button_rect):
    mouse_pos = pygame.mouse.get_pos()

    try:
        button_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL, bold=True)
    except pygame.error:
        button_font = pygame.font.Font(None, config.FONT_SIZE_SMALL)

    buttons_to_draw = {
        "Reset": reset_button_rect,
        "Wyjście": exit_button_rect
    }

    for text, rect in buttons_to_draw.items():
        if rect.collidepoint(mouse_pos):
            button_color = config.BUTTON_HOVER_COLOR
        else:
            button_color = config.BUTTON_COLOR

        pygame.draw.rect(screen, button_color, rect, border_radius=8)
        pygame.draw.rect(screen, config.DARK_NAVY, rect, 2, border_radius=8)

        text_surf = button_font.render(text, True, config.BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)