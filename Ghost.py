import gc

import networkx as nx
import pygame as pg
import pygame.time

from game_math import *
from pygame.sprite import Sprite
from Character import *
from art import *


class Ghosts:

    def __init__(self, g, starting_nodes, player):
        self.ghost_list = []
        self.ghost_names = ["inky", "pinky", "blinky", "clyde"]
        for i in range(len(starting_nodes)):
            if i <= len(self.ghost_names): name = self.ghost_names[i]
            else: name = self.ghost_names[len(self.ghost_names)]
            self.ghost_list.append(Ghost(g, starting_nodes[i], player, name))

        for ghost in self.ghost_list:
            print(ghost.name)

        # self.ghost_animations = {"inky_idle": Animation([g.settings.sprites["inky_move1"],
        #                                                   g.settings.sprites["inky_move2"]]),
        #                          "pinky_idle": Animation([g.settings.sprites["pinky_move1"],
        #                                                   g.settings.sprites["pinky_move2"]]),
        #                          "blinky_idle": Animation([g.settings.sprites["blinky_move1"],
        #                                                   g.settings.sprites["blinky_move2"]]),
        #                          "clyde_idle": Animation([g.settings.sprites["clyde_move1"],
        #                                                   g.settings.sprites["clyde_move2"]])
        #                          }
        #
        # self.ghost_list[0].setup_animations(self.ghost_animations["inky_idle"])
        # self.ghost_list[1].setup_animations(self.ghost_animations["inky_idle"])
        # self.ghost_list[2].setup_animations(self.ghost_animations["inky_idle"])
        # self.ghost_list[3].setup_animations(self.ghost_animations["inky_idle"])

        for ghost in self.ghost_list:
            print(ghost.name)

    def toggle_flee(self):
        for ghost in self.ghost_list:
            ghost.set_flee(not ghost.flee)

    def update(self):
        for ghost in self.ghost_list:
            ghost.update()

    def update_animations(self):
        for ghost in self.ghost_list:
            ghost.update_animation()

    def draw(self):
        for ghost in self.ghost_list:
            ghost.draw()

    def debug(self):
        for ghost in self.ghost_list:
            print(f'{ghost.name} | Pos = {ghost.current_node} | Vel = {ghost.velocity} | Animation = '
                  f'{ghost.Animations.current_animation} | Animation.current_key = {ghost.Animations.current_key}')


class Ghost(Character):

    def __init__(self, g, starting_node, player, name):
        super().__init__(g.screen, g.settings, g.map, starting_node, (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.reset_node = starting_node
        self.target_node = (0, 0)
        self.player = player
        self.name = name
        self.flee = False
        self.set_speed(2)

        self.setup_animations()

    def setup_animations(self):
        if self.name == "inky":
            self.Idle_Anim = Animation([self.settings.sprites["inky_move1"],
                                        self.settings.sprites["inky_move2"]])
        elif self.name == "pinky":
            self.Idle_Anim = Animation([self.settings.sprites["p"],
                                        self.settings.sprites["pinky_move2"]])
        elif self.name == "blinky":
            self.Idle_Anim = Animation([self.settings.sprites["blinky_move1"],
                                        self.settings.sprites["blinky_move2"]])
        elif self.name == "clyde":
            self.Idle_Anim = Animation([self.settings.sprites["clyde_move1"],
                                        self.settings.sprites["clyde_move2"]])

        self.Animations = Animations(idle=self.Idle_Anim)

        self.update_animation()
        self.rect = self.image.get_rect()

    def update_animation(self):
        self.image = self.Animations.get_current_animation().update()

    def set_flee(self, new_state):
        self.flee = new_state

    def set_target_node(self, new_node):
        self.target_node = new_node

    def generate_path(self, end_node):
        # print(f'Ghost path: Start = {self.current_node} End = {end_node}')
        self.path = nx.shortest_path(self.game_map.graph, self.current_node, end_node)
        # print("ghost path: ", self.path)

    def update(self):
        if not self.flee:
            self.generate_path(self.player.current_node)
        else:
            self.generate_path(self.reset_node)
        if len(self.path) > 2:
            next_step = self.path[1]
            next = (next_step[0] - self.current_node[0], next_step[1] - self.current_node[1])
            self.update_velocity(next)
            super().update()
        else:
            self.update_node(self.reset_node)
            self.move_to(self.current_node)

    def draw(self):
        self.screen.blit(self.image, self.rect)
