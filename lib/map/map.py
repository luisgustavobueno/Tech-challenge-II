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
    SLEEP = 0.00

    class MAPINFO(Enum):
        OBSTACLE = 1
        DESTINATION = 2
        DRONE_POSITION = 3
        FREE_PATH = 4

    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = [[self.MAPINFO.FREE_PATH.value for _ in range(grid_size)] for _ in range(grid_size)]
        self.delivery_points = []
        self.delivery_order = []
        self.start_position = None

    def draw_grid(self, screen):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.grid[y][x] == self.MAPINFO.OBSTACLE.value:
                    pygame.draw.rect(screen, self.BLACK, rect)
                elif self.grid[y][x] == self.MAPINFO.DESTINATION.value:
                    pygame.draw.rect(screen, self.GREEN, rect)
                elif self.grid[y][x] == self.MAPINFO.DRONE_POSITION.value:
                    pygame.draw.rect(screen, self.BLUE, rect)
                else:
                    pygame.draw.rect(screen, self.WHITE, rect)
                pygame.draw.rect(screen, self.RED, rect, 1)

    def draw_line(self, screen, actual_position, target):
        actual_pixel = (actual_position[1] * self.cell_size + self.cell_size // 2, 
                        actual_position[0] * self.cell_size + self.cell_size // 2)
        target_pixel = (target[1] * self.cell_size + self.cell_size // 2, 
                        target[0] * self.cell_size + self.cell_size // 2)
        
        pygame.draw.line(screen, self.BLACK, actual_pixel, target_pixel, 3)

    def move_drone(self, screen, target):
        path = []
        while True:
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if self.grid[y][x] == self.MAPINFO.DRONE_POSITION.value:
                        self.grid[y][x] = self.MAPINFO.FREE_PATH.value
                        drone_position = [y, x]

            new_position = self.sort_position_to_move(drone_position, target)

            self.grid[new_position[0]][new_position[1]] = self.MAPINFO.DRONE_POSITION.value
            path.append(new_position)

            self.draw_grid(screen)
            self.draw_line(screen, new_position, target)
            pygame.display.flip()
            time.sleep(self.SLEEP)
            
            if new_position == target:
                return False, path

    @staticmethod
    def clamp_value(value, min_value, max_value):
        return max(min_value, min(value, max_value))


    def sort_position_to_move(self, actual_position, target):
        new_position = actual_position.copy()  
        old_position = actual_position.copy()
        while True:
            change_x_or_y = random.randint(0, 1)
            value_to_change = random.choice([-1, 1])

            new_position[change_x_or_y] += value_to_change
            new_position[change_x_or_y] = self.clamp_value(new_position[change_x_or_y], 0, self.grid_size - 1)

            value_of_position = self.grid[new_position[0]][new_position[1]]

            if value_of_position != self.MAPINFO.OBSTACLE.value: #DESVIA DO OBSTACULO
                new_distance = self.is_new_position_closer(new_position, old_position, target)
                if new_distance == True:
                    print(f"Nova posição: {new_position}")
                    return new_position                   
                else:
                    new_position = actual_position.copy()
            else:
                new_position = actual_position.copy()

    def calculate_distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


    def is_new_position_closer (self, new_position, old_position, target):
        old_position_distance = self.calculate_distance(old_position, target)
        new_position_distance = self.calculate_distance(new_position, target)

        if (new_position_distance < old_position_distance):
            return True
        else:
            return False

    def get_delivery_order(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[x][y] == self.MAPINFO.DRONE_POSITION.value:
                    self.start_position = [x, y]
                if self.grid[x][y] == self.MAPINFO.DESTINATION.value:
                    self.delivery_points.append([x, y])

        random.shuffle(self.delivery_points)  # Embaralha a lista in-place
        return self.delivery_points  # Retorna a lista embaralhada

    def generate_population(self, screen, population_size):
        total_population = []
        
        for _ in range(population_size):
            delivery_order = self.get_delivery_order()
            
            total_path = [] 
            
            for point in delivery_order:
                path = self.move_drone(screen, point) 
                total_path.extend(path[1])
            total_population.append(total_path)


        return total_population



