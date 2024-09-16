from random import choices
import sys
import time
from typing import List, Tuple
import pygame
import itertools
from colors import WHITE
from grid import grid_default
from crossover import order_crossover, two_point_crossover
from simulation import DroneSimulation

CELL_SIZE = 40
GRID_SIZE = len(grid_default)

POPULATION_SIZE = 10
N_GENERATIONS = 1000
MUTATION_PROBABILITY = 0.5

FPS = 1

pygame.init()
WIDTH = GRID_SIZE * CELL_SIZE + 300
HEIGHT = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Path Optimization")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1

drone_simulation = DroneSimulation(GRID_SIZE, CELL_SIZE, grid_default)

# create inital population
population = drone_simulation.generate_random_population(POPULATION_SIZE)
drone_simulation.population = population

best_fitness_values = []
best_solutions: List[List[Tuple[int, int]]] = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                break

    generation = next(generation_counter)
    if generation >= N_GENERATIONS:
        running = False

    screen.fill(WHITE)

    # we could check the population_distances to get the best solutions with shortest distance
    best_fitness = drone_simulation.calculate_fitness(population[0])
    best_solution = population[0]
    for i in range(1, len(population)):
        fitness = drone_simulation.calculate_fitness(population[i])
        if fitness >= best_fitness:
            continue
        best_solution = population[i]
        best_fitness = fitness

    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    # Generate new population
    new_population = []  # Keep the best individual: ELITISM

    while len(new_population) < POPULATION_SIZE:
        # Selection - Pick at random
        selected_a, selected_b = choices(
            population,
            k=2,
            weights=[drone_simulation.calculate_fitness(p) for p in population]
        )

        # Crossover
        path = order_crossover(selected_a, selected_b)
        # path = two_point_crossover(selected_a, selected_b)

        # TODO mutation - Swap neighbor points(makes sense? drone should not move more than one house per draw)
        # should_mutate = randint(0, 1)
        # if should_mutate:
        #     index_to_mutate = randint(0, len(path)-1)
        #     aux = path[index_to_mutate]
        #     path[index_to_mutate] = path[index_to_mutate+1]
        #     path[index_to_mutate+1] = aux

        print('>', path)
        new_population.append(path)

    drone_simulation.population = new_population
    drone_simulation.move_drone_to(new_population[0][0])
    drone_simulation.draw_routes(screen)
    drone_simulation.draw_drone(screen)
    time.sleep(0.1)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
