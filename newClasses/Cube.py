import numpy
import pygame
from pygame import Color

from newClasses.Object import Object
from utils.types import Rotation, Position, Scaling


class Cube(Object):
    def __init__(self, env: list[Object], screen: pygame.Surface, pos: Position = Position(),
                 rot: Rotation = Rotation(),
                 scale: Scaling = Scaling()):
        super().__init__(env, pos, rot, scale)
        self.screen = screen
        self.edges = [
            [0, 1],
            [0, 2],
            [0, 4],

            [1, 3],
            [1, 5],

            [2, 3],
            [2, 6],

            [3, 7],

            [4, 5],
            [4, 6],

            [5, 7],

            [6, 7]
        ]

    @staticmethod
    def __getUnitCube():
        return numpy.array([
            [+ 1, + 1, + 1, 1],
            [+ 1, - 1, + 1, 1],
            [- 1, + 1, + 1, 1],
            [- 1, - 1, + 1, 1],
            [+ 1, + 1, - 1, 1],
            [+ 1, - 1, - 1, 1],
            [- 1, + 1, - 1, 1],
            [- 1, - 1, - 1, 1]
        ])

    def __transformVertices(self, vertices: numpy.ndarray) -> numpy.ndarray:
        transformedVertices = []
        for vertex in vertices:
            vertex = numpy.dot(super().getRotationMatrix(), vertex)
            vertex = numpy.dot(super().getScalingMatrix(), vertex)
            vertex = numpy.dot(super().getTranslationMatrix(), vertex)

            transformedVertices.append(vertex)
        return numpy.array(transformedVertices)

    def __drawEdges(self, pixels):
        for i in self.edges:
            pygame.draw.line(self.screen, Color(255, 255, 255), pixels[i[0]], pixels[i[1]], 2)

    def draw(self):
        screen = self.screen

        vertices: numpy.ndarray = self.__getUnitCube()

        transformedVertices: numpy.ndarray = self.__transformVertices(vertices)

        fov = 110  # Field of view in degrees
        aspect_ratio = screen.get_width() / screen.get_height()  # Aspect ratio of the screen
        near = 0.1  # Distance to the near clipping plane
        far = 100.0  # Distance to the far clipping plane

        f = 1 / numpy.tan(fov / 2 / 180 * numpy.pi)  # Calculate projection factor
        # projection_matrix = numpy.array([
        #     [-f / aspect_ratio, 0, 0, 0],
        #     [0, -f, 0, 0],
        #     [0, 0, (far + near) / (far - near), 1],
        #     [0, 0, -2 * far * near / (far - near), 0]
        # ])

        f = 1 / numpy.tan(fov / 2 / 180 * numpy.pi)  # Calculate projection factor
        projection_matrix = numpy.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (far - near), 1],
            [0, 0, -2 * far * near / (far - near), 0]
        ])

        pixels = []

        for vertex in transformedVertices:
            vertex = numpy.dot(projection_matrix, vertex)

            print(vertex / vertex[3])

            vertex /= vertex[3]

            screen_x = vertex[0] * screen.get_width() / 2 + screen.get_width() / 2
            screen_y = vertex[1] * screen.get_height() / 2 + screen.get_height() / 2

            pixel = (screen_x, screen_y)
            pixels.append(pixel)

            pygame.draw.circle(screen, Color(255, 255, 255), pixel, 5)

        self.__drawEdges(pixels)



    def tick(self):
        self.draw()
        super().tick()
