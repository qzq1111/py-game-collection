import pygame


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.key.set_repeat(100, 150)

    aircraft = pygame.image.load("./image/aircraft.png").convert_alpha()
    aircraft = pygame.transform.scale(aircraft, (100, 100))

    done = False

    x = 0
    y = 0

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x += 20
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x -= 20
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y -= 20
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y += 20

        screen.fill((255, 255, 255))
        screen.blit(aircraft, (x, y))

        pygame.display.update()
        fps_clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
