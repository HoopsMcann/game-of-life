import pygame

from random import randint


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TILE_SIZE = 10
GREY = (50, 50, 50)


class Cell(pygame.sprite.Sprite):
    def __init__(self, groups, size=TILE_SIZE):
        super().__init__(groups)
        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    def update(self, dt):
        pass
        # keys = pygame.key.get_pressed()


def draw_grid(screen, tile_size: int):
    # draw vertical lines
    for i in range(tile_size, WINDOW_WIDTH, tile_size):
        pygame.draw.line(screen, GREY, (i, 0), (i, WINDOW_HEIGHT))

    # draw horizontal lines
    for i in range(tile_size, WINDOW_HEIGHT, tile_size):
        pygame.draw.line(screen, GREY, (0, i), (WINDOW_WIDTH, i))


def main():
    print("Starting the Main-Loop!")
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    cell = Cell(all_sprites)
    while running:
        dt = clock.tick() / 1000  # convert to sec

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        all_sprites.update(dt)

        # blit places the surface in the rectangle
        screen.fill("black")
        draw_grid(screen, TILE_SIZE)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
