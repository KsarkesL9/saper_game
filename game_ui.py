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
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )

    submenu.add.label("Ustawienia Niestandardowe", font_size=40, margin=(0, 30))

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

    # ZAMIENIAMY istniejącą create_and_open_scoreboard_dynamically na to:
    def create_and_open_scoreboard_dynamically():
        # Tworzymy menu rankingów zawsze na świeżo i uruchamiamy jego pętlę.
        new_scoreboard_menu = create_scoreboard_display_menu(surface)
        try:
            new_scoreboard_menu.mainloop(surface)
        except Exception as e:
            print("Błąd przy otwieraniu tablicy wyników:", e)
        # Nie zwracamy Menu — callback kończy się po zamknięciu podmenu.
        return None

    static_scoreboard = create_scoreboard_display_menu(surface)
    menu.add.button("Tablica wyników", static_scoreboard)
    # -----------------------------------------------------------------------------

    menu.add.button("Wyjście", pygame_menu.events.EXIT)
    return menu


def create_scoreboard_display_menu(parent_surface):
    submenu_theme = pygame_menu.themes.THEME_DARK.copy()
    submenu = pygame_menu.Menu(
        "Tablica wyników",
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )
    # Ładowanie wyników następuje ZA KAŻDYM RAZEM, gdy menu jest tworzone (poprawne)
    high_scores_data = scoreboard.load_high_scores()

    # Wyświetlamy tylko rankingowe poziomy
    levels_in_order = list(config.DIFFICULTIES.keys())

    found_any_scores = False
    for level_key in levels_in_order:
        scores_list = high_scores_data.get(level_key, [])
        is_defined_level = level_key in config.DIFFICULTIES.keys()

        if scores_list:
            found_any_scores = True
            submenu.add.label(f"{level_key}:", font_size=36, margin=(0, 10))
            # Wyświetlamy czas ORAZ imię gracza
            for i, score_entry in enumerate(scores_list):
                time = score_entry.get("time", 0.0)
                name = score_entry.get("name", "Brak Im.")
                submenu.add.label(f"{i + 1}. {time:.2f} sek ({name})", font_size=28)
            submenu.add.vertical_margin(15)
        elif is_defined_level:  # Pokaż "Brak wyników" dla zdefiniowanych poziomów
            submenu.add.label(f"{level_key}: Brak wyników", font_size=30, margin=(0, 10))
            submenu.add.vertical_margin(15)

    if not found_any_scores and not any(high_scores_data.get(lvl) for lvl in levels_in_order):
        submenu.add.label("Brak zapisanych wyników.", font_size=30)

    submenu.add.button("Wróć", pygame_menu.events.BACK)
    return submenu


def display_name_input_menu(game_surface, final_time):
    """Wyświetla menu do wprowadzenia imienia gracza i opcje zapisu/rezygnacji."""
    title_text = "Nowy rekord!"
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.title_font_color = config.GREEN
    menu_theme.widget_font_color = config.WHITE

    menu_width, menu_height = game_surface.get_size()
    input_menu = pygame_menu.Menu(title_text, menu_width, menu_height, theme=menu_theme)

    # Przechowuje wynik akcji: ["save", "Imię Gracza"] lub ["skip", None]
    action_result = ["skip", None]

    def set_player_action_and_disable(action, name=None):
        nonlocal action_result
        action_result = [action, name]
        input_menu.disable()

    input_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    input_menu.add.vertical_margin(20)

    # Widget do wprowadzania imienia
    name_input = input_menu.add.text_input(
        'Imię: ',
        maxchar=10,
        input_underline='_',
        font_size=30,
        default='Anon'
    )

    input_menu.add.vertical_margin(30)

    # Przycisk "Zapisz" - pobiera wprowadzone imię
    input_menu.add.button("Zapisz wynik",
                          lambda: set_player_action_and_disable("save", name_input.get_value()))

    # Przycisk "Nie zapisuj" - wychodzi do menu
    input_menu.add.button("Nie zapisuj (Wróć do menu)",
                          lambda: set_player_action_and_disable("skip"))

    input_menu.mainloop(game_surface)
    return action_result


def display_end_game_menu(game_surface, game_won, level_played, final_time):
    # ... (cały kod display_end_game_menu bez zmian) ...
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