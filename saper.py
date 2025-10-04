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
        _current_custom_settings[setting_key] = value
    except (ValueError, TypeError):
        pass


def get_global_custom_setting(setting_key):
    return _current_custom_settings[setting_key]


def initiate_game_level(selected_level_name, menu):
    menu.disable()

    original_menu_screen_dimensions = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    size = _current_custom_settings["size"]
    mines = _current_custom_settings["mines"]

    game_manager.run_game_session(
        selected_level_name,
        size,
        mines,
        original_menu_screen_dimensions
    )

    menu.enable()


def main():
    pygame.init()
    _ = assets.FONT

    main_display_surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Saper – Wersja UI")

    saper_main_menu = game_ui.create_main_menu(
        main_display_surface,
        lambda level: initiate_game_level(level, saper_main_menu),
        get_global_custom_setting,
        update_global_custom_setting
    )

    saper_main_menu.mainloop(main_display_surface)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()