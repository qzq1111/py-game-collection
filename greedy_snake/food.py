import random

import pygame

from greedy_snake.conf import BACKGROUND_COLOR, FOOD_COLOR
from greedy_snake.location import Location


class Food(object):

    def __init__(self, screen, cell_size):
        self.screen = screen
        self.location = None
        self.cell_size = cell_size
        self.reset()

    def draw(self):
        surface = pygame.Surface((self.cell_size, self.cell_size))
        surface.fill(BACKGROUND_COLOR)
        pygame.draw.circle(surface, FOOD_COLOR, (10, 10), 10)
        self.screen.blit(surface, (self.location.x, self.location.y))

    def reset(self):
        # 重置当前实物位置
        x = round(random.randrange(0, self.screen.get_width() / self.cell_size)) * self.cell_size
        y = round(random.randrange(0, self.screen.get_height() / self.cell_size)) * self.cell_size
        self.location = Location(x, y)
