
import pygame
import random
import math
import time
from enum import Enum

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

delivery_points = []
delivery_order = []
start_position = None

class MapInfo(Enum):
    OBSTACLE = 1
    DESTINATION = 2
    DRONE_POSITION = 3
    FREE_PATH = 4

def draw_grid(screen, grid, GRID_SIZE, CELL_SIZE):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == MapInfo.OBSTACLE.value: 
                pygame.draw.rect(screen, BLACK, rect)
            elif grid[y][x] == MapInfo.DESTINATION.value: 
                pygame.draw.rect(screen, GREEN, rect)           
            elif grid[y][x] == MapInfo.DRONE_POSITION.value:  
                pygame.draw.rect(screen, BLUE, rect)
            else:  
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, RED, rect, 1)

def move_drone(screen, grid, path, GRID_SIZE, CELL_SIZE):
    for pos in path:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if grid[y][x] == MapInfo.DRONE_POSITION.value:
                    grid[y][x] = MapInfo.FREE_PATH.value

        grid[pos[0]][pos[1]] = MapInfo.DRONE_POSITION.value
        
        draw_grid(screen, grid, GRID_SIZE, CELL_SIZE)
        pygame.display.flip()

        time.sleep(0.5)  

def get_delivery_order(grid, GRID_SIZE):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[x][y] == MapInfo.DRONE_POSITION.value:
                start_position = [x, y]
            if grid[x][y] == MapInfo.DESTINATION.value:
                delivery_points.append([x, y]) 

    distancias = [(point, calculate_distance(start_position, point)) for point in delivery_points]
    distancias.sort(key=lambda x: x[1]) 

    return [point for point, _ in distancias] 

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    