import pygame

from greedy_snake.conf import BACKGROUND_COLOR


class Layout(object):

    def __init__(self, screen, width, height, cell_size, ):
        self.screen = screen
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def draw(self):
        """
        绘制运行界面
        :return:
        """
        surface = pygame.Surface((self.width, self.height))
        surface.fill(BACKGROUND_COLOR)
        self.screen.blit(surface, (0, 0))
        return
