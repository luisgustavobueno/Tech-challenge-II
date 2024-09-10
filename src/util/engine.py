import pygame

from src.enum.colors import Colors
from src.enum.map_position import MapPosition
from src.map.drone_simulation import DroneSimulation


GRID_COLORS = {
    MapPosition.OBSTACLE: Colors.BLACK,
    MapPosition.DESTINATION: Colors.GREEN,
    MapPosition.DRONE_POSITION: Colors.BLUE
}


class Engine:
    screen: pygame.Surface

    def __init__(self, width: int, height: int):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(width, height))

    def handle_events(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.K_ESCAPE:
                    pygame.quit()

        except KeyboardInterrupt:
            pygame.quit()

    def draw(self, drone_simulation: DroneSimulation):
        # Clean grid
        self.screen.fill(Colors.WHITE)

        # Draw grid
        for y in range(drone_simulation.grid_size):
            for x in range(drone_simulation.grid_size):
                left = x * drone_simulation.cell_size
                top = y * drone_simulation.cell_size
                width = drone_simulation.cell_size
                height = drone_simulation.cell_size

                rect = pygame.Rect(left, top, width, height)

                color = GRID_COLORS.get(drone_simulation.grid[y][x])
                if color is not None:
                    pygame.draw.rect(
                        surface=self.screen,
                        color=color,
                        rect=rect
                    )
                    continue

                pygame.draw.rect(
                    surface=self.screen,
                    color=Colors.WHITE,
                    rect=rect
                )
                pygame.draw.rect(
                    surface=self.screen,
                    color=Colors.RED,
                    rect=rect,
                    width=1
                )

        pygame.display.flip()

    def run(self, drone_simulation: DroneSimulation):
        running = True
        while running:
            self.handle_events()

            self.draw(drone_simulation=drone_simulation)

        pygame.quit()
