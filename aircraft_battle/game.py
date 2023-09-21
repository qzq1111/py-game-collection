import pygame


class Location(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Aircraft(object):

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.location = None  # 飞机位置
        self.aircraft_image = None  # 飞机贴图

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

        x = scree_center_x - (self.aircraft_image.get_width() / 2)
        y = self.screen.get_height() - self.aircraft_image.get_height()
        self.location = Location(x, y)

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
            self.location.x += 10
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.location.x -= 10
        elif key == pygame.K_UP or key == pygame.K_w:
            self.location.y -= 10
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.location.y += 10

        if self.location.x > self.screen.get_width() - self.aircraft_image.get_width():
            self.location.x = self.screen.get_width() - self.aircraft_image.get_width()

        if self.location.x < 0:
            self.location.x = 0

        if self.location.y > self.screen.get_height() - self.aircraft_image.get_height():
            self.location.y = self.screen.get_height() - self.aircraft_image.get_height()

        if self.location.y < 0:
            self.location.y = 0

        return

    def draw(self):
        self.screen.blit(self.aircraft_image, (self.location.x, self.location.y))


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 800))
    pygame.key.set_repeat(100, 100)

    aircraft = Aircraft(screen)

    done = False

    x = 0
    y = 0

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

        pygame.display.update()
        fps_clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
