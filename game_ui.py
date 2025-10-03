# game_ui.py
import pygame
import pygame_menu
import config
import scoreboard


def create_custom_game_menu(parent_surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    """Tworzy podmenu dla trybu niestandardowego, zawierające suwaki i przycisk startu."""
    submenu_theme = pygame_menu.themes.THEME_DARK.copy()
    submenu = pygame_menu.Menu(
        "Tryb Niestandardowy",
        # ZMIANA: Używamy pełnych wymiarów powierzchni rodzica
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )

    submenu.add.label("Ustawienia Niestandardowe", font_size=40, margin=(0, 30))
# ... (reszta funkcji create_custom_game_menu bez zmian) ...
    # Rozmiar planszy (Range Slider)
    submenu.add.range_slider(
        "Rozmiar planszy",
        default=get_custom_setting_fn("size"),
        range_values=(config.MIN_BOARD_SIZE, config.MAX_BOARD_SIZE),
        increment=1,
        value_format=lambda _: str(int(get_custom_setting_fn("size"))),
        onchange=lambda val: update_custom_setting_fn("size", val)
    )

    # Liczba min (Range Slider)
    max_slider_mines_limit = config.MAX_BOARD_SIZE * config.MAX_BOARD_SIZE - 1
    submenu.add.range_slider(
        "Liczba min",
        default=get_custom_setting_fn("mines"),
        range_values=(config.MIN_MINES_CUSTOM, max_slider_mines_limit),
        increment=1,
        value_format=lambda _: str(int(get_custom_setting_fn("mines"))),
        onchange=lambda val: update_custom_setting_fn("mines", val)
    )

    # Przycisk startu
    submenu.add.button("Rozpocznij", lambda: start_game_fn("Niestandardowy"), margin=(0, 40))

    # Przycisk powrotu
    submenu.add.button("Wróć", pygame_menu.events.BACK)
    return submenu


def create_main_menu(surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu = pygame_menu.Menu(
        'Saper – Menu Główne',
        surface.get_width(),
        surface.get_height(),
        theme=menu_theme
    )

    menu.add.label("Wybierz poziom", font_size=40, margin=(0, 20))
    for level_name_key in config.DIFFICULTIES:
        menu.add.button(level_name_key, lambda lvl=level_name_key: start_game_fn(lvl))

    custom_sub_menu = create_custom_game_menu(
        surface,
        start_game_fn,
        get_custom_setting_fn,
        update_custom_setting_fn
    )
    menu.add.button("Tryb Niestandardowy", custom_sub_menu, margin=(0, 40))

    scoreboard_sub_menu = create_scoreboard_display_menu(surface)
    menu.add.button("Tablica wyników", scoreboard_sub_menu)

    menu.add.button("Wyjście", pygame_menu.events.EXIT)
    return menu


def create_scoreboard_display_menu(parent_surface):
    submenu_theme = pygame_menu.themes.THEME_DARK.copy()
    submenu = pygame_menu.Menu(
        "Tablica wyników",
        # ZMIANA: Używamy pełnych wymiarów powierzchni rodzica
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )
    high_scores_data = scoreboard.load_high_scores()

    levels_in_order = list(config.DIFFICULTIES.keys())
    if "Niestandardowy" in high_scores_data or not any(lvl in high_scores_data for lvl in config.DIFFICULTIES.keys()):
        # Dodaj "Niestandardowy" jeśli ma wyniki lub jeśli nie ma żadnych innych wyników, aby pokazać info
        if "Niestandardowy" not in levels_in_order:
            levels_in_order.append("Niestandardowy")

    found_any_scores = False
    for level_key in levels_in_order:
        scores_list = high_scores_data.get(level_key, [])
        is_defined_level = level_key in config.DIFFICULTIES.keys() or level_key == "Niestandardowy"

        if scores_list:
            found_any_scores = True
            submenu.add.label(f"{level_key}:", font_size=36, margin=(0, 10))
            for i, score_time in enumerate(scores_list):
                submenu.add.label(f"{i + 1}. {score_time:.2f} sek", font_size=28)
            submenu.add.vertical_margin(15)
        elif is_defined_level:  # Pokaż "Brak wyników" dla zdefiniowanych poziomów
            submenu.add.label(f"{level_key}: Brak wyników", font_size=30, margin=(0, 10))
            submenu.add.vertical_margin(15)

    if not found_any_scores and not any(high_scores_data.get(lvl) for lvl in levels_in_order):
        submenu.add.label("Brak zapisanych wyników.", font_size=30)

    submenu.add.button("Wróć", pygame_menu.events.BACK)
    return submenu


def display_end_game_menu(game_surface, game_won, level_played, final_time):
    # ... (kod funkcji bez zmian) ...
    title_text = "Wygrana!" if game_won else "Przegrana!"
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.title_font_color = config.GREEN if game_won else config.RED
    menu_theme.widget_font_color = config.WHITE

    menu_width, menu_height = game_surface.get_size()
    end_menu = pygame_menu.Menu(title_text, menu_width, menu_height, theme=menu_theme)

    end_menu.add.label(f"Poziom: {level_played}", font_size=30)
    end_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    end_menu.add.vertical_margin(30)

    action_result = ["menu"]

    def set_player_action(selected_action):
        action_result[0] = selected_action
        end_menu.disable()

    button_bg_color_restart = config.BLUE if not game_won else (70, 70, 90)
    end_menu.add.button("Restart", lambda: set_player_action("restart"), background_color=button_bg_color_restart)
    end_menu.add.button("Menu Główne", lambda: set_player_action("menu"))
    end_menu.add.button("Wyjście", lambda: set_player_action("exit"))

    end_menu.mainloop(game_surface)
    return action_result[0]