import math
from typing import TYPE_CHECKING, Union, List, Literal

import numpy as np

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


point_type = Union[List, np.ndarray]


class Angles(object):

    @staticmethod
    def calculateAngleBetweenVectorAndAxis(v: 'Vector', axis_id: Literal['x', 'y', 'z']) -> float:
        axes_vectors = {
            'x': [1, 0, 0],
            'y': [0, 1, 0],
            'z': [0, 0, 1]
        }
        return Angles.calculateAngleFromThreePoints(axes_vectors[axis_id], [0., 0., 0.], v.getN1())

    @staticmethod
    def calculateAngleBetweenOriginVectors(v1: 'Vector', v2: 'Vector') -> float:
        return Angles.calculateAngleFromThreePoints(v1.getN1(), [0., 0., 0.], v2.getN1())

    @staticmethod
    def calculateAngleFromThreePoints(n0: point_type, n1: point_type, n2: point_type) -> float:
        """
        Returns the angle of 2 3D segments sharing n1 node.
        Note: arccos domain: [-1,1]
        :returns angle in degrees
        """
        n0, n1, n2 = np.array([n0, n1, n2])
        v0 = n2 - n1
        v1 = n0 - n1

        if np.linalg.norm(v0) == 0. or np.linalg.norm(v1) == 0.:
            raise ValueError("Repeated points in angle calculation.")

        a = np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1))

        if a < -1.:
            a = -1.
        elif a > 1:
            a = 1

        arc = np.arccos(a)
        ang = math.degrees(arc)
        if np.isnan(ang):
            ang = 180.

        return ang

