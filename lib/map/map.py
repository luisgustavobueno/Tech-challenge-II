import pygame
import random
import math
import time
from enum import Enum

class DroneSimulation:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)

    class MapInfo(Enum):
        OBSTACLE = 1
        DESTINATION = 2
        DRONE_POSITION = 3
        FREE_PATH = 4

    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = [[self.MapInfo.FREE_PATH.value for _ in range(grid_size)] for _ in range(grid_size)]
        self.delivery_points = []
        self.delivery_order = []
        self.start_position = None

    def draw_grid(self, screen):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.grid[y][x] == self.MapInfo.OBSTACLE.value:
                    pygame.draw.rect(screen, self.BLACK, rect)
                elif self.grid[y][x] == self.MapInfo.DESTINATION.value:
                    pygame.draw.rect(screen, self.GREEN, rect)
                elif self.grid[y][x] == self.MapInfo.DRONE_POSITION.value:
                    pygame.draw.rect(screen, self.BLUE, rect)
                else:
                    pygame.draw.rect(screen, self.WHITE, rect)
                pygame.draw.rect(screen, self.RED, rect, 1)

    def move_drone(self, screen, path):
        for pos in path:
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if self.grid[y][x] == self.MapInfo.DRONE_POSITION.value:
                        self.grid[y][x] = self.MapInfo.FREE_PATH.value
                        drone_position = [y, x]

            new_position = self.sort_position_to_move(drone_position)
            self.grid[new_position[0]][new_position[1]] = self.MapInfo.DRONE_POSITION.value

            self.draw_grid(screen)
            pygame.display.flip()
            time.sleep(0.1)

    @staticmethod
    def clamp_value(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    def sort_position_to_move(self, actual_position):
        while True:
            change_x_or_y = random.randint(0, 1)
            value_to_change = random.randint(-1, 1)

            actual_position[change_x_or_y] += value_to_change
            actual_position[change_x_or_y] = self.clamp_value(actual_position[change_x_or_y], 0, self.grid_size - 1)

            value_of_position = self.grid[actual_position[0]][actual_position[1]]

            if value_of_position != self.MapInfo.OBSTACLE.value:
                break 

        print(f"Posição atual: {actual_position}")
        return actual_position


    def get_delivery_order(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[x][y] == self.MapInfo.DRONE_POSITION.value:
                    self.start_position = [x, y]
                if self.grid[x][y] == self.MapInfo.DESTINATION.value:
                    self.delivery_points.append([x, y])

        distancias = [(point, self.calculate_distance(self.start_position, point)) for point in self.delivery_points]
        distancias.sort(key=lambda x: x[1])

        return [point for point, _ in distancias]

    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
