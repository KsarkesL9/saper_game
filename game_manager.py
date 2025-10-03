# game_manager.py
import pygame
import sys
import time
import config
import assets
import board_logic
import drawing
import scoreboard
import game_ui


def run_game_session(level_name_selected, cust_size, cust_mines, orig_screen_dims):
    current_level_name = level_name_selected
    if current_level_name in config.DIFFICULTIES:
        game_params = config.DIFFICULTIES[current_level_name]
        board_dimension = game_params["size"]
        num_mines_on_board = game_params["mines"]
    else:
        board_dimension = cust_size
        num_mines_on_board = cust_mines
        current_level_name = "Niestandardowy"

    # --- ZMIANA: Używamy stałego rozmiaru okna menu dla ekranu gry ---
    game_scr_width = config.SCREEN_WIDTH
    game_scr_height = config.SCREEN_HEIGHT
    active_game_screen = pygame.display.set_mode((game_scr_width, game_scr_height))
    pygame.display.set_caption(f"Saper – {current_level_name}")
    # -----------------------------------------------------------------

    # --- ZMIANA: Dynamiczne obliczanie rozmiaru kafelka i marginesów ---
    # 1. Oblicz maksymalny dostępny obszar dla planszy
    # Bierzemy mniejszy z wymiarów okna, aby plansza była kwadratowa i mieściła się w 80%
    available_size = min(game_scr_width, game_scr_height) * config.BOARD_AREA_PERCENTAGE

    # 2. Oblicz nowy CELL_SIZE
    # Dzielimy dostępny rozmiar przez wymiar planszy, aby uzyskać maksymalny rozmiar kafelka
    new_cell_size = int(available_size // board_dimension)

    # 3. Oblicz całkowity rozmiar planszy w pikselach
    board_pixel_width = board_dimension * new_cell_size
    board_pixel_height = board_dimension * new_cell_size

    # 4. Oblicz dynamiczne offsety (marginesy) dla wyśrodkowania planszy
    # Minimalny margines pionowy dla timera. Timer ma być na górze okna (offset_y = MIN_MARGIN)
    # Plansza powinna zaczynać się poniżej timera.

    # Timer zajmie ~FONT_SIZE_NORMAL wysokości. Wyznaczamy górną granicę planszy
    # na podstawie pozostałego obszaru po umieszczeniu timera.

    timer_height = assets.FONT.get_height()

    # Minimalny margines od góry, poniżej timera
    min_top_margin_for_board = timer_height + config.MIN_MARGIN * 2

    # Offset poziomy (wyśrodkowanie)
    offset_x = (game_scr_width - board_pixel_width) // 2
    offset_x = max(config.MIN_MARGIN, offset_x)

    # Offset pionowy: plansza powinna być wyśrodkowana w pozostałym miejscu, ale nie za nisko
    # W praktyce planszę po prostu umieszczamy poniżej minimalnego marginesu górnego
    offset_y = (game_scr_height - board_pixel_height) // 2
    # Zapewniamy, że plansza zaczyna się co najmniej za timerem + margines
    offset_y = max(min_top_margin_for_board, offset_y)
    # ---------------------------------------------------------------------

    game_clock = pygame.time.Clock()

    game_board, game_start_time, current_elapsed_time, cheat_active, game_is_lost, game_is_won, first_click_made = [None] * 7

    def reset_game_state():
        nonlocal game_board, game_start_time, current_elapsed_time, cheat_active, game_is_lost, game_is_won, first_click_made
        # Użyj board_dimension i num_mines_on_board, które są już ustawione dla poziomu
        game_board = board_logic.create_game_board(board_dimension, num_mines_on_board)
        game_start_time = time.time()
        current_elapsed_time = 0
        cheat_active = False
        game_is_lost = False
        game_is_won = False
        first_click_made = False  # Flaga dla bezpiecznego pierwszego kliknięcia

    reset_game_state()

    is_session_active = True
    while is_session_active:
        if not (game_is_lost or game_is_won):
            current_elapsed_time = time.time() - game_start_time

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_is_lost and not game_is_won:
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = evt.pos
                    # --- ZMIANA: Używamy nowego new_cell_size do obliczenia indeksu komórki ---
                    col_idx = (m_x - offset_x) // new_cell_size
                    row_idx = (m_y - offset_y) // new_cell_size
                    # -----------------------------------------------------------

                    if 0 <= col_idx < board_dimension and 0 <= row_idx < board_dimension:

                        assets.play_click_sound()  # Odtwórz dźwięk (jeśli jest)

                        if evt.button == 1:  # Lewy Przycisk
                            # --- Logika bezpiecznego pierwszego kliknięcia ---
                            if not first_click_made:
                                first_click_made = True
                                # Jeśli pierwszy klik trafił na minę, regeneruj planszę, aż będzie bezpiecznie
                                # Ta operacja zachowuje liczbę min, ale zmienia ich pozycje.
                                while game_board[row_idx][col_idx].has_mine:
                                    game_board = board_logic.create_game_board(board_dimension, num_mines_on_board)
                            # --- Koniec logiki bezpiecznego pierwszego kliknięcia ---

                            clicked_cell = game_board[row_idx][col_idx]  # Pobierz komórkę (może być z nowej planszy)

                            if not clicked_cell.flagged:  # Działaj tylko jeśli nieoflagowana
                                if clicked_cell.has_mine:  # Teraz to będzie prawdziwa przegrana
                                    clicked_cell.revealed = True
                                    for r in range(board_dimension):
                                        for c in range(board_dimension):
                                            if game_board[r][c].has_mine:
                                                game_board[r][c].revealed = True
                                    game_is_lost = True
                                else:
                                    board_logic.reveal_cell_recursive(game_board, row_idx, col_idx)
                                    if board_logic.check_win_condition(game_board):
                                        game_is_won = True
                                        # Logika zapisu przeniesiona niżej

                                if cheat_active and not (game_is_won or game_is_lost):
                                    board_logic.analyze_board_probabilities(game_board)

                        elif evt.button == 3:  # Prawy Przycisk
                            clicked_cell = game_board[row_idx][col_idx]  # Pobierz komórkę
                            if not clicked_cell.revealed:
                                clicked_cell.flagged = not clicked_cell.flagged
                                if cheat_active and not (game_is_won or game_is_lost):
                                    board_logic.analyze_board_probabilities(game_board)

                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_F1:
                        cheat_active = not cheat_active
                        if cheat_active and not (game_is_won or game_is_lost):
                            board_logic.analyze_board_probabilities(game_board)
                        else:  # Wyłączając cheat, wyczyść podpowiedzi
                            if not cheat_active:
                                for r_arr in game_board:
                                    for c_cell_item in r_arr: c_cell_item.probability = None

        active_game_screen.fill(config.BLACK)
        # --- ZMIANA: Przekazujemy offsety ORAZ new_cell_size do funkcji rysującej ---
        drawing.draw_game_board(active_game_screen, game_board, cheat_active, offset_x, offset_y, new_cell_size)

        if not (game_is_lost or game_is_won):
            # --- ZMIANA: Uaktualniamy pozycję timera (lewy górny róg) ---
            timer_surf = assets.FONT.render(f"Czas: {int(current_elapsed_time)}s", True, config.WHITE)
            # Stała pozycja w lewym górnym rogu z minimalnym marginesem
            active_game_screen.blit(timer_surf, (config.MIN_MARGIN, config.MIN_MARGIN))
            # -----------------------------------------------------------

        if game_is_won:
            status_text_surf = assets.BIG_FONT.render("WYGRANA!", True, config.GREEN)
            status_text_surf.set_colorkey(config.BLACK)  # Zapewniamy przezroczystość tła dla statusu
            active_game_screen.blit(status_text_surf,
                                    status_text_surf.get_rect(center=active_game_screen.get_rect().center))
        elif game_is_lost:
            status_text_surf = assets.BIG_FONT.render("PRZEGRANA!", True, config.RED)
            status_text_surf.set_colorkey(config.BLACK)  # Zapewniamy przezroczystość tła dla statusu
            active_game_screen.blit(status_text_surf,
                                    status_text_surf.get_rect(center=active_game_screen.get_rect().center))

        pygame.display.flip()
        game_clock.tick(30)

        if game_is_won or game_is_lost:
            pygame.time.wait(1000)

            # --- ZMIANA: Nowa logika obsługi wygranej ---
            if game_is_won and current_level_name in scoreboard.RANKED_LEVELS:
                # 1. Prosimy gracza o imię
                save_action, player_name = game_ui.display_name_input_menu(
                    active_game_screen,
                    current_elapsed_time
                )

                # 2. Jeśli gracz zdecydował się zapisać, zapisujemy
                if save_action == "save":
                    scoreboard.save_player_score(current_level_name, current_elapsed_time, player_name)
                    # Po zapisie przechodzimy do normalnego menu końca gry
                    player_choice = game_ui.display_end_game_menu(
                        active_game_screen,
                        game_is_won,
                        current_level_name,
                        current_elapsed_time
                    )
                else:
                    # Jeśli "skip" (nie zapisuj), przechodzimy od razu do menu
                    player_choice = "menu"

            else:
                # Standardowe menu końca gry dla przegranej lub trybu niestandardowego
                player_choice = game_ui.display_end_game_menu(
                    active_game_screen,
                    game_is_won,
                    current_level_name,
                    current_elapsed_time
                )
            # ----------------------------------------------

            # --- ZMIANA: Uproszczona obsługa wyboru gracza ---
            if player_choice == "restart":
                reset_game_state()
            elif player_choice == "menu":
                is_session_active = False
            elif player_choice == "exit":
                pygame.quit()
                sys.exit()
            # ------------------------------------------------

    pygame.display.set_mode(orig_screen_dims)
    pygame.display.set_caption("Saper – Wersja UI")