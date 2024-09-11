import sys
import time
import pygame
import itertools
from colors import WHITE
from grid import grid_default
from simulation import DroneSimulation

CELL_SIZE = 40
GRID_SIZE = len(grid_default)

POPULATION_SIZE = 10
N_GENERATIONS = 10
MUTATION_PROBABILITY = 0.5

FPS = 30

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 300, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Drone Path Optimization")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1

drone_simulation = DroneSimulation(GRID_SIZE, CELL_SIZE, grid_default)

# create inital population
population = drone_simulation.generate_random_population(POPULATION_SIZE)

best_fitness_values = []
best_solutions = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    generation = next(generation_counter)
    if generation >= N_GENERATIONS:
        running = False

    screen.fill(WHITE)

    # TODO: implement calculate_fitness
    # we could check the population_distances to get the best solutions with shortest distance
    # best_fitness = drone_simulation.calculate_fitness(population[0])
    # best_solution = population[0]

    # best_fitness_values.append(best_fitness)
    # best_solutions.append(best_solution)

    drone_simulation.draw_routes(screen)

    # TODO: generate new population
    new_population = [population[0]]  # Keep the best individual: ELITISM

    while len(new_population) < POPULATION_SIZE:
        # TODO: selection

        # TODO: crossover

        # TODO: mutation

        new_population.append([]) # TODO

    time.sleep(5)

    pygame.display.flip()
    clock.tick(FPS)

    # remove this
    running = False

pygame.quit()
sys.exit()
