import random

import pygame


# 贪吃蛇🐍

class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake(object):

    def __init__(self, screen, cell_size):
        self.screen = screen  # 图
        self.cell_size = cell_size  # 格子大小
        self.location = []  # 🐍的位置信息
        self.head = Location(0, 0)  # 🐍头位置
        self.length = 1  # 🐍长度

    # 画图
    def draw(self):
        for item in self.location:
            grid_surface = pygame.Surface((self.cell_size, self.cell_size))
            grid_surface.fill((0, 0, 0))
            self.screen.blit(grid_surface, (item.x, item.y))

    def eat(self):
        self.length += 1

    def run(self, x_change, y_change, food):

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


class Food(object):

    def __init__(self, screen, cell_size):
        self.screen = screen
        self.location = None
        self.cell_size = cell_size

    def draw(self):
        grid_surface = pygame.Surface((self.cell_size, self.cell_size))
        grid_surface.fill((0, 233, 211))
        self.screen.blit(grid_surface, (self.location.x, self.location.y))

    def reset(self):
        # 重置当前实物位置
        x = round(random.randrange(0, self.screen.get_width() / self.cell_size)) * self.cell_size
        y = round(random.randrange(0, self.screen.get_height() / self.cell_size)) * self.cell_size
        self.location = Location(x, y)


class Grid(object):

    def __init__(self, screen, width, height, cell_size):
        self.screen = screen
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def draw(self):
        grid_surface = pygame.Surface((self.width, self.height))
        grid_surface.fill((255, 255, 255))

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(grid_surface, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(grid_surface, (0, 0, 0), (0, y), (self.width, y))

        self.screen.blit(grid_surface, (0, 0))


def main():
    pygame.init()

    width, height = 800, 600

    screen = pygame.display.set_mode((width, height))
    fps = 10
    fps_clock = pygame.time.Clock()

    grid = Grid(screen=screen, width=width, height=height, cell_size=20)

    snake = Snake(screen=screen, cell_size=20)

    food = Food(screen=screen, cell_size=20)
    food.reset()

    x_change = 0
    y_change = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_change = 1
                    y_change = 0
                elif event.key == pygame.K_LEFT:
                    x_change = -1
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -1
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = 1
        # 绘制网格
        grid.draw()

        # 绘制🐍位置
        snake.run(x_change, y_change, food)
        snake.draw()
        # 绘制食物位置
        food.draw()

        pygame.display.update()
        fps_clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
