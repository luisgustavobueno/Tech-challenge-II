from typing import List


class DeliveryPoint:
    position: List[int]
    visited: bool

    def __init__(self, position: List[int]):
        self.position = position
        self.visited = False
