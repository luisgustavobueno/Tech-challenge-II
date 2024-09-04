import pygame
import time
from map import map  
CELL_SIZE = 40
GRID_SIZE = 8

WHITE = (255, 255, 255)

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

drone_simulation = map.DroneSimulation(GRID_SIZE, CELL_SIZE)
drone_simulation.grid = fix_grid  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    delivery_order = drone_simulation.get_delivery_order()
    drone_simulation.move_drone(screen, path)

pygame.quit()
