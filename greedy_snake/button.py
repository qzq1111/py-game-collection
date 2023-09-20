import pygame

from greedy_snake.conf import TEXT_COLOR, BUTTON_COLOR, BUTTON_ACTIVE_COLOR


class Button(object):
    def __init__(self, screen, msg):
        self.screen = screen
        self.font = pygame.font.SysFont('SimHei', 20)
        self.msg = msg
        self.is_active = False  # 是否选中
        self.is_hidden = False  # 是否隐藏
        self._init()

    def _init(self):
        # 绘制一个矩形
        self.rect = pygame.Rect(0, 0, 200, 50)
        # 绘制文字
        self.img = self.font.render(self.msg, True, TEXT_COLOR, BUTTON_COLOR)
        self.msg_image_rect = self.img.get_rect()

        self.img_active = self.font.render(self.msg, True, TEXT_COLOR, BUTTON_ACTIVE_COLOR)

        # 设置矩形的位置
        self.rect.center = self.screen.get_rect().center
        # 设置文字的位置
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        if self.is_hidden:
            return
        if self.is_active:
            self.screen.fill(BUTTON_ACTIVE_COLOR, self.rect)
            self.screen.blit(self.img_active, self.msg_image_rect)
        else:
            self.screen.fill(BUTTON_COLOR, self.rect)
            self.screen.blit(self.img, self.msg_image_rect)
