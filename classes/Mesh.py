import numpy as np
import pygame
from pygame import Color

from classes.Camera import Camera
from utils.types import Rotation, Position, Scaling


class Mesh:
    def __init__(self, modelPath, pos=Position(), rot=Rotation(), scale=Scaling()):
        self.__vertices = []
        self.__faces = []

        Colors = [Color(125, 125, 125), Color(0, 0, 255), Color(0, 255, 0), Color(0, 255, 255), Color(255, 0, 0),
                  Color(255, 0, 255), Color(255, 255, 0), Color(255, 255, 255)]

        # Open the model file and read the vertices and faces and assign it to the object
        for line in open(modelPath, 'r'):
            if line.startswith('v '):
                self.__vertices.append(list(map(float, line.strip().split()[1:4] + [1.0])))
            elif line.startswith('f '):
                face = []
                vertices = line.strip().split()[1:5]

                for vertex in vertices:
                    face.append(int(vertex.split('/')[0]))

                self.__faces.append({
                    'face': face,
                    'color': Colors[len(self.__faces) % len(Colors)]
                })

        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.__vertices = np.array(self.__vertices)
        self.__faces = self.__faces

    def draw(self, camera: Camera):
        vertices = self.__scale(self.__vertices)
        vertices = self.__rotate(vertices)
        vertices = self.__translate(vertices)

        cameraTransformMatrix = camera.getInverseTransformationMatrix()
        vertices = np.array([np.dot(cameraTransformMatrix, vertex) for vertex in vertices])

        vertices = self.__project(vertices, camera)

        faces = self.__faces

        # Sort faces depending on the average z value of their vertices
        faces = sorted(faces, key=self.__sortFaces(vertices), reverse=True)

        for index, face in enumerate(faces):
            screen = pygame.display.get_surface()
            color = face['color']
            breakFlag = False
            surface = []
            for vertexIndex in face['face']:
                vertex = vertices[vertexIndex - 1]

                if vertex[3] == 0:
                    breakFlag = True
                    break

                screen_x = vertex[0] * screen.get_width() / 2 + screen.get_width() / 2
                screen_y = vertex[1] * screen.get_height() / 2 + screen.get_height() / 2

                surface.append((screen_x, screen_y))
            if breakFlag:
                continue

            pygame.draw.polygon(screen, color, surface)

    def __translate(self, vertices):
        translationMatrix = np.array([
            [1, 0, 0, self.pos.x],
            [0, 1, 0, self.pos.y],
            [0, 0, 1, self.pos.z],
            [0, 0, 0, 1]
        ])

        return np.array([np.dot(translationMatrix, vertex) for vertex in vertices])

    def __rotate(self, vertices):
        rotationMatrixX = np.array([
            [1, 0, 0, 0],
            [0, np.cos(np.deg2rad(self.rot.x)), -np.sin(np.deg2rad(self.rot.x)), 0],
            [0, np.sin(np.deg2rad(self.rot.x)), np.cos(np.deg2rad(self.rot.x)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixY = np.array([
            [np.cos(np.deg2rad(self.rot.y)), 0, np.sin(np.deg2rad(self.rot.y)), 0],
            [0, 1, 0, 0],
            [-np.sin(np.deg2rad(self.rot.y)), 0, np.cos(np.deg2rad(self.rot.y)), 0],
            [0, 0, 0, 1]
        ])

        rotationMatrixZ = np.array([
            [np.cos(np.deg2rad(self.rot.z)), -np.sin(np.deg2rad(self.rot.z)), 0, 0],
            [np.sin(np.deg2rad(self.rot.z)), np.cos(np.deg2rad(self.rot.z)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return np.array([np.dot(np.dot(rotationMatrixX, np.dot(rotationMatrixY, rotationMatrixZ)), vertex) for vertex in vertices])

    def __scale(self, vertices):
        scalingMatrix = np.array([
            [self.scale.x, 0, 0, 0],
            [0, self.scale.y, 0, 0],
            [0, 0, self.scale.z, 0],
            [0, 0, 0, 1]
        ])

        return np.array([np.dot(scalingMatrix, vertex) for vertex in vertices])

    @staticmethod
    def __project(transformedVertices, camera):
        screen = pygame.display.get_surface()

        fov = 110
        aspect_ratio = screen.get_width() / screen.get_height()
        near = 0.1
        far = 100.0
        f = 1 / np.tan(fov / 2 / 180 * np.pi)

        projection_matrix = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (far - near), 1],
            [0, 0, -2 * far * near / (far - near), 0]
        ])

        vertices = []

        for vertex in transformedVertices:
            if vertex[2] < 0:
                vertices.append([0, 0, 0, 0])
                continue

            vertex = np.dot(projection_matrix, vertex)
            vertex /= vertex[3]

            vertices.append(vertex)

        return np.array(vertices)

    @staticmethod
    def __sortFaces(transformedVertices):
        def keyFunc(face):
            return sum([transformedVertices[vertex - 1][2] / len(face['face']) for vertex in face['face']])
        return keyFunc

    def __str__(self):
        return f'{self.__vertices}\n{self.__faces}'
