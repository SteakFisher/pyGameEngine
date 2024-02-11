import numpy
import pygame
from pygame import Color

from newClasses.Object import Object
from utils.types import Rotation, Position, Scaling


class Cube(Object):
    def __init__(self, env: list[Object], screen: pygame.Surface, pos: Position = Position(), rot: Rotation = Rotation(),
                 scale: Scaling = Scaling()):
        super().__init__(env, pos, rot, scale)
        self.screen = screen

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
        print(transformedVertices)

        projectedVertices = []

        for vertex in transformedVertices:
            orthographicProjectionMatrix = numpy.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1]
            ])

            perspectiveProjectionMatrix = numpy.array([
                [3, 0, 0, 0],
                [0, 3, 0, 0],
                [0, 0, 11, -24],
                [0, 0, 1, 0]
            ])

            finalPoint = numpy.dot(orthographicProjectionMatrix, numpy.dot(perspectiveProjectionMatrix, vertex))
            finalPoint = finalPoint / finalPoint[3]
            projectedVertices.append(finalPoint)

            pygame.draw.circle(screen, Color(255, 255, 255), ((screen.get_width() / 2) + (finalPoint[0] * 50), (screen.get_height() / 2) + (finalPoint[1] * 50)), 5)

        print("Projected matrix: \n", numpy.array(projectedVertices))

    def tick(self):
        self.draw()
        super().tick()
