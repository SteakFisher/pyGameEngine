import numpy

from utils.types import Position, Rotation


class Camera:
    def __init__(self, pos: Position = Position(), rot: Rotation = Rotation()):
        self.pos = pos
        self.rot = rot

    def getInverseTransformationMatrix(self):
        return numpy.linalg.inv(numpy.dot(self.__getRotationMatrix(), self.__getTranslationMatrix()))

    def __getTranslationMatrix(self):
        position = self.pos

        return numpy.array([
            [1, 0, 0, position.x],
            [0, 1, 0, position.y],
            [0, 0, 1, position.z],
            [0, 0, 0, 1]
        ])

    def __getRotationMatrix(self):
        rot = self.rot

        rotationMatrixX = numpy.array([
            [1, 0, 0, 0],
            [0, numpy.cos(numpy.deg2rad(rot.x)), -numpy.sin(numpy.deg2rad(rot.x)), 0],
            [0, numpy.sin(numpy.deg2rad(rot.x)), numpy.cos(numpy.deg2rad(rot.x)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixY = numpy.array([
            [numpy.cos(numpy.deg2rad(rot.y)), 0, numpy.sin(numpy.deg2rad(rot.y)), 0],
            [0, 1, 0, 0],
            [-numpy.sin(numpy.deg2rad(rot.y)), 0, numpy.cos(numpy.deg2rad(rot.y)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixZ = numpy.array([
            [numpy.cos(numpy.deg2rad(rot.z)), -numpy.sin(numpy.deg2rad(rot.z)), 0, 0],
            [numpy.sin(numpy.deg2rad(rot.z)), numpy.cos(numpy.deg2rad(rot.z)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return numpy.dot(rotationMatrixX, numpy.dot(rotationMatrixY, rotationMatrixZ))