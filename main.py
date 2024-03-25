import pygame
from pygame import Color

from classes.Camera import Camera
from classes.Mesh import Mesh
from utils.types import Position, Scaling

pygame.init()

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

mesh = Mesh('monkey.obj', scale=Scaling(0.5, 0.5, 0.5))
camera: Camera = Camera(pos=Position(0, 0, -4))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    mesh.rot.y = mesh.rot.y + 1
    # mesh.pos.z += 1
    # camera.pos.z -= 1
    # mesh.pos.x = mesh.pos.x + 0.01

    mesh.draw(camera)
    # pygame.draw.circle(screen, Color(255, 255, 255), (screen.get_width() / 2, screen.get_height() / 2), 5)

    pygame.display.flip()

    clock.tick(60)
    # clock.tick()
    # print('fps:', clock.get_fps())

pygame.quit()
