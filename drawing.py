# drawing.py
import pygame
import config
import assets  # For FONT


# Zmieniono sygnaturę, aby przyjmowała dynamiczny cell_size oraz offsety x i y.
def draw_game_board(screen, board, cheat_on, offset_x, offset_y, cell_size):
    size = len(board)

    # --- ZMIANA: Dynamiczne skalowanie czcionki dla liczb na planszy ---
    # Używamy rozmiaru ~60% cell_size dla optymalnej widoczności cyfr
    font_size_for_numbers = max(12, int(cell_size * 0.6))
    # Tworzymy tymczasowy obiekt czcionki SysFont
    try:
        numbers_font = pygame.font.SysFont(config.FONT_NAME, font_size_for_numbers)
    except pygame.error:
        numbers_font = pygame.font.Font(None, font_size_for_numbers)
    # ------------------------------------------------------------------

    for r in range(size):  # r for row
        for c in range(size):  # c for column
            cell_obj = board[r][c]
            rect = pygame.Rect(
                # Używamy przekazanych offsetów i cell_size
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size,
                cell_size
            )

            # Determine cell color
            cell_display_color = config.DARK_GRAY  # Default for unrevealed
            if cell_obj.revealed:
                cell_display_color = config.GRAY
            elif cheat_on and cell_obj.probability is not None:
                p = cell_obj.probability
                if p == 1.0:
                    cell_display_color = config.RED
                elif p == 0.0:
                    cell_display_color = config.GREEN
                elif p == 0.5:
                    cell_display_color = config.YELLOW
                else:
                    cell_display_color = config.BLUE  # For -1.0 (error/unknown) or other probabilities

            pygame.draw.rect(screen, cell_display_color, rect)
            pygame.draw.rect(screen, config.BLACK, rect, 1)  # Border

            # Draw content of the cell
            if cell_obj.revealed:
                if cell_obj.has_mine:
                    # Używamy dynamicznego cell_size do obliczenia rozmiaru kółka
                    pygame.draw.circle(screen, config.RED, rect.center, cell_size // 5)
                elif cell_obj.adjacent_mines > 0:
                    # --- ZMIANA: Używamy dynamicznej czcionki ---
                    text_surface = numbers_font.render(str(cell_obj.adjacent_mines), True, config.BLUE)
                    # -------------------------------------------
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
            elif cell_obj.flagged:
                # Simple green circle for flag
                # Używamy dynamicznego cell_size do obliczenia rozmiaru flagi
                pygame.draw.circle(screen, config.GREEN, rect.center, cell_size // 7)