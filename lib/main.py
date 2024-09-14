import pygame
import time
from map import map  
CELL_SIZE = 40
GRID_SIZE = 16

WHITE = (255, 255, 255)

POPULATION_SIZE = 3

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 300, GRID_SIZE * CELL_SIZE))

fix_grid_with_obstacle = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 2, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2],  # Drone começa no meio
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [2, 1, 0, 0, 0, 1, 0, 0]
]

fix_grid_without_obstacle = [
    [2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2],  
    [0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0]
]

fix_grid_without_obstacleII = [
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  
    [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

fix_grid_with_obstacleII = [
    [2, 0, 0, 1, 2, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 2],
    [0, 2, 1, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 3, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0], 
    [0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
]


drone_simulation = map.DroneSimulation(GRID_SIZE, CELL_SIZE)
drone_simulation.grid = fix_grid_without_obstacleII
population = drone_simulation.generate_population(screen, POPULATION_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    delivery_order = drone_simulation.get_delivery_order()
    delivery_order = [{'position': point, 'visited': False} for point in delivery_order]
    drone_simulation.delivery_order = delivery_order 

    for delivery_point in delivery_order:
        if delivery_point['visited'] == False:
            running = drone_simulation.move_drone(screen, delivery_point['position'])
            delivery_point['visited'] = True

    running = False  

pygame.quit()
