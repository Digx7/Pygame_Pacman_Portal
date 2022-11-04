import pygame as pg
import pygame.time

from game_math import *
from pygame.sprite import Sprite


class Character(Sprite):

    def __init__(self, screen, settings, game_map, starting_node, color=(255, 0, 0)):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.setup_test_art()
        self.color = color

        self.game_map = game_map
        self.update_node(starting_node)
        self.move_to(starting_node)

        self.velocity = (0, 0)
        self.last_velocity = (1, 0)

        self.move_every = 100
        self.speed = 5
        self.current = 0

        self.move_by_velocity = True

    def set_speed(self, new_speed):
        self.speed = new_speed

    def setup_test_art(self):
        self.rect = pg.Rect(0, 0, 25, 25)

    def update_node(self, new_node):
        self.current_node = new_node

    def update_velocity(self, new_velocity):
        self.velocity = new_velocity

    def update_last_velocity(self):
        if self.velocity != (0, 0) and self.last_velocity != self.velocity:
            self.last_velocity = self.velocity

    def move_to(self, destination):
        # print(self.game_map.has_node(destination))
        if self.game_map.has_node(destination):
            self.update_node(destination)
            map_node = self.game_map.graph.nodes[destination]['info']
            self.rect.center = map_node.rect.center

            # print(f'Moving character to {map_node.pos} from MapNode')
            # map_node.show()

    def move_by(self, delta):
        destination = (self.current_node[0] + delta[0], self.current_node[1] + delta[1],)
        # print(f'Trying to move to {destination}')
        self.move_to(destination)

    def update(self):
        if self.current >= self.move_every:
            if self.move_by_velocity:
                self.move_by(self.velocity)
            self.current = 0
        else: self.current += self.speed
        self.update_last_velocity()

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)
