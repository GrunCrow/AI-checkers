import pygame

# sizes
WIDTH, HEIGHT = 800, 800    # window size
ROWS, COLS = 10, 10           # board size (8x8)
SQUARE_SIZE = WIDTH//COLS   # board square size

# RGB colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player colours
WHITE = (255, 255, 255)
PLAYER_WHITE = (205, 205, 205)

BLACK = (0, 0, 0)
PLAYER_BLACK = (50, 50, 50)

GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
