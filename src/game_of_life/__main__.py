import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TILE_SIZE = 10
GREY = (50, 50, 50)


class Cell(pygame.sprite.Sprite):
    def __init__(self, groups, pos: tuple[int, int], size=TILE_SIZE):
        if not self._validate_pos(pos):
            raise ValueError("Coordinates not divisible by TILE_SIZE")
        self._pos = pos  # private, read-only
        self._size = size  # if needed

        super().__init__(groups)  # Safe now that attributes are ready

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_frect(topleft=pos)
        self.alive = False

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    def __eq__(self, other):
        return isinstance(other, Cell) and self._pos == other._pos

    def __hash__(self):
        return hash(self._pos)

    @staticmethod
    def _validate_pos(pos: tuple[int, int]) -> bool:
        return all(coord % TILE_SIZE == 0 for coord in pos)

    def toggle(self):
        if not self.alive:
            self.image.fill((255, 255, 255, 255))
            self.alive = True
        else:
            self.image.fill((0, 0, 0, 0))
            self.alive = False

    def get_next_state(self, all_cells: dict[tuple[int, int], "Cell"]):
        nbrs = self.get_nbrs(all_cells)

        # game of life rules
        live_nbrs = sum([n.alive for n in nbrs])
        if self.alive:
            self.next_state = live_nbrs == 2 or live_nbrs == 3
        if not self.alive:
            self.next_state = live_nbrs == 3

    def update(self):
        self.alive = self.next_state
        if self.alive:
            self.image.fill((255, 255, 255, 255))
        else:
            self.image.fill((0, 0, 0, 0))

    def get_nbrs(self, cells: dict[tuple[int, int], "Cell"]):
        nbrs = []
        positions = [
            (-TILE_SIZE, -TILE_SIZE),
            (TILE_SIZE, -TILE_SIZE),
            (0, -TILE_SIZE),
            (-TILE_SIZE, 0),
            (TILE_SIZE, 0),
            (0, TILE_SIZE),
            (-TILE_SIZE, TILE_SIZE),
            (TILE_SIZE, TILE_SIZE),
        ]
        for i, j in positions:
            nbr_x = (self.pos[0] + i) % WINDOW_WIDTH
            nbr_y = (self.pos[1] + j) % WINDOW_HEIGHT
            nbrs.append(cells[(nbr_x, nbr_y)])
        return nbrs


def draw_grid(screen, tile_size: int):
    # draw vertical lines
    for i in range(tile_size, WINDOW_WIDTH, tile_size):
        pygame.draw.line(screen, GREY, (i, 0), (i, WINDOW_HEIGHT))

    # draw horizontal lines
    for i in range(tile_size, WINDOW_HEIGHT, tile_size):
        pygame.draw.line(screen, GREY, (0, i), (WINDOW_WIDTH, i))


def convert_pos_to_grid(pos: tuple[int, int]):
    x = pos[0] - pos[0] % TILE_SIZE
    y = pos[1] - pos[1] % TILE_SIZE
    return (x, y)


def get_all_cells(groups):
    cells = {}
    for i in range(0, WINDOW_WIDTH, TILE_SIZE):
        for j in range(0, WINDOW_HEIGHT, TILE_SIZE):
            cells[(i, j)] = Cell(groups, (i, j))
    return cells


def compute_next_state(cells):
    for _, cell in cells.items():
        cell.get_next_state(cells)


def main():
    print("Starting the Main-Loop!")
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    all_cells = get_all_cells(all_sprites)

    start = False
    while running:
        dt = clock.tick(10) / 1000  # convert to sec

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        if pygame.mouse.get_just_pressed()[0]:
            mpos = convert_pos_to_grid(pygame.mouse.get_pos())
            chosen_cell = all_cells[mpos]
            chosen_cell.toggle()

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            start = True

        if start:
            compute_next_state(all_cells)
            all_sprites.update()

        screen.fill("black")
        draw_grid(screen, TILE_SIZE)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
