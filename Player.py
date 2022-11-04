import pygame as pg
import pygame.time

from game_math import *
from pygame.sprite import Sprite
from Character import *
from art import *


class Player(Character):

    def __init__(self, g, starting_node):
        super().__init__(g.screen, g.settings, g.map, starting_node, (255, 255, 0))

        self.setup_animations()

    def update(self):
        super().update()

    def setup_animations(self):
        self.Idle_Anim = Animation([self.settings.sprites["player_move1"],
                                    self.settings.sprites["player_move2"]])
        self.Death_Anim = Animation([self.settings.sprites["player_dead1"],
                                     self.settings.sprites["player_dead2"],
                                     self.settings.sprites["player_dead3"],
                                     self.settings.sprites["player_dead4"]], 1)

        self.Animations = Animations(idle=self.Idle_Anim, death=self.Death_Anim)

        self.update_animation()
        self.rect = self.image.get_rect()

    def update_animation(self):
        self.image = self.Animations.get_current_animation().update()
        self.image, self.rect = self.rotate_image(self.image)

    def rotate_image(self, img):

        angle = 0

        if self.last_velocity[0] == 1: angle = 0
        elif self.last_velocity[0] == -1: angle = 180
        elif self.last_velocity[1] == -1: angle = 90
        elif self.last_velocity[1] == 1: angle = 270

        return self.rot_center(img, angle, self.rect.centerx, self.rect.centery)

    def rot_center(self, img, angle, x, y):
        rotated_img = pygame.transform.rotate(img, angle)
        new_rect = rotated_img.get_rect(center=img.get_rect(center=(x, y)).center)

        return rotated_img, new_rect

    def draw(self):
        self.screen.blit(self.image, self.rect)
