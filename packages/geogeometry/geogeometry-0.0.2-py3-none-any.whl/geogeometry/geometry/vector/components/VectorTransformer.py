import math
from typing import TYPE_CHECKING, List

import numpy as np

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorTransformer(object):

    def __init__(self, vector: 'Vector'):
        self.vector: 'Vector' = vector

    def reverse(self) -> List[np.ndarray]:
        n0 = -1 * self.vector.getN0()
        n1 = -1 * self.vector.getN1()
        return [n0, n1]

    def rotate2d(self, angle: float) -> List[np.ndarray]:
        """
        ANTI-CLOCKWISE. Rotation axis at the origin (0,0).
        :param angle: In degrees.
        """
        angle = math.radians(angle)
        rot_matrix = np.array([
                                [math.cos(angle), -math.sin(angle)],
                                [math.sin(angle), math.cos(angle)],
                            ])

        n0 = rot_matrix.dot(self.vector.getN0())
        n1 = rot_matrix.dot(self.vector.getN1())

        return [n0, n1]
