from typing import List

import numpy as np

from classes import Cube


def orthographic_projection (env: List[Cube]) -> List[Cube]:
    projectionMatrix = np.array([
        [1,0,0],
        [0,1,0]
    ])
    cubes = []

    for cube in env:
        projected = []
        for vertex in cube.vertices:
            projected.append(np.matmul(projectionMatrix, vertex))
        cubes.append(projected)

    return cubes