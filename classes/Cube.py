from utils.types import Position, Rotation
import numpy as np

class Cube:
    def __init__(self, pos: Position = dict(x=5, y=0, z=0), rot: Rotation = dict(x=1, y=0, z=0), size: float = 1) -> None:
        self.pos = pos
        self.rot = rot

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