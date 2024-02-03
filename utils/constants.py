import numpy as np

from utils.types import Rotation, ScalingFactor, Position


def getRotationMatrix(angle: Rotation, a):
    if a == 'x':
        return [
            [1, 0, 0, 0],
            [0, np.cos(np.deg2rad(angle['x'])), -np.sin(np.deg2rad(angle['x'])), 0],
            [0, np.sin(np.deg2rad(angle['x'])), np.cos(np.deg2rad(angle['x'])), 0],
            [0, 0, 0, 1]
        ]

    elif a == 'y':
        return [
            [np.cos(np.deg2rad(angle['y'])), 0, np.sin(np.deg2rad(angle['y'])), 0],
            [0, 1, 0, 0],
            [-np.sin(np.deg2rad(angle['y'])), 0, np.cos(np.deg2rad(angle['y'])), 0],
            [0, 0, 0, 1]
        ]

    elif a == 'z':
        return [
            [np.cos(np.deg2rad(angle['z'])), -np.sin(np.deg2rad(angle['z'])), 0, 0],
            [np.sin(np.deg2rad(angle['z'])), np.cos(np.deg2rad(angle['z'])), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]


def getScalingMatrix(factor: ScalingFactor):
    return [
        [factor['x'], 0, 0, 0],
        [0, factor['y'], 0, 0],
        [0, 0, factor['z'], 0],
        [0, 0, 0, 1]
    ]


def getTranslationMatrix(pos: Position):
    return [
        [1, 0, 0, pos['x']],
        [0, 1, 0, pos['y']],
        [0, 0, 1, pos['z']],
        [0, 0, 0, 1]
    ]
