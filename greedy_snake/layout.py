import pygame

from greedy_snake.conf import BACKGROUND_COLOR


class Layout(object):

    def __init__(self, screen, width, height, cell_size):
        self.screen = screen
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(BACKGROUND_COLOR)

    def draw(self):
        """
        绘制运行界面
        :return:
        """

        self.screen.blit(self.surface, (0, 0))
        return
