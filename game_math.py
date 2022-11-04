from io import UnsupportedOperation
from math import sqrt
import networkx as nx
import pygame
from pygame import *
from random import *


class Vector:
    '''General purpose, 2d vector class for use in moving objects in games
       it turns out linear algebra IS useful after all !

       uses Python's version of operator overloading  v.__add__(u) can be written as v + u
    '''
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
    def __repr__(self):                 
        return f'Vector({self.x},{self.y})'
    def __add__(self, other):                     # v + u
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):                     # v - u
        return self + -other
    def __neg__(self):                            # -v
        return Vector(-self.x, -self.y)
    def __mul__(self, k):                         # v * k
        return Vector(k * self.x, k * self.y)
    def __rmul__(self, k):                        # k * v
        return self.__mul__(k)
    def __floordiv__(self, k):                    # v // k
        return Vector(self.x // k, self.y // k)
    def __truediv__(self, k):                     # v / k
        return Vector(self.x / k, self.y / k)

    def dot(self, other):            # dot product, length of self when projected on other
        return self.x * other.x + self.y + other.y
    def cross(self, other): raise UnsupportedOperation    # not supported at this time: requires 3d Vectors !
    def norm(self):                  # length of a vector
        return sqrt(self.dot(self))
    def magnitude(self):             # another name for the norm
        return self.norm()
    def unit_vector(self):            # v of unit length in same direction as v
        return self / self.magnitude()

    def __iadd__(self, other):         # v += u
        self.x += other.x
        self.y += other.y
        return self
    def __isub__(self, other):         # v -= u
        self += -other
        return self
    def __imul__(self, k):             # v *= k
        self.x *= k
        self.y += k
        return self


class Map:

    def __init__(self, screen, settings):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.setup_graph()
        self.map_img = pygame.image.load('images/pacmanMap.jpg')
        self.map_img = pygame.transform.scale(self.map_img, (settings.screen_width, settings.screen_height))
        self.map_img_rect = self.map_img.get_rect()

        self.map_img_rect.center = self.screen_rect.center

    def setup_graph(self):

        m = 22
        n = 24

        self.graph = nx.grid_2d_graph(m, n)

        attr = {}

        for x in range(m):
            for y in range(n):
                attr[(x, y)] = {'info': MapNode((x, y))}

        nx.set_node_attributes(self.graph, attr)
        nodes_to_remove = []
        nodes_to_remove.extend(self.remove_square((1, 1), (4, 3)))
        nodes_to_remove.extend(self.remove_square((5, 1), (9, 3)))
        nodes_to_remove.extend(self.remove_square((10, 0), (12, 3)))
        nodes_to_remove.extend(self.remove_square((1, 4), (4, 6)))
        nodes_to_remove.extend(self.remove_square((5, 4), (7, 11)))
        nodes_to_remove.extend(self.remove_square((0, 7), (4, 11)))
        nodes_to_remove.extend(self.remove_square((0, 12), (4, 15)))
        nodes_to_remove.extend(self.remove_square((5, 12), (7, 15)))
        nodes_to_remove.extend(self.remove_square((1, 16), (4, 18)))
        nodes_to_remove.extend(self.remove_square((3, 18), (4, 20)))
        nodes_to_remove.extend(self.remove_square((0, 19), (2, 20)))
        nodes_to_remove.extend(self.remove_square((1, 21), (9, 23)))
        nodes_to_remove.extend(self.remove_square((5, 19), (7, 22)))

        nodes_to_remove.extend(self.remove_square((5, 16), (9, 18)))
        nodes_to_remove.extend(self.remove_square((8, 19), (14, 20)))
        nodes_to_remove.extend(self.remove_square((10, 20), (12, 23)))
        nodes_to_remove.extend(self.remove_square((8, 14), (14, 15)))
        nodes_to_remove.extend(self.remove_square((10, 15), (12, 18)))
        nodes_to_remove.extend(self.remove_square((8, 9), (9, 13)))
        nodes_to_remove.extend(self.remove_square((13, 9), (14, 13)))
        nodes_to_remove.extend(self.remove_square((8, 12), (14, 13)))
        nodes_to_remove.extend(self.remove_square((8, 4), (14, 5)))
        nodes_to_remove.extend(self.remove_square((10, 5), (12, 8)))

        nodes_to_remove.append((9, 9))
        nodes_to_remove.append((12, 9))
        nodes_to_remove.append((8, 5))
        nodes_to_remove.append((9, 5))
        nodes_to_remove.append((8, 7))
        nodes_to_remove.append((7, 7))

        mirror = []

        for i in nodes_to_remove:
            l = list(i)
            l[0] = 21 - l[0]
            t = tuple(l)
            mirror.append(t)

        nodes_to_remove.extend(mirror)

        self.graph.remove_nodes_from(nodes_to_remove)

    def remove_square(self, top_left, bot_right):
        output = []
        for x in range(top_left[0],bot_right[0]):
            for y in range(top_left[1],bot_right[1]):
                output.append((x,y))
        return output

    def find_path(self, start_node, end_node):
        return nx.shortest_path(self.graph, start_node, end_node)

    def has_node(self, node):
        return self.graph.has_node(node)

    def draw(self):
        self.screen.blit(self.map_img, self.map_img_rect)

        for v, info in self.graph.nodes(data=True):
            info['info'].draw(self.screen)

        for e in self.graph.edges:
            start_pos = self.graph.nodes[e[0]]['info'].rect.center
            end_pos = self.graph.nodes[e[1]]['info'].rect.center

            pygame.draw.line(self.screen, (255, 255, 255), start_pos, end_pos)



class MapNode:

    def __init__(self, pos, item='empty'):
        self.pos = pos
        self.item = item

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.centerx = (self.pos[0] * 40) + 40
        self.rect.centery = (self.pos[1] * 40) + 40
        self.rect.width = 1
        self.rect.height = 1

    def show(self):
        print(f'Pos : {self.pos} , Item : {self.item}')

    def get_item(self):
        item = self.item
        self.item = 'empty'
        return item

    def draw(self, screen):
        pygame.draw.rect(screen, [255, 255, 255], self.rect)
