from typing import List

import pygame
from pygame import Color

from utils.constants import getRotationMatrix, getScalingMatrix, getTranslationMatrix
from utils.types import Position, Rotation, ScalingFactor
from utils.config import getConfig
import numpy as np


class Cube:
    def __init__(self, env: List, pos: Position = dict(x=0, y=0, z=0), size: float = 1) -> None:
        env.append(self)
        pos['w'] = 1
        self.pos = pos

        self.size = size

        self.vertices = np.array([
            [self.pos['x'] + size, self.pos['y'] + size, self.pos['z'] + size, self.pos['w']],
            [self.pos['x'] + size, self.pos['y'] - size, self.pos['z'] + size, self.pos['w']],
            [self.pos['x'] - size, self.pos['y'] + size, self.pos['z'] + size, self.pos['w']],
            [self.pos['x'] - size, self.pos['y'] - size, self.pos['z'] + size, self.pos['w']],
            [self.pos['x'] + size, self.pos['y'] + size, self.pos['z'] - size, self.pos['w']],
            [self.pos['x'] + size, self.pos['y'] - size, self.pos['z'] - size, self.pos['w']],
            [self.pos['x'] - size, self.pos['y'] + size, self.pos['z'] - size, self.pos['w']],
            [self.pos['x'] - size, self.pos['y'] - size, self.pos['z'] - size, self.pos['w']]
        ])

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

    def __str__(self) -> str:
        return f"{self.vertices}"

    def rotate(self, angle: Rotation) -> None:
        prevPos = self.pos

        self.translate({"x": -prevPos['x'], "y": -prevPos['y'], "z": 0, "w": -prevPos['z']})

        print(self.pos)

        xRotationMatrix = np.array(getRotationMatrix(angle, 'x'))

        yRotationMatrix = np.array(getRotationMatrix(angle, 'y'))

        zRotationMatrix = np.array(getRotationMatrix(angle, 'z'))

        rotated = []

        for vertex in self.vertices:
            vertex = np.matmul(zRotationMatrix, vertex)
            vertex = np.matmul(yRotationMatrix, vertex)
            vertex = np.matmul(xRotationMatrix, vertex)

            rotated.append(vertex)

        self.vertices = np.array(rotated)

        self.translate(prevPos)


    def scale(self, factor: ScalingFactor):
        scalingMatrix = np.array(getScalingMatrix(factor))

        scaled = []

        for vertex in self.vertices:
            scaledVertex = np.matmul(scalingMatrix, vertex)

            scaled.append(scaledVertex)

        self.vertices = np.array(scaled)

    def translate(self, translation: Position) -> None:
        translationMatrix = np.array(getTranslationMatrix(translation))

        translated = []

        for vertex in self.vertices:
            translatedVertex = np.matmul(translationMatrix, vertex)

            translated.append(translatedVertex)

        self.vertices = np.array(translated)

    def orthographic_project(self):
        projectionMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])

        projected = []
        for vertex in self.vertices:
            projected.append(np.matmul(projectionMatrix, vertex))

        return projected

    def draw(self, screen):
        projected = self.orthographic_project()

        screen.get_width()
        screen.get_height()

        points = []

        pygame.draw.circle(screen, Color(255, 255, 255),(screen.get_width()/2, screen.get_height()/2), 5)

        for vertex in projected:
            pygame.draw.circle(screen, Color(255, 255, 255),
                               (
                                   (screen.get_width() / 2 + (vertex[0] * getConfig()['scale'])),
                                   (screen.get_height() / 2 + (vertex[1] * getConfig()['scale']))
                               ), 5)
            points.append((
                (screen.get_width() / 2 + (vertex[0] * getConfig()['scale'])),
                (screen.get_height() / 2 + (vertex[1] * getConfig()['scale']))
            ))

        for i in self.edges:
            pygame.draw.line(screen, Color(255, 255, 255), points[i[0]], points[i[1]], 2)
