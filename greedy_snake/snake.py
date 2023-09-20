import pygame

from greedy_snake.conf import SNAKE_MOVE_UP, SNAKE_MOVE_LEFT, SNAKE_MOVE_RIGHT, SNAKE_MOVE_DOWN, SNAKE_COLOR, \
    SNAKE_BODY_COLOR
from greedy_snake.location import Location


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
        if key == pygame.K_RIGHT or key == pygame.K_d:
            if self.move_direction != SNAKE_MOVE_LEFT:
                self.move_direction = SNAKE_MOVE_RIGHT
        elif key == pygame.K_LEFT or key == pygame.K_a:
            if self.move_direction != SNAKE_MOVE_RIGHT:
                self.move_direction = SNAKE_MOVE_LEFT
        elif key == pygame.K_UP or key == pygame.K_w:
            if self.move_direction != SNAKE_MOVE_DOWN:
                self.move_direction = SNAKE_MOVE_UP
        elif key == pygame.K_DOWN or key == pygame.K_s:
            if self.move_direction != SNAKE_MOVE_UP:
                self.move_direction = SNAKE_MOVE_DOWN
        return

    def draw(self):
        for item in self.location:
            surface = pygame.Surface((self.cell_size, self.cell_size))
            surface.fill(SNAKE_BODY_COLOR)
            self.screen.blit(surface, (item.x, item.y))
        else:
            surface = pygame.Surface((self.cell_size, self.cell_size))
            surface.fill(SNAKE_COLOR)
            self.screen.blit(surface, (self.head.x, self.head.y))

    def check_is_wall(self):
        """
        检测是否撞墙
        :return:
        """
        if self.head.x > self.screen.get_width():
            return True

        if self.head.x < 0:
            return True

        if self.head.y > self.screen.get_height():
            return True

        if self.head.y < 0:
            return True

        return False

    def check_eat_self(self):
        """
        检测是吃到自己了
        :return:
        """
        for item in self.location[:-1]:
            if item.x == self.head.x and item.y == self.head.y:
                return True
        return False

    def move(self, food):

        move_direction = self.MOVE_DIRECTION[self.move_direction]
        if not move_direction:
            return

        x_change = move_direction.x
        y_change = move_direction.y

        # 🐍头坐标变化位置
        self.head.x += x_change * self.cell_size
        self.head.y += y_change * self.cell_size
        self.location.append(Location(self.head.x, self.head.y))

        # 如果位置内容大于当前🐍的长度，就移除第一个位置数据
        if len(self.location) > self.length > 0:
            self.location.pop(0)

        # 如果两个坐标相等了，就重置实物的地址
        if food.location.x == self.head.x and food.location.y == self.head.y:
            self.eat()
            food.reset()

        self.draw()

    def rest(self):
        self.location = []  # 🐍的位置信息
        self.head = Location(*self.screen.get_rect().center)  # 🐍头位置
        self.location.append(self.head)
        self.length = 1  # 🐍长度
        self.move_direction = SNAKE_MOVE_UP  # 🐍移动方向
