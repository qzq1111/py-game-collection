import pygame
import pygame.font

from greedy_snake.button import Button
from greedy_snake.conf import GAME_STATUS_INIT, GAME_STATUS_RUN, GAME_STATUS_OVER, GAME_FPS, GAME_SCORE_COLOR
from greedy_snake.food import Food
from greedy_snake.layout import Layout
from greedy_snake.snake import Snake


class Game(object):
    status = GAME_STATUS_INIT
    done = False

    def __init__(self, width, height, cell_size):

        self.width, self.height, self.cell_size = width, height, cell_size
        self.__init()

    def __init(self):
        pygame.init()
        pygame.display.set_caption("贪吃蛇")
        self.font = pygame.font.SysFont('SimHei', 20)

        self.fps_clock = pygame.time.Clock()
        self.fps = GAME_FPS
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
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]:
                    self.snake.update_move_direction(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标按下
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_play_mouse(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION:
                # 鼠标移动
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_move_mouse(mouse_x, mouse_y)

        return

    def handle_play_mouse(self, mouse_x, mouse_y):

        if self.status == GAME_STATUS_RUN:
            # 游戏运行中，不用检测鼠标
            return

        # 检测鼠标是否点击开始游戏
        if self.button.rect.collidepoint(mouse_x, mouse_y):
            self.status = GAME_STATUS_RUN
            self.button.is_hidden = True

        return

    def handle_move_mouse(self, mouse_x, mouse_y):
        if self.status:
            return
        self.button.is_active = self.button.rect.collidepoint(mouse_x, mouse_y)

    def game_over(self):
        self.status = GAME_STATUS_OVER  # 重置游戏状态
        self.button.set_msg("重新开始游戏")
        self.button.is_hidden = False  # 显示开始按钮
        self.food.reset()  # 重置食物位置
        self.snake.rest()  # 重置🐍状态

    def draw_score(self, score):
        value = self.font.render("分数: " + str(score), True, GAME_SCORE_COLOR)
        self.screen.blit(value, [0, 0])

    def run(self):

        while not self.done:
            self.handle_events()
            self.layout.draw()
            self.button.draw()

            if self.status == GAME_STATUS_RUN:
                # 绘制🐍位置
                self.snake.move(self.food)
                # 绘制食物位置
                self.food.draw()
                # 绘制分数
                self.draw_score(self.snake.length)
                # 检测🐍是否还存活
                if self.snake.check_is_wall() or self.snake.check_eat_self():
                    self.game_over()

            pygame.display.update()
            self.fps_clock.tick(self.fps)
        pygame.quit()
        return


if __name__ == '__main__':
    game = Game(800, 600, 20)
    game.run()
