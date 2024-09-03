import pygame
import time
from map import map

CELL_SIZE = 40
GRID_SIZE = 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

fix_grid = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 2, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2],  # Drone começa no meio
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 0, 0, 0, 1, 0, 0]  
]


path = [(4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7)]  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    delivery_order = map.get_delivery_order(fix_grid, GRID_SIZE)
    map.move_drone(screen, fix_grid, path, GRID_SIZE, CELL_SIZE)

    running = False  

pygame.quit()
