import numpy as np
import pygame
from pygame import Color

from newClasses.Cube import Cube
from newClasses.Object import Object
from utils.types import Rotation, Position


class Camera(Object):
    def __init__(self, env: list[Object], pos: Position = Position(), rot: Rotation = Rotation()):
        super().__init__(env, pos, rot)

    def draw(self, cube: Cube, transformedVertices):
        fov = 110  # Field of view in degrees
        aspect_ratio = cube.screen.get_width() / cube.screen.get_height()  # Aspect ratio of the screen
        near = 0.1  # Distance to the near clipping plane
        far = 100.0  # Distance to the far clipping plane

        f = 1 / np.tan(fov / 2 / 180 * np.pi)  # Calculate projection factor
        projection_matrix = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (far - near), 1],
            [0, 0, -2 * far * near / (far - near), 0]
        ])

        pixels = []

        # transformedVertices = sorted(transformedVertices, key=lambda x: x[2])

        cameraMatrix = np.matmul(self.getRotationMatrix(), self.getTranslationMatrix())
        cameraInverseMatrix = np.linalg.inv(cameraMatrix)

        inversed = []

        for vertex in transformedVertices:
            inversed.append(np.matmul(cameraInverseMatrix, vertex))

        transformedVertices = np.array(inversed)

        for vertex in transformedVertices:
            if vertex[2] < 0:
                pixels.append(None)
                continue

            vertex = np.dot(projection_matrix, vertex)

            vertex /= vertex[3]

            screen_x = vertex[0] * cube.screen.get_width() / 2 + cube.screen.get_width() / 2
            screen_y = vertex[1] * cube.screen.get_height() / 2 + cube.screen.get_height() / 2

            pixel = (screen_x, screen_y)
            pixels.append(pixel)

            pygame.draw.circle(cube.screen, Color(255, 255, 255), pixel, 5)

        cube.drawEdges(pixels)
        cube.drawFaces(pixels, transformedVertices)
