import pygame


class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bullet(object):

    def __init__(self, x, y, screen: pygame.Surface):
        self.x = x + 20
        self.y = y - 10
        self.screen = screen
        self.bullet_image = None

        self.init()

    def init(self, path=None):
        """
        初始化子弹贴图，
        :param path: 飞机贴图位置
        :return:
        """
        if not path:
            bullet_image = pygame.image.load("./image/bullet.png").convert_alpha()
        else:
            bullet_image = pygame.image.load(path).convert_alpha()

        self.bullet_image = pygame.transform.scale(bullet_image, (10, 10))

    def update(self):
        self.y -= 10

    def is_over(self):
        return self.y <= 0

    def draw(self):
        self.screen.blit(self.bullet_image, (self.x, self.y))


class Aircraft(object):

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # 飞机位置
        self.x = None
        self.y = None

        self.aircraft_image = None  # 飞机贴图
        self.bullet_list = []  # 飞机子弹

        self.init()

    def init(self):
        self.init_aircraft()
        self.init_location()

    def init_location(self):
        """
        初始化飞机位置，屏幕最下方中间
        :return:
        """
        scree_center_x, scree_center_y = self.screen.get_rect().center

        self.x = scree_center_x - (self.aircraft_image.get_width() / 2)
        self.y = self.screen.get_height() - self.aircraft_image.get_height()

    def init_aircraft(self, path=None):
        """
        初始化飞机贴图，
        :param path: 飞机贴图位置
        :return:
        """
        if not path:
            aircraft_image = pygame.image.load("./image/aircraft.png").convert_alpha()
        else:
            aircraft_image = pygame.image.load(path).convert_alpha()

        self.aircraft_image = pygame.transform.scale(aircraft_image, (50, 50))

    def update(self, key):
        """
        判断移动方向
        :param key:
        :return:
        """

        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.x += 10
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.x -= 10
        elif key == pygame.K_UP or key == pygame.K_w:
            self.y -= 10
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.y += 10

        if self.x > self.screen.get_width() - self.aircraft_image.get_width():
            self.x = self.screen.get_width() - self.aircraft_image.get_width()

        if self.x < 0:
            self.x = 0

        if self.y > self.screen.get_height() - self.aircraft_image.get_height():
            self.y = self.screen.get_height() - self.aircraft_image.get_height()

        if self.y < 0:
            self.y = 0

        return

    def draw(self):
        self.screen.blit(self.aircraft_image, (self.x, self.y))

        # 子弹的行动
        for item in self.bullet_list:
            item.draw()
            item.update()

        # 移除无效的子弹

        tmp = []
        for item in self.bullet_list:
            if not item.is_over():
                tmp.append(item)
        self.bullet_list = tmp

    def fire(self):
        self.bullet_list.append(Bullet(self.x, self.y, self.screen))


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 800))
    pygame.key.set_repeat(100, 100)

    aircraft = Aircraft(screen)

    done = False

    shoot_frequency = 0
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]:
                    aircraft.update(event.key)

        screen.fill((255, 255, 255))
        aircraft.draw()

        if shoot_frequency % 15 == 0:
            aircraft.fire()
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

        pygame.display.update()
        fps_clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
