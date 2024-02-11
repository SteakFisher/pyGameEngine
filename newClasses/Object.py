from typing import List, Self

import numpy

from utils.types import Position, Rotation, Scaling


class Object:
    def __init__(self: Self, env: List[Self], pos: Position = Position(), rot: Rotation = Rotation(), scale: Scaling() = Scaling()):
        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.tempPos = pos
        self.tempRot = rot
        self.tempScale = scale

        env.append(self)

    def getRotationMatrix(self) -> numpy.ndarray:
        angle = self.tempRot

        rotationMatrixX = numpy.array([
            [1, 0, 0, 0],
            [0, numpy.cos(numpy.deg2rad(angle.x)), -numpy.sin(numpy.deg2rad(angle.x)), 0],
            [0, numpy.sin(numpy.deg2rad(angle.x)), numpy.cos(numpy.deg2rad(angle.x)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixY = numpy.array([
            [numpy.cos(numpy.deg2rad(angle.y)), 0, numpy.sin(numpy.deg2rad(angle.y)), 0],
            [0, 1, 0, 0],
            [-numpy.sin(numpy.deg2rad(angle.y)), 0, numpy.cos(numpy.deg2rad(angle.y)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixZ = numpy.array([
            [numpy.cos(numpy.deg2rad(angle.z)), -numpy.sin(numpy.deg2rad(angle.z)), 0, 0],
            [numpy.sin(numpy.deg2rad(angle.z)), numpy.cos(numpy.deg2rad(angle.z)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return numpy.dot(rotationMatrixX, numpy.dot(rotationMatrixY, rotationMatrixZ))

    def getScalingMatrix(self) -> numpy.ndarray:
        factor = self.tempScale

        return numpy.array([
            [factor.x, 0, 0, 0],
            [0, factor.y, 0, 0],
            [0, 0, factor.z, 0],
            [0, 0, 0, 1]
        ])

    def getTranslationMatrix(self) -> numpy.ndarray:
        position = self.tempPos

        return numpy.array([
            [1, 0, 0, position.x],
            [0, 1, 0, position.y],
            [0, 0, 1, position.z],
            [0, 0, 0, 1]
        ])

    def setRotation(self, rot: Rotation):
        self.tempRot = rot

    def setScale(self, scale: Scaling):
        self.tempScale = scale

    def setPosition(self, pos: Position):
        self.tempPos = pos

    def tick(self):
        self.pos = self.tempPos
        self.rot = self.tempRot
        self.scale = self.tempScale
