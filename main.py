from typing import List

import pygame

from classes.Cube import Cube
from classes.Camera import Camera

pygame.init()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

scale = 100

mainCamera: Camera = Camera()

environment: List[Cube] = []
cube1: Cube = Cube(environment, {'x': 3, 'y': 0, 'z': 0})

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    cube1.translate({'x': cube1.pos['x'] + 0.000, 'y': cube1.pos['y'] + 0.000, 'z': cube1.pos['z'] + 0.000})
    cube1.translate({"x": 0.001, "y": 0, "z": 0})
    cube1.scale({'x': 1, 'y': 1, 'z': 1})
    cube1.rotate({'x': 1, 'y': 2, 'z': 1})

    for item in environment:
        item.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
