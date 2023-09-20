import random

import pygame
import time
import pygame.font

"""
色卡：
250,240,228 背景色

155,205,210

255,133,81

255, 222, 222
"""

BACKGROUND_COLOR = (250, 240, 228)  # 背景色
LINE_COLOR = (255, 222, 222)  # 线条颜色
BUTTON_COLOR = (155, 205, 210)  # 按钮颜色
BUTTON_ACTIVE_COLOR = (255, 133, 81)  # 按钮激活颜色
TEXT_COLOR = (255, 255, 255)  # 文字颜色
SNAKE_COLOR = (155, 205, 210)  # 蛇🐍颜色
SNAKE_MOVE_UP = "UP"  # 🐍向上移动
SNAKE_MOVE_DOWN = "DOWN"  # 🐍向下移动
SNAKE_MOVE_LEFT = "LEFT"  # 🐍向左移动
SNAKE_MOVE_RIGHT = "RIGHT"  # 🐍向右移动


# 贪吃蛇🐍

class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake(object):
    MOVE_DIRECTION = {
        SNAKE_MOVE_UP: Location(0, -1),
        SNAKE_MOVE_DOWN: Location(0, 1),
        SNAKE_MOVE_LEFT: Location(-1, 0),
        SNAKE_MOVE_RIGHT: Location(1, 0),
    }

    def __init__(self, screen, cell_size):
        self.screen = screen  # 图
        self.cell_size = cell_size  # 格子大小
        self.location = []  # 🐍的位置信息
        self.head = Location(*screen.get_rect().center)  # 🐍头位置
        self.location.append(self.head)
        self.length = 1  # 🐍长度
        self.move_direction = SNAKE_MOVE_UP  # 🐍移动方向

    def eat(self):
        self.length += 1

    def update_move_direction(self, key):
        """
        判断移动方向
        :param key:
        :return:
        """
        if key == pygame.K_RIGHT:
            if self.move_direction != SNAKE_MOVE_LEFT:
                self.move_direction = SNAKE_MOVE_RIGHT
        elif key == pygame.K_LEFT:
            if self.move_direction != SNAKE_MOVE_RIGHT:
                self.move_direction = SNAKE_MOVE_LEFT
        elif key == pygame.K_UP:
            if self.move_direction != SNAKE_MOVE_DOWN:
                self.move_direction = SNAKE_MOVE_UP
        elif key == pygame.K_DOWN:
            if self.move_direction != SNAKE_MOVE_UP:
                self.move_direction = SNAKE_MOVE_DOWN
        return

    def draw(self):
        for item in self.location:
            grid_surface = pygame.Surface((self.cell_size, self.cell_size))
            grid_surface.fill(SNAKE_COLOR)
            self.screen.blit(grid_surface, (item.x, item.y))

    def move(self, food):

        move_direction = self.MOVE_DIRECTION[self.move_direction]
        if not move_direction:
            return

        x_change = move_direction.x
        y_change = move_direction.y

        # 🐍头坐标变化位置
        self.head.x += x_change * self.cell_size
        self.head.y += y_change * self.cell_size

        if self.head.x > self.screen.get_width():
            self.head.x = 0

        if self.head.x < 0:
            self.head.x = self.screen.get_width()

        if self.head.y > self.screen.get_height():
            self.head.y = 0

        if self.head.y < 0:
            self.head.y = self.screen.get_height()

        self.location.append(Location(self.head.x, self.head.y))

        # 如果位置内容大于当前🐍的长度，就移除第一个位置数据
        if len(self.location) > self.length > 0:
            self.location.pop(0)

        # 如果两个坐标相等了，就重置实物的地址
        if food.location.x == self.head.x and food.location.y == self.head.y:
            self.eat()
            food.reset()

        self.draw()


class Food(object):

    def __init__(self, screen, cell_size):
        self.screen = screen
        self.location = None
        self.cell_size = cell_size
        self.reset()

    def draw(self):
        grid_surface = pygame.Surface((self.cell_size, self.cell_size))
        grid_surface.fill((0, 233, 211))
        self.screen.blit(grid_surface, (self.location.x, self.location.y))

    def reset(self):
        # 重置当前实物位置
        x = round(random.randrange(0, self.screen.get_width() / self.cell_size)) * self.cell_size
        y = round(random.randrange(0, self.screen.get_height() / self.cell_size)) * self.cell_size
        self.location = Location(x, y)


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

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(surface, LINE_COLOR, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(surface, LINE_COLOR, (0, y), (self.width, y))

        self.screen.blit(surface, (0, 0))
        return


class GameLoop(object):
    status = False
    done = False

    def __init__(self, width, height, cell_size):
        self.width, self.height, self.cell_size = width, height, cell_size
        self.__init()

    def __init(self):
        pygame.init()
        pygame.display.set_caption("贪吃蛇")

        self.fps_clock = pygame.time.Clock()
        self.fps = 10
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.layout = Layout(screen=self.screen, width=self.width, height=self.height, cell_size=self.cell_size)
        self.button = Button(self.screen, "开始游戏")
        self.snake = Snake(self.screen, self.cell_size)
        self.food = Food(self.screen, self.cell_size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
                    self.snake.update_move_direction(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标按下，
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_play_mouse(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION:
                # 鼠标移动
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_move_mouse(mouse_x, mouse_y)

        return

    def handle_play_mouse(self, mouse_x, mouse_y):
        if self.status:
            return
        if self.button.rect.collidepoint(mouse_x, mouse_y):
            self.status = True
            self.button.is_hidden = True

    def handle_move_mouse(self, mouse_x, mouse_y):
        if self.status:
            return
        self.button.is_active = self.button.rect.collidepoint(mouse_x, mouse_y)

    def run(self):

        while not self.done:
            self.handle_events()
            self.layout.draw()
            self.button.draw()

            if self.status:
                # 绘制🐍位置
                self.snake.move(self.food)
                # 绘制食物位置
                self.food.draw()

            pygame.display.update()
            self.fps_clock.tick(self.fps)
        pygame.quit()
        return


if __name__ == '__main__':
    game = GameLoop(800, 600, 20)
    game.run()
