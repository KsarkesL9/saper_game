# saper.py
import pygame
import sys
import config
import assets
import game_ui
import game_manager

_current_custom_settings = {
    "size": config.INITIAL_CUSTOM_SIZE,
    "mines": config.INITIAL_CUSTOM_MINES
}


def update_global_custom_setting(setting_key, new_value_str_or_int):
    global _current_custom_settings

    try:
        value = int(new_value_str_or_int)
    except ValueError:
        print(f"Błąd: Nieprawidłowa wartość dla ustawienia niestandardowego: {new_value_str_or_int}")
        return  # Ignoruj nieprawidłowe wartości

    if setting_key == "size":
        # Ogranicz rozmiar planszy
        value = max(config.MIN_BOARD_SIZE, min(value, config.MAX_BOARD_SIZE))
        _current_custom_settings["size"] = value

        # Dostosuj liczbę min, jeśli obecna jest nieprawidłowa dla nowego rozmiaru
        # Liczba min musi być > 0 i < (rozmiar * rozmiar)
        max_possible_mines = (_current_custom_settings["size"] * _current_custom_settings["size"]) - 1
        # Upewnij się, że max_possible_mines jest co najmniej MIN_MINES_CUSTOM (np. dla małych plansz)
        max_possible_mines = max(config.MIN_MINES_CUSTOM, max_possible_mines)

        _current_custom_settings["mines"] = max(config.MIN_MINES_CUSTOM,
                                                min(_current_custom_settings["mines"], max_possible_mines))

    elif setting_key == "mines":
        current_board_size = _current_custom_settings["size"]
        max_possible_mines = (current_board_size * current_board_size) - 1
        max_possible_mines = max(config.MIN_MINES_CUSTOM, max_possible_mines)

        _current_custom_settings["mines"] = max(config.MIN_MINES_CUSTOM, min(value, max_possible_mines))


def get_global_custom_setting(setting_key):
    return _current_custom_settings[setting_key]


def initiate_game_level(selected_level_name):
    original_menu_screen_dimensions = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    # Upewnij się, że niestandardowe ustawienia są poprawne przed startem gry
    # (chociaż update_global_custom_setting powinien to już robić)
    if selected_level_name == "Niestandardowy":
        size = _current_custom_settings["size"]
        mines = _current_custom_settings["mines"]
        max_mines = (size * size) - 1
        _current_custom_settings["mines"] = max(config.MIN_MINES_CUSTOM, min(mines, max_mines))

    game_manager.run_game_session(
        selected_level_name,
        _current_custom_settings["size"],
        _current_custom_settings["mines"],
        original_menu_screen_dimensions
    )


def main():
    pygame.init()
    # pygame.mixer.init() # Przeniesione do assets.py lub usunięte jeśli nie ma dźwięku

    _ = assets.FONT  # Upewnij się, że zasoby (czcionki) są załadowane

    main_display_surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Saper – Wersja UI")

    saper_main_menu = game_ui.create_main_menu(
        main_display_surface,
        initiate_game_level,
        get_global_custom_setting,
        update_global_custom_setting
    )

    saper_main_menu.mainloop(main_display_surface)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()