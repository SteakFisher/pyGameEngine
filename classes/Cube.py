import math
from typing import List

from utils.types import Position, Rotation
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

        new = []

        for vertex in self.vertices:
            vertex = np.matmul(zRotationMatrix, vertex)
            vertex = np.matmul(yRotationMatrix, vertex)
            vertex = np.matmul(xRotationMatrix, vertex)

            new.append(vertex)

        self.vertices = np.array(new)