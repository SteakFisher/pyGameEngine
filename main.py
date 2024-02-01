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

environment: List[Cube] = [Cube()]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    projectedCubes = orthographic_projection(environment)

    for cube in projectedCubes:
        for vertex in cube:
            print(vertex)
            pygame.draw.circle(screen, Color(255,255,255), ((screen_width/2 + (vertex[0] * 50)), (screen_height/2 + (vertex[1] * 50))), 5)
            print(((screen_width + (vertex[0] * 50))/2), ((screen_height + (vertex[1]))/2))

    pygame.draw.line(screen, Color(255, 255, 255), (0, 100), (100, 100))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
