import pygame
import pygame_menu
import pygame_menu.locals
import config
import scoreboard


def create_custom_game_menu(parent_surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    submenu_theme = pygame_menu.themes.THEME_DARK.copy()
    submenu_theme.background_color = config.DARK_NAVY
    submenu_theme.widget_font_color = config.WHITE
    submenu_theme.selection_color = config.CYAN
    submenu_theme.title_font_color = config.ELECTRIC_BLUE

    submenu = pygame_menu.Menu(
        "Tryb Niestandardowy",
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )

    submenu.add.label("Ustawienia Niestandardowe", font_size=40, margin=(0, 20))
    submenu.add.vertical_margin(30)

    def validate_settings_and_update_ui():
        size = get_custom_setting_fn("size")
        mines = get_custom_setting_fn("mines")
        max_mines = (size * size) - 1

        validation_label = submenu.get_widget("validation_label")
        start_button = submenu.get_widget("start_button")

        if mines > max_mines:
            validation_label.set_title(f"Za dużo min! (maks. dla tej planszy: {max_mines})")
            validation_label.update_font({'color': config.RED_ACCENT})
            start_button.readonly = True
        else:
            validation_label.set_title("")
            validation_label.update_font({'color': config.WHITE})
            start_button.readonly = False

    def on_size_change(value):
        update_custom_setting_fn("size", value)
        validate_settings_and_update_ui()

    def on_mines_change(value):
        update_custom_setting_fn("mines", value)
        validate_settings_and_update_ui()

    submenu.add.range_slider(
        "Rozmiar planszy",
        default=get_custom_setting_fn("size"),
        range_values=(config.MIN_BOARD_SIZE, config.MAX_BOARD_SIZE),
        increment=1,
        onchange=on_size_change,
        value_format=lambda x: str(int(x))
    )

    submenu.add.range_slider(
        "Liczba min",
        default=get_custom_setting_fn("mines"),
        range_values=(config.MIN_MINES_CUSTOM, 600),
        increment=1,
        onchange=on_mines_change,
        value_format=lambda x: str(int(x))
    )

    submenu.add.label("", label_id="validation_label", font_size=24, margin=(0, 20))
    submenu.add.button("Rozpocznij", lambda: start_game_fn("Niestandardowy"), button_id="start_button", margin=(0, 20),
                       background_color=config.GREEN_ACCENT)
    submenu.add.button("Wróć", pygame_menu.events.BACK)

    validate_settings_and_update_ui()
    return submenu


def create_main_menu(surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.background_color = config.DARK_NAVY
    menu_theme.widget_font_color = config.WHITE
    menu_theme.selection_color = config.CYAN
    menu_theme.title_font_color = config.ELECTRIC_BLUE

    menu = pygame_menu.Menu(
        '',
        surface.get_width(),
        surface.get_height(),
        theme=menu_theme
    )

    menu.add.label(
        "MineSat",
        font_name=config.FONT_NAME,
        font_size=120,
        font_color=config.ELECTRIC_BLUE
    )
    menu.add.vertical_margin(50)

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

    static_scoreboard = create_scoreboard_display_menu(surface)
    menu.add.button("Tablica wyników", static_scoreboard)

    menu.add.button("Wyjście", pygame_menu.events.EXIT, background_color=config.RED_ACCENT)
    return menu


def create_scoreboard_display_menu(parent_surface):
    submenu_theme = pygame_menu.themes.THEME_DARK.copy()
    submenu_theme.background_color = config.DARK_NAVY
    submenu_theme.widget_font_color = config.WHITE
    submenu_theme.selection_color = config.CYAN
    submenu_theme.title_font_color = config.ELECTRIC_BLUE

    submenu = pygame_menu.Menu(
        "Tablica wyników",
        parent_surface.get_width(),
        parent_surface.get_height(),
        theme=submenu_theme
    )
    high_scores_data = scoreboard.load_high_scores()
    levels_in_order = list(config.DIFFICULTIES.keys())
    found_any_scores = False

    for level_key in levels_in_order:
        scores_list = high_scores_data.get(level_key, [])
        is_defined_level = level_key in config.DIFFICULTIES.keys()

        if scores_list:
            found_any_scores = True
            submenu.add.label(f"{level_key}:", font_size=36, margin=(0, 10))
            for i, score_entry in enumerate(scores_list):
                time = score_entry.get("time", 0.0)
                name = score_entry.get("name", "Brak Im.")
                submenu.add.label(f"{i + 1}. {time:.2f} sek ({name})", font_size=28)
            submenu.add.vertical_margin(15)
        elif is_defined_level:
            submenu.add.label(f"{level_key}: Brak wyników", font_size=30, margin=(0, 10))
            submenu.add.vertical_margin(15)

    if not found_any_scores and not any(high_scores_data.get(lvl) for lvl in levels_in_order):
        submenu.add.label("Brak zapisanych wyników.", font_size=30)

    submenu.add.button("Wróć", pygame_menu.events.BACK)
    return submenu


def display_name_input_menu(game_surface, final_time):
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.background_color = config.DARK_NAVY
    menu_theme.title_font_color = config.GREEN_ACCENT
    menu_theme.widget_font_color = config.WHITE
    menu_theme.selection_color = config.CYAN

    input_menu = pygame_menu.Menu("Nowy rekord!", game_surface.get_width(), game_surface.get_height(), theme=menu_theme)

    action_result = ["skip", None]

    def set_player_action_and_disable(action, name=None):
        nonlocal action_result
        action_result = [action, name]
        input_menu.disable()

    input_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    input_menu.add.vertical_margin(20)

    name_input = input_menu.add.text_input('Imię: ', maxchar=10, input_underline='_', font_size=30, default='Anon')
    input_menu.add.vertical_margin(30)
    input_menu.add.button("Zapisz wynik", lambda: set_player_action_and_disable("save", name_input.get_value()),
                          background_color=config.GREEN_ACCENT)
    input_menu.add.button("Nie zapisuj", lambda: set_player_action_and_disable("skip"))

    input_menu.mainloop(game_surface)
    return action_result


def display_end_game_menu(game_surface, game_won, level_played, final_time):
    title_text = "Wygrana!" if game_won else "Przegrana!"
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.background_color = config.DARK_NAVY
    menu_theme.title_font_color = config.GREEN_ACCENT if game_won else config.RED_ACCENT
    menu_theme.widget_font_color = config.WHITE
    menu_theme.selection_color = config.CYAN

    end_menu = pygame_menu.Menu(title_text, game_surface.get_width(), game_surface.get_height(), theme=menu_theme)

    end_menu.add.label(f"Poziom: {level_played}", font_size=30)
    end_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    end_menu.add.vertical_margin(30)

    action_result = ["menu"]

    def set_player_action(selected_action):
        action_result[0] = selected_action
        end_menu.disable()

    end_menu.add.button("Restart", lambda: set_player_action("restart"), background_color=config.LIGHT_NAVY)
    end_menu.add.button("Menu Główne", lambda: set_player_action("menu"))
    end_menu.add.button("Wyjście", lambda: set_player_action("exit"), background_color=config.RED_ACCENT)

    end_menu.mainloop(game_surface)
    return action_result[0]