from typing import List

import pygame
from pygame import Color

from utils.types import Position, Rotation, ScalingFactor
from utils.config import getConfig
import numpy as np


class Cube:
    def __init__(self, env: List, pos: Position = dict(x=0, y=0, z=0), size: float = 1) -> None:
        env.append(self)

        self.pos = pos

        self.size = size

        self.vertices = np.array([
            [self.pos['x'] + size, self.pos['y'] + size, self.pos['z'] + size],
            [self.pos['x'] + size, self.pos['y'] - size, self.pos['z'] + size],
            [self.pos['x'] - size, self.pos['y'] + size, self.pos['z'] + size],
            [self.pos['x'] - size, self.pos['y'] - size, self.pos['z'] + size],
            [self.pos['x'] + size, self.pos['y'] + size, self.pos['z'] - size],
            [self.pos['x'] + size, self.pos['y'] - size, self.pos['z'] - size],
            [self.pos['x'] - size, self.pos['y'] + size, self.pos['z'] - size],
            [self.pos['x'] - size, self.pos['y'] - size, self.pos['z'] - size]
        ])

    def __str__(self) -> str:
        return f"{self.vertices}"

    def rotate(self, angle: Rotation) -> None:
        xRotationMatrix = np.array([
            [1, 0, 0],
            [0, np.cos(np.deg2rad(angle['x'])), -np.sin(np.deg2rad(angle['x']))],
            [0, np.sin(np.deg2rad(angle['x'])), np.cos(np.deg2rad(angle['x']))]
        ])

        yRotationMatrix = np.array([
            [np.cos(np.deg2rad(angle['y'])), 0, np.sin(np.deg2rad(angle['y']))],
            [0, 1, 0],
            [-np.sin(np.deg2rad(angle['y'])), 0, np.cos(np.deg2rad(angle['y']))]
        ])

        zRotationMatrix = np.array([
            [np.cos(np.deg2rad(angle['z'])), -np.sin(np.deg2rad(angle['z'])), 0],
            [np.sin(np.deg2rad(angle['z'])), np.cos(np.deg2rad(angle['z'])), 0],
            [0, 0, 1]
        ])

        rotated = []

        for vertex in self.vertices:
            vertex = np.matmul(zRotationMatrix, vertex)
            vertex = np.matmul(yRotationMatrix, vertex)
            vertex = np.matmul(xRotationMatrix, vertex)

            rotated.append(vertex)

        self.vertices = np.array(rotated)

    def scale(self, factor: ScalingFactor):
        scalingMatrix = np.array([
            [factor['x'], 0, 0],
            [0, factor['y'], 0],
            [0, 0, factor['z']]
        ])

        scaled = []

        for vertex in self.vertices:
            scaledVertex = np.matmul(scalingMatrix, vertex)

            scaled.append(scaledVertex)

        self.vertices = np.array(scaled)

    def orthographic_project(self):
        projectionMatrix = np.array([
            [1, 0, 0],
            [0, 1, 0]
        ])

        projected = []
        for vertex in self.vertices:
            projected.append(np.matmul(projectionMatrix, vertex))

        return projected

    def draw(self, screen):
        projected = self.orthographic_project()

        screen.get_width()
        screen.get_height()

        for vertex in projected:
            pygame.draw.circle(screen, Color(255, 255, 255),
                               (
                                        (screen.get_width() / 2 + (vertex[0] * getConfig()['scale'])),
                                        (screen.get_height() / 2 + (vertex[1] * getConfig()['scale']))
                                       ), 5)

