import numpy
import pygame
from pygame import Color

from newClasses.Object import Object
from utils.types import Rotation, Position, Scaling


class Cube(Object):
    def __init__(self, env: list[Object], screen: pygame.Surface, camera, pos: Position = Position(),
                 rot: Rotation = Rotation(),
                 scale: Scaling = Scaling()):
        super().__init__(env, pos, rot, scale)
        self.screen = screen
        self.camera = camera
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
        self.faces = [
            [0, 3, 1, 5],
            [0, 8, 2, 4],
            [1, 9, 2, 6],
            [3, 10, 4, 7],
            [5, 11, 6, 7],
            [8, 11, 9, 10]
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

    def drawEdges(self, pixels):
        for i in self.edges:
            if pixels[i[0]] is not None and pixels[i[1]] is not None:
                pygame.draw.line(self.screen, Color(255, 255, 255), pixels[i[0]], pixels[i[1]], 2)

    def __drawFace(self, pixels, face, color):
        surface = []
        for edge in face:
            if pixels[self.edges[edge][0]] is None or pixels[self.edges[edge][1]] is None:
                return

            surface.append(pixels[self.edges[edge][0]])
            surface.append(pixels[self.edges[edge][1]])

        pygame.draw.polygon(self.screen, color, tuple(surface))

    def drawFaces(self, pixels, transformedVertices):
        # pygame.draw.polygon(self.screen, Color(0,255,0), ((15, 65), (86, 125), (250, 375), (400, 25), (60, 540)))

        Colors = [Color(0, 0, 0), Color(0, 0, 255), Color(0, 255, 0), Color(0, 255, 255), Color(255, 0, 0),
                  Color(255, 0, 255), Color(255, 255, 0), Color(255, 255, 255)]

        faces = self.faces

        indices = []

        for i, face in enumerate(faces):
            sumVertices = 0
            for edge in face:
                for index, vertex in enumerate(self.edges[edge]):
                    sumVertices += transformedVertices[vertex][2]
            indices.append((face, sumVertices / 4, i))

        indices = sorted(indices, key=lambda x: x[1], reverse=True)

        i = 0

        for index in indices:
            self.__drawFace(pixels, index[0], Colors[index[2]])

    def render(self):
        screen = self.screen

        vertices: numpy.ndarray = self.__getUnitCube()

        transformedVertices: numpy.ndarray = self.__transformVertices(vertices)

        fov = 110  # Field of view in degrees
        aspect_ratio = screen.get_width() / screen.get_height()  # Aspect ratio of the screen
        near = 0.1  # Distance to the near clipping plane
        far = 100.0  # Distance to the far clipping plane

        # f = 1 / numpy.tan(fov / 2 / 180 * numpy.pi)  # Calculate projection factor
        # projection_matrix = numpy.array([
        #     [-f / aspect_ratio, 0, 0, 0],
        #     [0, -f, 0, 0],
        #     [0, 0, (far + near) / (far - near), 1],
        #     [0, 0, -2 * far * near / (far - near), 0]
        # ])

        self.camera.draw(self, transformedVertices)

    def tick(self):
        self.render()
        super().tick()
