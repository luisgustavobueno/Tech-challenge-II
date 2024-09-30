import random
import numpy as np
import pygame
import time
import math

# Configurações do Algoritmo Genético
POP_SIZE = 100
MUTATION_RATE = 0.8
NUM_GENERATIONS = 5
ELITISM_COUNT = 5
CELL_SIZE = 40
GRID_SIZE = 16
SLEEP = 0.01

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)


# Constantes de movimentação
OBSTACLE = 1
DESTINATION = 2
DRONE_POSITION = 3
FREE_PATH = 4

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

fix_grid_with_obstacle = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 2, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2],  # Drone começa no meio
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [2, 1, 0, 0, 0, 1, 0, 0],
]

fix_grid_without_obstacle = [
    [2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2],
    [0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0],
]

fix_grid_without_obstacleII = [
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

fix_grid_with_obstacleII = [
    [2, 0, 0, 1, 2, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 2],
    [0, 2, 1, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 3, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

BASE_GRID = fix_grid_with_obstacleII
delivery_points = []
start_position = None


def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


# Função de Fitness (minimizar a distância total da rota)
def calculate_fitness(route):
    total_distance = 0
    current_position = start_position
    for point in route:
        total_distance += calculate_distance(current_position, point)
        current_position = point
    return total_distance


# Seleção de pais usando torneio
def selection(population, fitnesses):
    selected = random.sample(list(zip(population, fitnesses)), k=2)
    return min(selected, key=lambda x: x[1])[0]


# Crossover para gerar novas rotas
def crossover(parent1, parent2):
    cut_point = random.randint(1, len(parent1) - 1)
    child = parent1[:cut_point]
    for point in parent2:
        if point not in child:
            child.append(point)
    return child


# Mutação: trocar posições de entrega aleatórias
def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route


# Geração inicial aleatória de rotas
def generate_population():
    population = []
    for _ in range(POP_SIZE):
        route = random.sample(delivery_points, len(delivery_points))
        population.append(route)
    return population


# Desenho da grade no pygame
def draw_grid(grid, target):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == OBSTACLE:
                pygame.draw.rect(screen, BLACK, rect)
            elif grid[y][x] == DRONE_POSITION:
                pygame.draw.rect(screen, BLUE, rect)
            elif [y, x] == target:
                pygame.draw.rect(screen, ORANGE, rect)
            elif grid[y][x] == DESTINATION:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, RED, rect, 1)
    pygame.display.flip()


def clamp_value(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def sort_random_position_to_move(grid, pos_y, pos_x, previous_position, target):
    new_position = [pos_y, pos_x]

    possible_positions = [
        [pos_y, pos_x - 1],  # left
        [pos_y, pos_x + 1],  # right
        [pos_y - 1, pos_x],  # up
        [pos_y + 1, pos_x],  # down
    ]
    possible_positions = list(filter(
        lambda pos: (0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE) and \
                    grid[pos[0]][pos[1]] != OBSTACLE and \
                    pos != previous_position,
        possible_positions
    ))

    smallest_distance = float('inf')
    for position in possible_positions:
        distance = calculate_distance(position, target)
        if distance < smallest_distance:
            smallest_distance = distance
            new_position = position

    return new_position


# Função para mover o drone célula por célula até o destino
def move_drone(route):
    current_position = start_position.copy()
    grid = [row[:] for row in BASE_GRID]  # Copia da grid original

    positions = []
    previous_position = None

    for point in route:
        while current_position != point:  # Enquanto não chega no destino
            previous_position = positions[-1] if positions else None
            positions.append(current_position)

            pos_y = current_position[0]
            pos_x = current_position[1]

            grid[pos_y][pos_x] = FREE_PATH

            moves_made = 0

            # Calcula a direção de movimento
            if pos_y < point[0] or pos_y > point[0]:
                if pos_y < point[0] and moves_made == 0:
                    if grid[pos_y + 1][pos_x] != OBSTACLE and [pos_y + 1, pos_x] not in positions:
                        pos_y += 1  # Move para baixo
                    else:
                        # move to a random position around the current position
                        [pos_y, pos_x] = sort_random_position_to_move(grid, pos_y, pos_x, previous_position, point)
                    moves_made += 1

                if pos_y > point[0] and moves_made == 0:
                    if grid[pos_y - 1][pos_x] != OBSTACLE and [pos_y - 1, pos_x] not in positions:
                        pos_y -= 1  # Move para cima
                    else:
                        # move to a random position around the current position
                        [pos_y, pos_x] = sort_random_position_to_move(grid, pos_y, pos_x, previous_position, point)
                    moves_made += 1

            elif pos_x < point[1] or pos_x > point[1]:
                if pos_x < point[1] and moves_made == 0:
                    if grid[pos_y][pos_x + 1] != OBSTACLE and [pos_y, pos_x + 1] not in positions:
                        pos_x += 1  # Move para a direita
                    else:
                        # move to a random position around the current position
                        [pos_y, pos_x] = sort_random_position_to_move(grid, pos_y, pos_x, previous_position, point)
                    moves_made += 1

                if pos_x > point[1] and moves_made == 0:
                    if grid[pos_y][pos_x - 1] != OBSTACLE and [pos_y, pos_x - 1] not in positions:
                        pos_x -= 1  # Move para a esquerda
                    else:
                        # move to a random position around the current position
                        [pos_y, pos_x] = sort_random_position_to_move(grid, pos_y, pos_x, previous_position, point)
                    moves_made += 1

            current_position = [pos_y, pos_x]

            # Atualiza a nova posição do drone
            grid[pos_y][pos_x] = DRONE_POSITION

            # Desenhar a nova grade
            draw_grid(grid, point)
            time.sleep(SLEEP)  # Pausa para simular o movimento gradual

            # pega as ultimas 8 posições para manter o histórico
            positions = positions[-8:]

    if current_position == route[-1]:
        print("Último ponto de entrega alcançado!")
        time.sleep(SLEEP)


# Lógica principal com Algoritmo Genético
def main():
    global delivery_points, start_position

    grid = BASE_GRID

    best_fitness_global = float("inf")
    best_route_global = None

    # Definir pontos de entrega e posição inicial do drone
    delivery_points = [
        [x, y]
        for x in range(GRID_SIZE)
        for y in range(GRID_SIZE)
        if grid[x][y] == DESTINATION
    ]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == DRONE_POSITION:
                start_position = [x, y]
                break

    # Gerar população inicial
    population = generate_population()
    print('population', population[0:2])

    for generation in range(NUM_GENERATIONS):
        # Avaliar a população
        fitnesses = [calculate_fitness(route) for route in population]
        print('fitnesses', fitnesses[0:2])

        # Selecionar a melhor população (elitismo)
        new_population = []
        elite_indices = np.argsort(fitnesses)[:ELITISM_COUNT]
        for i in elite_indices:
            new_population.append(population[i])

        print('elite_indices', elite_indices[0:2])
        print('new_population', new_population[0:2])

        # Criar nova geração com crossover e mutação
        while len(new_population) < POP_SIZE:
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

        # Mostrar a melhor rota da geração atual
        best_route = population[0]

        fitness = calculate_fitness(best_route)
        print(
            f"Geração {generation}, melhor rota: {best_route}, fitness: {fitness}"
        )

        if fitness < best_fitness_global:
            best_fitness_global = fitness
            best_route_global = best_route

        # Simular movimento do drone com a melhor rota
        move_drone(best_route)

    print()
    print(f"Melhor fitness encontrado: {best_fitness_global}")
    print(f"Melhor rota encontrada: {best_route_global}")

    pygame.quit()


if __name__ == "__main__":
    main()
