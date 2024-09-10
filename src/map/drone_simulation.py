from typing import List
import math
import random

from src.enum.map_position import MapPosition


class DroneSimulation:
    grid_size: int
    cell_size: int
    delivery_points: List[List[int]]
    delivery_order: List[List[int]]
    start_position: List[int]
    grid: List[List[int]]

    def __init__(self, grid_size: int, cell_size: int):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = [
            [
                MapPosition.FREE_PATH
                for _ in range(grid_size)
            ]
            for _ in range(grid_size)
        ]
        self.delivery_points = []
        self.delivery_order = []
        self.start_position = [0, 0]

    def move_drone(self, target: List[int]):
        drone_position = None

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == MapPosition.DRONE_POSITION:
                    self.grid[y][x] = MapPosition.FREE_PATH
                    drone_position = [y, x]

        if drone_position is None:
            raise ValueError("Sem posicao do drone")

        new_pos = self.sort_position_to_move(drone_position, target)
        self.grid[new_pos[0]][new_pos[1]] = MapPosition.DRONE_POSITION

        if new_pos == target:
            raise ValueError("Target encontrado!")

    def clamp_value(self, value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))

    def sort_position_to_move(self, actual_position: List[int], target: List[int]) -> List[int]:
        new_pos = actual_position.copy()
        old_position = actual_position.copy()

        while True:
            change_x = random.randint(0, 1)
            value_to_change = random.choice([-1, 1])

            new_pos[change_x] += value_to_change
            new_pos[change_x] = int(self.clamp_value(
                value=new_pos[change_x],
                min_value=0,
                max_value=self.grid_size - 1
            ))

            value_of_position = self.grid[new_pos[0]][new_pos[1]]

            if value_of_position == MapPosition.OBSTACLE:
                new_pos = actual_position.copy()
                return new_pos

            new_distance = self.is_new_position_closer(
                new_position=new_pos,
                old_position=old_position,
                target=target
            )
            if new_distance == True:
                print(f"Nova posição: {new_pos}")
                return new_pos

            new_pos = actual_position.copy()
            return new_pos

    def calculate_distance(self, point1: List[int], point2: List[int]) -> float:
        '''
        a² + b² = distance²
        '''
        a = (point2[0] - point1[0])
        b = (point2[1] - point1[1])
        distance = math.sqrt(a ** 2 + b ** 2)
        return distance

    def is_new_position_closer(self, new_position: List[int], old_position: List[int], target) -> bool:
        old_position_distance = self.calculate_distance(old_position, target)
        new_position_distance = self.calculate_distance(new_position, target)

        return new_position_distance < old_position_distance

    def get_delivery_order(self) -> List[List[int]]:
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[x][y] == MapPosition.DRONE_POSITION:
                    self.start_position = [x, y]

                if self.grid[x][y] == MapPosition.DESTINATION:
                    self.delivery_points.append([x, y])

        distances = [
            (point, self.calculate_distance(self.start_position, point))
            for point in self.delivery_points
        ]
        distances.sort(key=lambda x: x[1])

        return [point for point, _ in distances]
