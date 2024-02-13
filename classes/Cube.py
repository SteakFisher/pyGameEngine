import math
from typing import List

import pygame
from pygame import Color

from classes.Camera import Camera
from utils.constants import getRotationMatrix, getScalingMatrix, getTranslationMatrix
from utils.types import Position, Rotation, ScalingFactor
from utils.config import getConfig
import numpy as np


class Cube:
    def __init__(self, env: List, pos: Position = dict(x=0, y=0, z=0, w=1), size: float = 1) -> None:
        env.append(self)

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

        self.translate({"x": 0, "y": 0, "z": 0, "w": 1})

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

        position = Position()

        position['x'] = translation['x'] - self.pos['x']
        position['y'] = translation['y'] - self.pos['y']
        position['z'] = translation['z'] - self.pos['z']

        if position['x'] == 0 and position['y'] == 0 and position['z'] == 0:
            return

        position['w'] = 1

        translationMatrix = np.array(getTranslationMatrix(position))

        translated = []

        for vertex in self.vertices:
            translatedVertex = np.matmul(translationMatrix, vertex)

            translated.append(translatedVertex)

        self.pos = translation
        self.vertices = np.array(translated)

    def orthographic_project(self, camera: Camera):

        projected = []
        z = self.pos['z'] - camera.pos['z']
        for vertex in self.vertices:
            projectionMatrix = np.array([
                [z, 0, 0, 0],
                [0, z, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1]
            ])

            # print(vertex)
            # vertex = np.divide(vertex, np.absolute(vertex[2]))
            projected.append(np.matmul(projectionMatrix, vertex))
            print(vertex)

        return projected

    def draw(self, screen, camera: Camera):
        oldPos = self.pos
        oldPoints = self.vertices

        cameraTranslationMatrix = getTranslationMatrix(camera.pos)
        cameraRotationMatrixX = getRotationMatrix(camera.rot, 'x')
        cameraRotationMatrixY = getRotationMatrix(camera.rot, 'y')
        cameraRotationMatrixZ = getRotationMatrix(camera.rot, 'z')

        cameraMatrix = np.matmul(np.array(cameraRotationMatrixZ), np.array(cameraTranslationMatrix))
        cameraMatrix = np.matmul(np.array(cameraRotationMatrixY), np.array(cameraMatrix))
        cameraMatrix = np.matmul(np.array(cameraRotationMatrixX), np.array(cameraMatrix))

        cameraInverse = np.linalg.inv(cameraMatrix)

        inversed = []

        for vertex in self.vertices:
            inversed.append(np.matmul(cameraInverse, vertex))

        self.vertices = np.array(inversed)

        projected = self.orthographic_project(camera)

        self.vertices = oldPoints
        self.pos = oldPos

        screen.get_width()
        screen.get_height()

        points = []

        pygame.draw.circle(screen, Color(255, 255, 255), (screen.get_width() / 2, screen.get_height() / 2), 5)

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
