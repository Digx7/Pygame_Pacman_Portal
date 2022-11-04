import sys
from time import sleep

import pygame
import pygame as pg
from game_math import *

movement = {pg.K_LEFT: (-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_RIGHT: (1, 0),
            pg.K_UP: (0, -1),
            pg.K_DOWN: (0, 1),
            pg.K_a: (-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_d: (1, 0),
            pg.K_w: (0, -1),
            pg.K_s: (0, 1)
            }


# update and draw managers ===============


def start_menu_update(g):
    pg.mouse.set_visible(True)
    check_events(g)


def start_menu_draw(g):
    g.screen.fill(g.settings.bg_color)
    g.StartUI.draw()


def main_update(g):
    pg.mouse.set_visible(False)
    check_events(g)
    g.player.update()
    g.ghosts.update()


def main_draw(g):
    g.screen.fill(g.settings.bg_color)
    g.map.draw()
    g.player.draw()
    g.ghosts.draw()


def end_update(g):
    pg.mouse.set_visible(True)
    check_events(g)


def end_draw(g):
    g.screen.fill(g.settings.bg_color)


# event listeners ===================


def check_events(g):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if g.data.is_current_scene("menu"): start_events(event, g)
        elif g.data.is_current_scene("main"): main_events(event, g)
        elif g.data.is_current_scene("end"): end_events(event, g)


def start_events(event, g):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if g.StartUI.current_mode == g.StartUI.modes["Main"]:
            if g.StartUI.buttons.check_button("play_button", mouse_x, mouse_y):
                on_play_click(g)
            elif g.StartUI.buttons.check_button("score_button", mouse_x, mouse_y):
                on_leaderboard_click(g)
                print("Score got clicked")
            elif g.StartUI.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                print("Back got clicked")
                on_leaderboard_back_click(g)
        elif g.StartUI.current_mode == g.StartUI.modes["LeaderBoard"]:
            if g.StartUI.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                print("Back got clicked")
                on_leaderboard_back_click(g)
    elif event.type == pygame.MOUSEMOTION:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if g.StartUI.current_mode == g.StartUI.modes["Main"]:
            if g.StartUI.buttons.check_button("play_button", mouse_x, mouse_y):
                pass
            elif g.StartUI.buttons.check_button("score_button", mouse_x, mouse_y):
                pass
            elif g.StartUI.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                pass
        elif g.StartUI.current_mode == g.StartUI.modes["LeaderBoard"]:
            if g.StartUI.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                pass




def main_events(event, g):
    if event.type == pygame.KEYDOWN:
        main_keydown_events(event, g)
    elif event.type == pygame.KEYUP:
        main_keyup_events(event, g)
    elif event.type == pg.USEREVENT:
        g.player.update_animation()
        g.ghosts.update_animations()


def main_keydown_events(event, g):
    key = event.key
    if key == pg.K_q:
        sys.exit()
    elif key in movement.keys(): g.player.update_velocity(movement[key])
    elif key == pg.K_f:
        g.ghosts.toggle_flee()
    elif key == pg.K_t:
        g.ghosts.debug()


def main_keyup_events(event, g):
    key = event.key
    if key in movement.keys(): g.player.update_velocity((0, 0))


def end_events(event, g):
    pass


# on button click ======================


def on_play_click(g):
    g.data.reset_stats()
    g.data.set_current_scene("main")
    reset(g)


def on_leaderboard_click(g):
    g.StartUI.current_mode = g.StartUI.modes["LeaderBoard"]


def on_leaderboard_back_click(g):
    g.StartUI.current_mode = g.StartUI.modes["Main"]
    print("Back")

# helper functions =================


# collision manager functions


def reset(g):
    """Resets after player dead"""
    pass
