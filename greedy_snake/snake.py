import pygame
from greedy_snake.conf import SNAKE_MOVE_UP, SNAKE_MOVE_LEFT, SNAKE_MOVE_RIGHT, SNAKE_MOVE_DOWN, SNAKE_COLOR, \
    SNAKE_BODY_COLOR


class SnakeEntity(object):

    def __init__(self, x, y, cell_size, color):
        self.x, self.y, self.cell_size = x, y, cell_size
        self.surface = pygame.Surface((self.cell_size, self.cell_size))
        self.surface.fill(color)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class Snake(object):
    MOVE_DIRECTION = {
        SNAKE_MOVE_UP: (0, -1),
        SNAKE_MOVE_DOWN: (0, 1),
        SNAKE_MOVE_LEFT: (-1, 0),
        SNAKE_MOVE_RIGHT: (1, 0),
    }

    def __init__(self, screen, cell_size, ):
        self.screen = screen  # 图
        self.cell_size = cell_size  # 格子大小

        x, y = screen.get_rect().center

        self.head = SnakeEntity(x, y, cell_size, SNAKE_COLOR)  # 🐍头

        self.route = []  # 🐍的路线信息

        self.length = 1  # 🐍长度
        self.move_direction = SNAKE_MOVE_UP  # 🐍移动方向

        self.speed = 20  # 5次移动一格
        self.__times = 0  # 计次

    def eat(self):
        self.length += 1
        self.change_speed()

    def change_speed(self):

        if self.length > 0:
            self.speed = 20
        elif self.length > 5:
            self.speed = 15
        elif self.length > 10:
            self.speed = 10
        elif self.length > 15:
            self.speed = 8
        else:
            self.speed = 5

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
        for item in self.route[:-1]:
            if item.x == self.head.x and item.y == self.head.y:
                return True
        return False

    def check_eat_food(self, food_x, food_y):
        """
        是否吃到了食物
        :param food_x: 食物x坐标
        :param food_y: 食物y坐标
        :return:
        """
        # 如果两个坐标相等了，就重置实物的地址
        if food_x == self.head.x and food_y == self.head.y:
            return True
        return False

    def can_move(self):
        """
        检查是否可以移动
        :return:
        """
        self.__times += 1
        if self.__times >= self.speed:
            self.__times = 0
            return True

        return False

    def move(self):
        """
        更新蛇状态
        :return:
        """

        move_direction = self.MOVE_DIRECTION[self.move_direction]
        if not move_direction:
            return

        x_change, y_change = move_direction

        # 🐍头坐标变化位置
        self.head.x += x_change * self.cell_size
        self.head.y += y_change * self.cell_size

        # 记录🐍头位置
        self.route.append(SnakeEntity(x=self.head.x, y=self.head.y, cell_size=self.cell_size, color=SNAKE_BODY_COLOR))

        # 如果位置内容大于当前🐍的长度，就移除第一个位置数据
        if len(self.route) > self.length:
            self.route.pop(0)

        return

    def draw(self):
        """
        绘画蛇路径
        :return:
        """
        for item in self.route:
            item.draw(self.screen)

    def rest(self):
        """
        重置蛇状态
        :return:
        """
        self.route = []  # 🐍的位置信息
        x, y = self.screen.get_rect().center
        self.head = SnakeEntity(x, y, self.cell_size, SNAKE_COLOR)  # 🐍头
        self.length = 1  # 🐍长度
        self.move_direction = SNAKE_MOVE_UP  # 🐍移动方向
