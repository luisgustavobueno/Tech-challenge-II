from random import randint
from typing import List, Tuple


def two_point_crossover(
    path_a: List[Tuple[int, int]],
    path_b: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    start_index = randint(0, len(path_a)-1)
    end_index = randint(start_index+1, len(path_a))

    new_path = path_a[:]
    new_path[start_index:end_index] = path_b[start_index:end_index]
    return new_path


def order_crossover(
    path_a: List[Tuple[int, int]],
    path_b: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    start_index = randint(0, len(path_a)-1)
    end_index = randint(start_index+1, len(path_a))

    new_path = path_a[start_index:end_index]

    # Pick elements before start index
    remaining_indexes = [
        i
        for i in range(0, start_index)
    ]
    # Pick elements past end_index index
    remaining_indexes += [
        i
        for i in range(end_index+1, len(path_a))
    ]

    # Pick remaining points and insert them in the remaining indexes
    # Remaining indexes length may differ from remaining points,
    # but zip takes care of handling until the array with smaller length
    remaining_points = [point for point in path_b if point not in new_path]

    for pos, point in zip(remaining_indexes, remaining_points):
        new_path.insert(pos, point)

    # print(path_a, new_path)
    return new_path
