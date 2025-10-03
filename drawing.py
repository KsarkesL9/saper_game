# drawing.py
import pygame
import config
import assets  # For FONT


def draw_game_board(screen, board, cheat_on):
    size = len(board)
    for r in range(size):  # r for row
        for c in range(size):  # c for column
            cell_obj = board[r][c]
            rect = pygame.Rect(
                config.MARGIN + c * config.CELL_SIZE,
                config.MARGIN + r * config.CELL_SIZE,
                config.CELL_SIZE,
                config.CELL_SIZE
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
                    pygame.draw.circle(screen, config.RED, rect.center, config.CELL_SIZE // 5)  # Adjusted bomb size
                elif cell_obj.adjacent_mines > 0:
                    text_surface = assets.FONT.render(str(cell_obj.adjacent_mines), True, config.BLUE)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
            elif cell_obj.flagged:
                # Simple green circle for flag
                pygame.draw.circle(screen, config.GREEN, rect.center, config.CELL_SIZE // 7)  # Adjusted flag size