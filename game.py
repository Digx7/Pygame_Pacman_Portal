import pygame as pg
import pygame.time

from game_settings import Settings
import game_functions as gf
from pygame.sprite import Group
from sound import *
from runtime_data import *
from ui import *
from game_math import *
from Character import *
from Player import *
from Ghost import *


class Game:
    def __init__(self):
        # initialize pygame and set up screen
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Pacman Portal")

        # set up frame rate
        self.clock = pg.time.Clock()
        self.clock.tick(self.settings.fps)
        pygame.time.set_timer(pygame.USEREVENT, 250)

        # set up data
        self.data = RuntimeData(self.settings)

        # set up sound
        self.sound = Sound('Sounds/Pacman Remix.mp3')

        # set up UI
        self.StartUI = StartUI(self.settings, self.screen, self.data)
        self.GameUI = GameUI(self.settings, self.screen, self.data)
        self.EndUI = EndUI(self.settings, self.screen, self.data)

        # set up map
        self.map = Map(self.screen, self.settings)

        # set up player and ghost character
        self.player = Player(self, (10, 13))
        self.ghosts = Ghosts(self, ((0, 0), (21, 0), (11, 11), (12, 11)), self.player)

    def play(self):
        # self.sound.play_bg()
        while True:
            if self.data.is_current_scene("menu"):
                gf.start_menu_update(self)
                gf.start_menu_draw(self)
            elif self.data.is_current_scene("main"):
                gf.main_update(self)
                gf.main_draw(self)
            elif self.data.is_current_scene("end"):
                gf.end_update(self)
                gf.end_draw(self)
            # self.clock.tick(self.settings.fps)
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
