from time import sleep
from typing import List, Tuple
import pygame
import random
import math
# import time
from enum import Enum
from colors import ORANGE, WHITE, BLACK, RED, GREEN, BLUE


class MAPINFO(Enum):
    OBSTACLE = 1
    DESTINATION = 2
    DRONE_POSITION = 3
    FREE_PATH = 4


class DroneSimulation:
    SLEEP: float
    grid_size: int
    cell_size: int
    grid: List[List[int]]
    start_position: Tuple[int, int]
    delivery_points: List[Tuple[int, int]]
    population: List[List[Tuple[int, int]]]

    def __init__(self, grid_size: int, cell_size: int, grid: List[List[int]]):
        self.SLEEP = 0.5
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = grid
        self.start_position, self.delivery_points = self.set_delivery_points()
        self.population = []

    @staticmethod
    def clamp_value(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    @staticmethod
    def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def move_drone_to(self, pos: Tuple[int, int]):
        if abs(self.start_position[0] - pos[0]) > 1:
            print(f"Moving more than one house horizontally:\npos: {pos}\nstart_position:{self.start_position}")
            return
        if abs(self.start_position[1] - pos[1]) > 1:
            print(f"Moving more than one house vertically:\npos: {pos}\nstart_position:{self.start_position}")
            return

        if pos == self.start_position:
            return

        if self.grid[pos[0]][pos[1]] == MAPINFO.OBSTACLE.value:
            return

        if self.grid[pos[0]][pos[1]] == MAPINFO.DESTINATION.value:
            found_index = self.delivery_points.index(pos)
            found_delivery_point = self.delivery_points.pop(found_index)
            print(f'Delivered {found_index+1}º delivery point at {found_delivery_point}')
            print(f'Pending deliveries {self.delivery_points}')

        self.grid[pos[0]][pos[1]] = MAPINFO.DRONE_POSITION.value
        self.grid[self.start_position[0]][self.start_position[1]] = MAPINFO.FREE_PATH.value
        print(f'Moving from {self.start_position} to {pos}')
        self.start_position = (pos[0], pos[1])

    def draw_routes(self, screen: pygame.Surface):
        # Clear grid
        WIDTH = screen.get_width()
        HEIGHT = screen.get_width()
        screen.fill(RED)
        screen.fill(WHITE, (WIDTH-299, 0, 300, HEIGHT))

        # Draw matrix
        for route in self.population:
            count = 1
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    # print('route', route, '[x][y]', x, y)
                    left = x * self.cell_size + 1
                    top = y * self.cell_size + 1
                    width = self.cell_size - 1
                    height = self.cell_size - 1
                    rect = pygame.Rect(left, top, width, height)
                    if self.grid[x][y] == MAPINFO.OBSTACLE.value:
                        pygame.draw.rect(screen, BLACK, rect)
                        continue

                    if self.grid[x][y] == MAPINFO.DESTINATION.value:
                        pygame.draw.rect(screen, GREEN, rect)
                        continue

                    if (x, y) in route:
                        _c = BLUE
                        _c.a = min(255, 10800 // count)
                        count += 1
                        pygame.draw.rect(screen, _c, rect)
                        continue

                    pygame.draw.rect(screen, WHITE, rect)
        # pygame.display.flip()

    def draw_drone(self, screen: pygame.Surface):
        # Draw drone
        x, y = self.start_position
        rect = pygame.Rect(x * self.cell_size+10, y * self.cell_size+10, self.cell_size-20, self.cell_size-20)
        pygame.draw.rect(screen, ORANGE, rect)
        # pygame.display.flip()

    def set_delivery_points(self) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        delivery_points = []
        start_position = None

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] == MAPINFO.DRONE_POSITION.value:
                    start_position = (x, y)
                if self.grid[x][y] == MAPINFO.DESTINATION.value:
                    delivery_points.append((x, y))

        if start_position is None:
            raise Exception("Could not find start position")

        return start_position, delivery_points

    def get_next_position(self, current_position: Tuple[int, int], target_position: Tuple[int, int]) -> Tuple[int, int]:
        possible_movements = [
            (current_position[0]-1, current_position[1]),  # Left
            (current_position[0], current_position[1]-1),  # Top
            (current_position[0] + 1, current_position[1]),  # Right
            (current_position[0], current_position[1] + 1),  # Bottom
        ]
        possible_movements = [
            move
            for move in possible_movements
            if (
                 move[0] <= self.grid_size -1 and
                 move[0] >= 0 and
                 move[1] <= self.grid_size -1 and
                 move[1] >= 0 and
                 self.grid[move[0]][move[1]] != MAPINFO.OBSTACLE.value
            )
        ]
        best_move = possible_movements[0]
        best_distance = self.calculate_distance(possible_movements[0], target_position)
        for move in possible_movements[1:]:
            distance = self.calculate_distance(move, target_position)
            if distance < best_distance:
                best_move = move
                best_distance = distance
        
        print({
            "current_position": current_position,
            "possible_movements": possible_movements,
            "best_move": best_move
        })
        return best_move

    def calculate_path(self, start_position: Tuple[int, int], target_position: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        current_position = start_position

        while current_position != target_position:
            next_position = self.get_next_position(current_position, target_position)
            path.append(next_position)
            current_position = next_position

        return path

    def calculate_fitness(self, path: List[Tuple[int, int]]) -> float:
        fitness = 0.0

        for i in range(len(path)-1):
            point_a = path[i]
            point_b = path[i+1]
            fitness += DroneSimulation.calculate_distance(point_a, point_b)

        return fitness

    def generate_random_population(self, population_size: int) -> List[List[Tuple[int, int]]]:
        population = []
        population_distances = []

        while len(population) < population_size:
            random_delivery_point = random.choice(self.delivery_points)
            path = self.calculate_path(
                start_position=self.start_position,
                target_position=random_delivery_point
            )
            path_distance = self.calculate_fitness(path)
            population.append(path)
            population_distances.append(path_distance)

        population = [p[0] for p in sorted(zip(population, population_distances), key=lambda x: x[1])]

        return population
