import pygame
import pygame_menu
import pygame_menu.locals
import config
import scoreboard

# ------------- helpers (safe defaults) -------------
def C(name, default):
    return getattr(config, name, default)

DARK_NAVY = C("DARK_NAVY", (21, 28, 41))
MID_NAVY = C("MID_NAVY", (33, 42, 63))
LIGHT_NAVY = C("LIGHT_NAVY", (50, 63, 94))
WHITE = C("WHITE", (240, 240, 240))
BLACK = C("BLACK", (10, 10, 10))
ELECTRIC = C("ELECTRIC_BLUE", (125, 249, 255))
CYAN = C("CYAN", (0, 255, 255))
GREEN = C("GREEN_ACCENT", (0, 200, 150))
RED = C("RED_ACCENT", (255, 80, 100))
YELLOW = C("YELLOW_ACCENT", (255, 220, 0))
FONT_NAME = C("FONT_NAME", "Segoe UI")

def _draw_linear_gradient(surf, rect, c_top, c_bottom):
    x, y, w, h = rect
    if h <= 0:
        return
    for i in range(h):
        t = i / max(1, h - 1)
        color = (
            int(c_top[0] + (c_bottom[0] - c_top[0]) * t),
            int(c_top[1] + (c_bottom[1] - c_top[1]) * t),
            int(c_top[2] + (c_bottom[2] - c_top[2]) * t),
        )
        pygame.draw.line(surf, color, (x, y + i), (x + w, y + i))

def _glass_panel(surf, rect, border_color=(255,255,255), alpha=28, radius=18):
    x,y,w,h = rect
    panel = pygame.Surface((w,h), pygame.SRCALPHA)
    panel.fill((255,255,255, alpha))
    surf.blit(panel, (x,y))
    pygame.draw.rect(surf, border_color, rect, 1, border_radius=radius)

def _menu_bgfun(surface):
    surface.fill(DARK_NAVY)
    _draw_linear_gradient(surface, surface.get_rect(), (16,22,34), (26,36,58))
    glow = pygame.Surface((surface.get_width(), 8), pygame.SRCALPHA)
    glow.fill((0, 160, 220, 120))
    surface.blit(glow, (0, 72))
    _glass_panel(surface, pygame.Rect(20, 16, surface.get_width()-40, 56),
                 border_color=(200,220,255), alpha=18, radius=16)

# unified theme
def _neo_theme():
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.background_color = DARK_NAVY
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    theme.title_background_color = (30, 42, 64)
    theme.title_font = FONT_NAME
    theme.title_font_color = ELECTRIC
    theme.title_font_size = 42
    theme.widget_font = FONT_NAME
    theme.widget_font_color = WHITE

    effect = pygame_menu.widgets.HighlightSelection(border_width=2, margin_x=6, margin_y=4)
    effect.set_color(CYAN)
    theme.widget_selection_effect = effect
    theme.selection_color = CYAN

    theme.widget_margin = (0, 14)
    theme.widget_padding = 12
    theme.widget_background_color = (40,54,82)
    theme.widget_shadow = True
    theme.widget_shadow_position = pygame_menu.locals.POSITION_SOUTHEAST
    theme.widget_shadow_offset = 3
    theme.widget_border_color = (90, 120, 170)
    theme.widget_border_width = 1
    return theme

# ------------- Submenus -------------
def create_custom_game_menu(parent_surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    theme = _neo_theme()
    submenu = pygame_menu.Menu(
        title="Tryb niestandardowy",
        width=parent_surface.get_width(),
        height=parent_surface.get_height(),
        theme=theme
    )

    start_btn_holder = [None]

    def validate_settings_and_update_ui():
        size = int(get_custom_setting_fn("size"))
        mines = int(get_custom_setting_fn("mines"))
        max_mines = size*size - 1
        start_btn = start_btn_holder[0]
        validation_label = submenu.get_widget("validation_label")

        if mines > max_mines or mines < 1:
            validation_label.set_title(f"Niepoprawna liczba min (1 - {max_mines}).")
            validation_label.update_font({'color': RED})
            if start_btn: start_btn.readonly = True
        else:
            validation_label.set_title("")
            validation_label.update_font({'color': WHITE})
            if start_btn: start_btn.readonly = False

    def on_size_change(value):
        update_custom_setting_fn("size", value)
        validate_settings_and_update_ui()

    def on_mines_change(value):
        update_custom_setting_fn("mines", value)
        validate_settings_and_update_ui()

    submenu.add.label("Ustawienia planszy", font_size=36, font_color=ELECTRIC)
    submenu.add.vertical_margin(15)

    submenu.add.range_slider(
        "Rozmiar planszy",
        default=get_custom_setting_fn("size"),
        range_values=(C("MIN_BOARD_SIZE", 4), C("MAX_BOARD_SIZE", 30)),
        increment=1,
        value_format=lambda x: str(int(x)),
        onchange=on_size_change
    )
    submenu.add.range_slider(
        "Liczba min",
        default=get_custom_setting_fn("mines"),
        range_values=(C("MIN_MINES_CUSTOM", 1), 999),
        increment=1,
        value_format=lambda x: str(int(x)),
        onchange=on_mines_change
    )
    submenu.add.label("", label_id="validation_label", font_size=24)
    submenu.add.vertical_margin(10)

    start_button = submenu.add.button(
        "Start",
        lambda: (start_game_fn("Niestandardowy"), submenu.disable()),
        background_color=GREEN
    )
    start_btn_holder[0] = start_button
    submenu.add.button("Wróć", pygame_menu.events.BACK)

    submenu.mainloop = (lambda *args, **kwargs:
                        pygame_menu.Menu.mainloop(submenu, parent_surface,
                                                  bgfun=lambda: _menu_bgfun(parent_surface)))
    validate_settings_and_update_ui()
    return submenu


def create_scoreboard_display_menu(parent_surface):
    theme = _neo_theme()
    submenu = pygame_menu.Menu(
        title="Tablica wyników",
        width=parent_surface.get_width(),
        height=parent_surface.get_height(),
        theme=theme
    )

    levels = list(C("DIFFICULTIES", {}).keys())
    if not levels:
        levels = ["Łatwy", "Średni", "Trudny", "Ekspert"]

    high_scores_data = scoreboard.load_high_scores()

    table = submenu.add.table(table_id="scores_table", font_size=28)
    table.default_cell_padding = 10
    table.default_row_background_color = (38, 50, 78)

    def render_table_for_level(level_name):
        table.clear()
        header = table.add_row(["#", "Imię", "Czas [s]"], cell_align=pygame_menu.locals.ALIGN_CENTER, cell_font_size=30)
        header.background_color = (50, 65, 95)

        scores_for_level = high_scores_data.get(level_name, [])
        if not scores_for_level:
            table.add_row(["—", "Brak wyników", "—"], cell_align=pygame_menu.locals.ALIGN_CENTER)
        else:
            sorted_scores = sorted(scores_for_level, key=lambda x: x.get("time", 0))[:5]
            for i, score in enumerate(sorted_scores, 1):
                name = score.get("name", "Anon")
                time_val = f'{score.get("time", 0):.2f}'
                table.add_row([str(i), name, time_val], cell_align=pygame_menu.locals.ALIGN_CENTER)

    def on_level_change(selected_item, level_name):
        render_table_for_level(level_name)

    submenu.add.selector(
        "Poziom: ",
        [(lvl, lvl) for lvl in levels],
        onchange=on_level_change
    )
    submenu.add.vertical_margin(20)

    render_table_for_level(levels[0]) # Initial table render

    submenu.add.vertical_margin(20)
    submenu.add.button("Wróć", pygame_menu.events.BACK)

    submenu.mainloop = (lambda *args, **kwargs:
                        pygame_menu.Menu.mainloop(submenu, parent_surface,
                                                  bgfun=lambda: _menu_bgfun(parent_surface)))
    return submenu


# ------------- Main menu -------------
def create_main_menu(surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn):
    theme = _neo_theme()
    menu = pygame_menu.Menu(
        title="MineSat Neo",
        width=surface.get_width(),
        height=surface.get_height(),
        theme=theme,
    )

    menu.add.label("MineSat Neo", font_name=FONT_NAME, font_size=96, font_color=ELECTRIC)
    menu.add.vertical_margin(10)
    menu.add.label("Nowocześniejszy interfejs • neon + szkło", font_size=28, font_color=WHITE)
    menu.add.vertical_margin(30)

    levels = list(C("DIFFICULTIES", {}).keys())
    if not levels:
        levels = ["Łatwy", "Średni", "Trudny", "Ekspert"]
    for lvl in levels:
        menu.add.button(lvl, lambda l=lvl: (start_game_fn(l), menu.disable()))

    menu.add.vertical_margin(20)
    custom_submenu = create_custom_game_menu(surface, start_game_fn, get_custom_setting_fn, update_custom_setting_fn)
    scoreboard_submenu = create_scoreboard_display_menu(surface)

    menu.add.button("Tryb niestandardowy", custom_submenu)
    menu.add.button("Tablica wyników", scoreboard_submenu)
    menu.add.button("Wyjście", pygame_menu.events.EXIT, background_color=RED)

    menu.mainloop = (lambda *args, **kwargs:
                     pygame_menu.Menu.mainloop(menu, surface, bgfun=lambda: _menu_bgfun(surface)))
    return menu

# ------------- Record name input -------------
def display_name_input_menu(game_surface, final_time):
    theme = _neo_theme()
    theme.title_font_color = GREEN
    input_menu = pygame_menu.Menu(
        "Nowy rekord!",
        game_surface.get_width(),
        game_surface.get_height(),
        theme=theme
    )

    action_result = ["skip", None]

    def set_player_action_and_disable(action, name=None):
        action_result[0] = action
        action_result[1] = name
        input_menu.disable()

    input_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    input_menu.add.vertical_margin(20)

    name_input = input_menu.add.text_input('Imię: ', maxchar=10, input_underline='_', font_size=30, default='Anon')
    input_menu.add.vertical_margin(30)
    input_menu.add.button("Zapisz wynik", lambda: set_player_action_and_disable("save", name_input.get_value()), background_color=GREEN)
    input_menu.add.button("Pomiń", lambda: set_player_action_and_disable("skip"))

    pygame_menu.Menu.mainloop(input_menu, game_surface, bgfun=lambda: _menu_bgfun(game_surface))
    return action_result[0], action_result[1]

# ------------- End game menu -------------
def display_end_game_menu(game_surface, is_won, current_level_name, final_time):
    theme = _neo_theme()
    theme.title_font_color = GREEN if is_won else RED
    end_menu = pygame_menu.Menu(
        "Wygrana!" if is_won else "Przegrana...",
        game_surface.get_width(),
        game_surface.get_height(),
        theme=theme
    )

    end_menu.add.label(f"Poziom: {current_level_name}", font_size=28)
    end_menu.add.label(f"Czas: {final_time:.2f} sek", font_size=30)
    end_menu.add.vertical_margin(30)

    action_result = ["menu"]

    def set_player_action(selected_action):
        action_result[0] = selected_action
        end_menu.disable()

    end_menu.add.button("Restart", lambda: set_player_action("restart"), background_color=LIGHT_NAVY)
    end_menu.add.button("Menu Główne", lambda: set_player_action("menu"))
    end_menu.add.button("Wyjście", lambda: set_player_action("exit"), background_color=RED)

    pygame_menu.Menu.mainloop(end_menu, game_surface, bgfun=lambda: _menu_bgfun(game_surface))
    return action_result[0]