from typing import List

import pygame
from pygame import Color

from utils.orthographic import orthographic_projection

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
cube1: Cube = Cube(environment)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    cube1.rotate({'x': 1, 'y': 2, 'z': 3})

    print(environment[0])

    projectedCubes = orthographic_projection(environment)

    for cube in projectedCubes:
        for vertex in cube:
            pygame.draw.circle(screen, Color(255,255,255), ((screen_width/2 + (vertex[0] * scale)), (screen_height/2 + (vertex[1] * scale))), 5)

    # pygame.draw.line(screen, Color(255, 255, 255), (0, 100), (100, 100))


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
