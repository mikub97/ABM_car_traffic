import pygame
import os

from pygame import font

from src.traffic.model import TrafficModel

model = TrafficModel()
screen = pygame.display.set_mode((model.width, model.height))
pygame.font.init()
WIDTH = model.width
HEIGHT = model.height
LANE_WIDTH = model.lane_width
NODE_SIZE = 20
FPS=20
WHITE = (255, 255, 255)
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
        self.rect.center = driver.pos
        self.text_surface = FONT.render(str(self.driver.unique_id), True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        pygame.Surface.blit(self.image, self.text_surface, (driver.car_size/4, 0))

    def update(self):
        self.rect.x = self.driver.pos[0]
        self.rect.y = self.driver.pos[1]

def draw_window():
    screen.fill(BLACK)
    for i in range(3):
        pygame.draw.line(screen, WHITE, (0, LANE_WIDTH * i), (WIDTH, LANE_WIDTH * i))

    for node in model.nodes[:-1]:
        draw_node(node,False)
    draw_node(model.nodes[-1],True)


def draw_node(node, is_final = False):
    if node.state == "RED":
        if (is_final):
            pygame.draw.rect(screen, RED, (node.position-NODE_SIZE, 0, NODE_SIZE, NODE_SIZE))
            text_render = FONT.render(str(node.nodeID[0]), True, WHITE)
            text_rect = text_render.get_rect(center=(node.position-NODE_SIZE + NODE_SIZE // 2, 0 + NODE_SIZE // 2))
            screen.blit(text_render, text_rect)
        else:
            pygame.draw.rect(screen, RED, (node.position, 0, NODE_SIZE, NODE_SIZE))
            text_render = FONT.render(str(node.nodeID[0]), True, WHITE)
            text_rect = text_render.get_rect(center=(node.position + NODE_SIZE // 2, 0 + NODE_SIZE // 2))
            screen.blit(text_render, text_rect)
            pygame.draw.line(screen, WHITE, (node.position, 0), (node.position, HEIGHT))
def main():
    cars = pygame.sprite.Group()
    for driver in model.drivers:
        cars.add(Car(driver))
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
        draw_window()
        cars.update()
        draw_window()
        cars.draw(screen)  # Draw all the sprites
        pygame.display.flip()
        # keys_pressed = pygame.key.get_pressed()
        model.step()

# main()


if __name__ == "__main__":
    main()
