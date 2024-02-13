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

    def draw(self):
        screen = self.screen

        vertices: numpy.ndarray = self.__getUnitCube()

        transformedVertices: numpy.ndarray = self.__transformVertices(vertices)

        orthographicProjectionMatrix = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])

        pixels = []

        for vertex in transformedVertices:
            vertex = numpy.dot(orthographicProjectionMatrix, vertex) / vertex[2]

            pixel = (int(screen.get_width() / 2 + vertex[0] * 100), int(screen.get_height() / 2 + vertex[1] * 100))
            pixels.append(pixel)

            pygame.draw.circle(screen, Color(255, 255, 255), pixel, 5)

        for i in self.edges:
            pygame.draw.line(screen, Color(255, 255, 255), pixels[i[0]], pixels[i[1]], 2)

    def tick(self):
        self.draw()
        super().tick()
