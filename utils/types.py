from typing import TypedDict, Optional


class Position(TypedDict):
    x: float
    y: float
    z: float
    w: Optional[float]


class Rotation(TypedDict):
    x: float
    y: float
    z: float


class ScalingFactor(TypedDict):
    x: float
    y: float
    z: float

