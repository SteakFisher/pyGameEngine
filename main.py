from typing import List

import pygame
from pygame import Color

from newClasses.Camera import Camera
from newClasses.Cube import Cube
from newClasses.Object import Object
from utils.types import Position, Rotation, Scaling

pygame.init()

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

environment: List[Object] = []

camera: Camera = Camera(environment, pos=Position(0, 0, -4))

cube1: Cube = Cube(environment, screen, camera, Position(0, 0, 8), Rotation(0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # camera.setPosition(camera.pos + Position(0, 0, 0.05))
    camera.setRotation(camera.rot + Rotation(0, 1, 0))

    cube1.setPosition(cube1.pos + Position(0.01, 0, 0.0))
    cube1.setRotation(cube1.rot + Rotation(1, 1, 1))
    # cube1.setScale(cube1.scale + Scaling(0.01, 0.01, 0.01))

    pygame.draw.circle(screen, Color(255, 255, 255), (screen.get_width() / 2, screen.get_height() / 2), 5)

    for obj in environment:
        obj.tick()

    pygame.display.flip()

    clock.tick(60)
    # clock.tick()
    # print('fps:', clock.get_fps())

pygame.quit()
