from typing import List, Tuple
import pygame
import random
import math
from colors import ORANGE, WHITE, BLACK, RED, GREEN

class MOVE:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    BOTTOM_RIGHT = (1, 1)
    BOTTOM_LEFT = (-1, 1)
    TOP_LEFT = (-1, -1)
    TOP_RIGHT = (1, -1)
    NEUTRAL = (0, 0)


class MAPINFO:
    OBSTACLE = 1
    DESTINATION = 2
    DRONE_POSITION = 3
    FREE_PATH = 4


AVAILABLE_MOVEMENTS = [
    MOVE.LEFT,
    MOVE.UP,
    MOVE.RIGHT,
    MOVE.DOWN,
    # MOVE.TOP_LEFT,
    # MOVE.TOP_RIGHT,
    # MOVE.BOTTOM_LEFT,
    # MOVE.BOTTOM_RIGHT,
]

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

    def move_drone_to(self, move: Tuple[int, int]):
        next_pos = (self.start_position[0]+move[0], self.start_position[1]+move[1])

        if move == MOVE.NEUTRAL:
            print("Move was neutral")
            return

        if next_pos[0] < 0 or next_pos[0] >= len(self.grid[0]):
            print("Cannot move horizontally - Out of bounds")
            return

        if next_pos[1] < 0 or next_pos[1] >= len(self.grid):
            print("Cannot move horizontally - Out of bounds")
            return

        if self.grid[next_pos[0]][next_pos[1]] == MAPINFO.OBSTACLE:
            return

        if self.grid[next_pos[0]][next_pos[1]] == MAPINFO.DESTINATION:
            found_index = self.delivery_points.index(next_pos)
            found_delivery_point = self.delivery_points.pop(found_index)
            print(f'Delivered {found_index+1}° delivery point at {found_delivery_point}')
            print(f'Pending deliveries {self.delivery_points}')

            if len(self.delivery_points) == 0:
                raise Exception("Delivered everything!")

        self.grid[next_pos[0]][next_pos[1]] = MAPINFO.DRONE_POSITION
        self.grid[self.start_position[0]][self.start_position[1]] = MAPINFO.FREE_PATH
        print(f'Moving from {self.start_position} to {(self.start_position[0]+move[0],self.start_position[1]+move[1])}')
        self.start_position = next_pos

    def draw_routes(self, screen: pygame.Surface):
        # Clear grid
        WIDTH = screen.get_width()
        HEIGHT = screen.get_width()
        screen.fill(RED)
        screen.fill(WHITE, (WIDTH-299, 0, 300, HEIGHT))

        # Draw matrix
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                left = x * self.cell_size + 1
                top = y * self.cell_size + 1
                width = self.cell_size - 1
                height = self.cell_size - 1
                rect = pygame.Rect(left, top, width, height)
                if self.grid[x][y] == MAPINFO.OBSTACLE:
                    pygame.draw.rect(screen, BLACK, rect)
                    continue

                if self.grid[x][y] == MAPINFO.DESTINATION:
                    pygame.draw.rect(screen, GREEN, rect)
                    continue

                pygame.draw.rect(screen, WHITE, rect)

    def draw_drone(self, screen: pygame.Surface):
        # Draw drone
        x, y = self.start_position
        rect = pygame.Rect(x * self.cell_size+10, y * self.cell_size+10, self.cell_size-20, self.cell_size-20)
        pygame.draw.rect(screen, ORANGE, rect)

    def set_delivery_points(self) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        delivery_points = []
        start_position = None

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] == MAPINFO.DRONE_POSITION:
                    start_position = (x, y)
                if self.grid[x][y] == MAPINFO.DESTINATION:
                    delivery_points.append((x, y))

        if start_position is None:
            raise Exception("Could not find start position")

        return start_position, delivery_points

    def get_random_move(self, position: Tuple[int, int]) -> Tuple[int, int]:
        possible_movements = [
            move
            for move in AVAILABLE_MOVEMENTS
            if (
                 position[0]+move[0] <= self.grid_size -1 and
                 position[0]+move[0] >= 0 and
                 position[1]+move[1] <= self.grid_size -1 and
                 position[1]+move[1] >= 0 and
                 self.grid[position[0]+move[0]][position[1]+move[1]] != MAPINFO.OBSTACLE
            )
        ]

        # Pick random possible move
        return random.choice(possible_movements)

    def get_best_move(self, position: Tuple[int, int], target: Tuple[int, int]) -> Tuple[int, int]:
        possible_movements = [
            move
            for move in AVAILABLE_MOVEMENTS
            if (
                 position[0]+move[0] <= self.grid_size -1 and
                 position[0]+move[0] >= 0 and
                 position[1]+move[1] <= self.grid_size -1 and
                 position[1]+move[1] >= 0 and
                 self.grid[position[0]+move[0]][position[1]+move[1]] != MAPINFO.OBSTACLE
            )
        ]

        # Pick move according to smaller distance
        best_move = possible_movements[0]
        best_distance = self.calculate_distance(
            point1=(position[0]+best_move[0], position[1]+best_move[1]),
            point2=target
        )

        for move in possible_movements[1:]:
            distance = self.calculate_distance(
                point1=(position[0]+move[0], position[1]+move[1]),
                point2=target
            )
            if distance < best_distance:
                best_move = move
                best_distance = distance

        print({
            "best_move": best_move,
            "best_distance": best_distance,
        })
        return best_move

    def calculate_fitness(self, move_list: List[Tuple[int, int]]) -> float:
        fitness = 0.0

        for i in range(len(move_list)-1):
            point_a = (self.start_position[0]+move_list[i][0], self.start_position[1]+move_list[i][1])
            point_b = (point_a[0]+move_list[i+1][0], point_a[1]+move_list[i+1][1])
            fitness += DroneSimulation.calculate_distance(point_a, point_b)

        return fitness

    def convert_move_list_to_path(
        self,
        start_position: Tuple[int, int],
        move_list: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        path = [start_position]
        pos = start_position

        for move in move_list:
            pos = (pos[0] + move[0], pos[1]+move[1])
            path.append(pos)

        return path

    def generate_random_population(self, population_size: int) -> List[List[Tuple[int, int]]]:
        population = []
        population_distances = []

        while len(population) < population_size:
            current_position = self.start_position
            move_list = []
            best_distance = 0.0

            delivery_points = self.delivery_points[:]

            while True:
                if not delivery_points:
                    break

                delivery_points_distances = [
                    self.calculate_distance(
                        point1=current_position,
                        point2=point
                    )
                    for point in delivery_points
                ]
                delivery_points_with_distances = sorted(zip(delivery_points, delivery_points_distances), key=lambda x: x[1])
                best_delivery_point = delivery_points_with_distances[0][0]

                # Pick move based on distance
                # best_move = self.get_best_move(
                #     position=current_position,
                #     target=best_delivery_point
                # )

                # Pick move randomly
                best_move = self.get_random_move(position=current_position)

                best_distance += self.calculate_distance(
                    point1=(current_position[0]+best_move[0], current_position[1]+best_move[1]),
                    point2=best_delivery_point
                )
                current_position = (current_position[0]+best_move[0], current_position[1]+best_move[1])
                if current_position == best_delivery_point:
                    delivery_points.pop(delivery_points.index(best_delivery_point))

                move_list.append(best_move)

            population.append(move_list)
            population_distances.append(best_distance)


        population = [p[0] for p in sorted(zip(population, population_distances), key=lambda x: x[1])]

        return population
