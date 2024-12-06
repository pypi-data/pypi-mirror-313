import copy
from typing import TYPE_CHECKING, Tuple

import numpy as np

from geogeometry.geometry.operations.Angles import Angles

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorMetrics(object):

    def __init__(self, vector: 'Vector'):
        self.vector: 'Vector' = vector

    def calculateMetrics(self) -> None:
        self.calculateLength()
        self.calculateNormalizedVector()
        self.calculateDipDipdir()

    def calculateLength(self) -> None:
        diff = self.vector.getN1() - self.vector.getN0()
        length = np.linalg.norm(diff)
        self.vector.setLength(length=length)

        self.vector.setUnitary(unitary=length == 1.)

    def calculateNormalizedVector(self) -> None:

        if self.vector.isUnitary():
            self.vector.setNormalizedVector(normalized_vector=copy.deepcopy(self.vector))
            return

        vector = np.array(self.vector.getN1() - self.vector.getN0())
        norm = np.linalg.norm(vector)

        if norm == 0.:
            raise ValueError("Origin as vector.")

        self.vector.createNormalizedVector(n=vector/norm)

    def calculateDipDipdir(self) -> None:

        if self.vector.getNormalizedVector() is None:
            self.calculateNormalizedVector()

        norm_vector = self.vector.getNormalizedVector()

        dipdir = None
        if norm_vector.getN0().shape[0] == 2:
            dip = 90.
        else:
            if abs(norm_vector.getN1()[2]) == 1.:
                dip, dipdir = 0, 0
            else:
                dip = Angles.calculateAngleBetweenVectorAndAxis(v=norm_vector, axis_id='z')
                if dip > 90.:
                    dip = Angles.calculateAngleBetweenVectorAndAxis(v=norm_vector.reverse(), axis_id='z')

        if dipdir is None:
            dipdir = Angles.calculateAngleFromThreePoints([0., 1.], [0., 0.], norm_vector.getN1()[:2])

        if norm_vector.getN1()[0] < 0.:
            dipdir = 360. - dipdir

        self.vector.setDip(dip=round(dip, 2))
        self.vector.setDipdir(dipdir=round(dipdir, 2))
