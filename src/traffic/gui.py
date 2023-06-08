import warnings

import pygame
from pygame.locals import *

from src.traffic.model import TrafficModel

pygame.font.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT = pygame.font.SysFont('comicsans', 13)


class Car(pygame.sprite.Sprite):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.image = pygame.Surface((driver.car_size, driver.car_size))
        self.image.fill(WHITE)  # Replace with car image loading or drawing logic
        self.rect = self.image.get_rect()
        self.rect.center = (driver.pos[0], 0)
        self.is_visible = False
        self.text_surface = FONT.render(str(self.driver.unique_id), True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        pygame.Surface.blit(self.image, self.text_surface, (driver.car_size / 4, 0))

    def update(self):
        if self.driver is None or self.driver.pos is None:
            self.kill()
            print(f"The driver {self.driver.unique_id} is DEAD")
            return
        self.is_visible = self.driver.pos[0] > 0
        self.rect.x = self.driver.pos[0]
        self.rect.y = self.driver.pos[1]


class GUI:
    def __init__(self, model):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.model = model
        self.screen = pygame.display.set_mode((model.width, model.height))
        self.width = self.model.width
        self.height = self.model.height
        self.lane_width = self.model.lane_width
        self.node_size = 20
        self.fps = model.fps
        pygame.display.set_caption("Traffic")

        self.cars = pygame.sprite.Group()
        for driver in self.model.drivers_schedule.agents:
            self.cars.add(Car(driver))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.is_running = False

        keys = pygame.key.get_pressed()
        slow_down_drivers = []
        # Perform actions based on key states
        if keys[K_0]:
            slow_down_drivers.append(0)
        for driver in self.model.drivers_schedule.agents:
            if driver.unique_id in slow_down_drivers:
                driver.max_speed = (driver.max_speed[0]-0.0001,)
                print("Driver 1 max speed is",driver.max_speed)

    def update(self):
        self.model.step()
        if (len(self.model.killed_drivers) == self.model.n_agents):
            self.model.data_collector_save()
            self.is_running=False

    def render(self):
        self.screen.fill((255, 255, 255))
        # Draw GUI elements here
        self.draw_window()
        self.cars.update()
        self.draw_window()
        visible_cars = pygame.sprite.Group()

        for car in self.cars:
            if car.is_visible:
                visible_cars.add(car)
        visible_cars.draw(self.screen)  # Draw all the sprites
        pygame.display.flip()

    def draw_node(self, node, is_final=False):
        if node.state == "red":
            col = RED
        elif node.state == "yellow":
            col = YELLOW
        else:
            col = GREEN
        if (is_final):
            pygame.draw.rect(self.screen, col, (node.pos[0] - self.node_size, 0, self.node_size, self.node_size))
            text_render = FONT.render(str(node.unique_id), True, WHITE)
            text_rect = text_render.get_rect(
                center=(node.pos[0] - self.node_size + self.node_size // 2, 0 + self.node_size // 2))
            self.screen.blit(text_render, text_rect)
        else:
            pygame.draw.rect(self.screen, col, (node.pos[0], 0, self.node_size, self.node_size))
            text_render = FONT.render(str(node.unique_id), True, WHITE)
            text_rect = text_render.get_rect(center=(node.pos[0] + self.node_size // 2, 0 + self.node_size // 2))
            self.screen.blit(text_render, text_rect)
            pygame.draw.line(self.screen, WHITE, (node.pos[0], 0), (node.pos[0], self.height))

    def draw_window(self):
        self.screen.fill(BLACK)
        for i in range(3):
            pygame.draw.line(self.screen, WHITE, (0, self.lane_width * i), (self.width, self.lane_width * i))

        for node in self.model.nodes[:-1]:
            self.draw_node(node, False)
        self.draw_node(self.model.nodes[-1], True)

    def run(self):
        pygame.display.flip()
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == "__main__":
    gui = GUI(TrafficModel())
    gui.run()
