from typing import TypedDict, Optional


class Position:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other: 'Position'):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Rotation:
    def __init__(self, x: float = 0, y: float = 0, z: float = 180):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other: 'Rotation'):
        return Rotation(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Scaling:
    def __init__(self, x: float = 1, y: float = 1, z: float = 1):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other: 'Scaling'):
        return Scaling(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"