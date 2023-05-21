import pygame
import os

from pygame import font

from src.traffic.model import TrafficModel

pygame.font.init()
pygame.mixer.init()
signal_img_width = 10
DRIVER_SIZE = 20
signal_img_height = signal_img_width*3
signal_img =  pygame.transform.scale(pygame.image.load('signals.jpg'),(signal_img_width,signal_img_height))
model = TrafficModel()

FPS=1
WIDTH = model.width
HEIGHT=model.height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic")
LANE_WIDTH = HEIGHT/model.n_lines
SHIFT_Y=DRIVER_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')

FONT = pygame.font.SysFont('comicsans', 13)


#
# SPACE = pygame.transform.scale(pygame.image.load(
#     os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(model):
    for i in range(3):
        pygame.draw.line(WIN, WHITE, (0, DRIVER_SIZE+LANE_WIDTH*i), (WIDTH, DRIVER_SIZE+LANE_WIDTH*i))

    for node in model.nodes:
        if node.state=="RED":
            pygame.draw.rect(WIN, RED, (node.position, 0, DRIVER_SIZE, DRIVER_SIZE))
            text_render = FONT.render(str(node.nodeID[0]), True, WHITE)
            text_rect = text_render.get_rect(center=(node.position + DRIVER_SIZE // 2, 0+DRIVER_SIZE//2))
            WIN.blit(text_render, text_rect)
            pygame.draw.line(WIN, WHITE, (node.position, 0), (node.position,HEIGHT))

    for driver in model.drivers:
        driver_x = driver.pos[0]
        driver_y = LANE_WIDTH/2+driver.current_lane[0]*LANE_WIDTH+SHIFT_Y
        pygame.draw.rect(WIN, WHITE, (driver_x, driver_y, DRIVER_SIZE, DRIVER_SIZE))
        text_render = FONT.render(str(driver.unique_id), True, BLACK)
        text_rect = text_render.get_rect(center=(driver.pos[0] + DRIVER_SIZE // 2, driver_y + DRIVER_SIZE // 2))
        WIN.blit(text_render, text_rect)
        pygame.display.update()


def main():
    for driver in model.drivers:
        print(driver)
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        model.step()
        draw_window(model)

main()


if __name__ == "__main__":
    main()
