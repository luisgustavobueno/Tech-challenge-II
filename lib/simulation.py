import pygame
import random
import math
import time
from enum import Enum
from colors import WHITE, BLACK, RED, GREEN, BLUE

class DroneSimulation:
    SLEEP = 0.5

    class MAPINFO(Enum):
        OBSTACLE = 1
        DESTINATION = 2
        DRONE_POSITION = 3
        FREE_PATH = 4

    def __init__(self, grid_size, cell_size, grid):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = grid
        self.grid_cells_count = grid_size * grid_size
        self.start_position, self.end_position, self.delivery_points = self.set_delivery_points()
        self.population = []
        self.population_distances = []

    @staticmethod
    def clamp_value(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def draw_routes(self, screen):
        for route in self.population:
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    # print('route', route, '[y][x]', y, x)
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    if self.grid[y][x] == self.MAPINFO.OBSTACLE.value:
                        pygame.draw.rect(screen, BLACK, rect)
                    elif self.grid[y][x] == self.MAPINFO.DESTINATION.value:
                        pygame.draw.rect(screen, GREEN, rect)
                    elif (y, x) in route:
                        pygame.draw.rect(screen, BLUE, rect)
                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, RED, rect, 1)

            pygame.display.flip()
            time.sleep(self.SLEEP)

    def set_delivery_points(self):
        delivery_points = []
        start_position = None
        end_position = None

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[x][y] == self.MAPINFO.DRONE_POSITION.value:
                    start_position = (x, y)
                if self.grid[x][y] == self.MAPINFO.DESTINATION.value:
                    delivery_points.append((x, y))

        end_position = delivery_points.pop()
        print('delivery_points', delivery_points)

        return start_position, end_position, delivery_points

    def get_next_position(self, current_position, target_position):
        old_position = list(current_position)
        new_position = list(current_position)

        # greedy algorithm - we are not going to consider all the possible cells
        while True:
            x_or_y = random.randint(0, 1) # 0 = x, 1 = y
            direction = random.choice([-1, 1]) # -1 = left or up, 1 = right or down

            new_position[x_or_y] += direction
            new_position[x_or_y] = self.clamp_value(new_position[x_or_y], 0, self.grid_size - 1)

            # not considering obstacles initially
            old_position_distance = self.calculate_distance(old_position, target_position)
            new_position_distance = self.calculate_distance(new_position, target_position)
            if new_position_distance < old_position_distance:
                return tuple(new_position), new_position_distance

            new_position = list(current_position)

    def calculate_path(self, start_position, target_position):
        path = []
        current_position = start_position
        path_distance = 0

        while current_position != target_position:
            next_position, distance = self.get_next_position(current_position, target_position)
            path.append(next_position)
            current_position = next_position
            path_distance += distance

        return path, path_distance

    def generate_random_population(self, population_size):
        self.population = []
        self.population_distances = []

        while len(self.population) < population_size:
            random_delivery_points = self.delivery_points.copy()
            random.shuffle(random_delivery_points)

            # keep the start and end position
            random_delivery_points.insert(0, self.start_position)
            random_delivery_points.append(self.end_position)
            print('random_delivery_points', random_delivery_points)

            route = []
            route_distance = 0
            # for each delivery point, we calculate the path between the previous position and the delivery point
            for i in range(1, len(random_delivery_points)):
                path, path_distance = self.calculate_path(random_delivery_points[i - 1], random_delivery_points[i])
                route.extend(path)
                route_distance += path_distance

            route.insert(0, self.start_position)
            route.append(self.end_position)
            print('route', route[0:10], 'len', len(route))

            self.population.append(route)
            self.population_distances.append(route_distance)

        print('self.population', self.population[0][0:10], 'len', len(self.population))
        print('self.population_distances', self.population_distances)
        return self.population
