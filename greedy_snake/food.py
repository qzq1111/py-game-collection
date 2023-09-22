import random

import pygame

from greedy_snake.conf import BACKGROUND_COLOR, FOOD_COLOR


class Food(object):

    def __init__(self, screen, cell_size):
        self.cell_size = cell_size
        self.screen = screen

        self.surface = pygame.Surface((self.cell_size, self.cell_size))
        self.surface.fill(BACKGROUND_COLOR)
        pygame.draw.circle(self.surface, FOOD_COLOR, (10, 10), 10)

        self.x = 0
        self.y = 0

        self.reset()

    def draw(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def reset(self):
        # 重置当前实物位置
        self.x = round(random.randrange(10, (self.screen.get_width() // self.cell_size)) - 10) * self.cell_size
        self.y = round(random.randrange(10, (self.screen.get_height() // self.cell_size)) - 10) * self.cell_size
