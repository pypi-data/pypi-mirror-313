from typing import Optional, TYPE_CHECKING, Literal

import numpy as np

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorProperties(object):

    def __init__(self):

        self.n0: Optional[np.ndarray] = None
        self.n1: Optional[np.ndarray] = None

        self.dimensions: Optional[int] = None

        self.length: Optional[float] = None
        self.unitary: Optional[bool] = None

        self.normalized_vector: Optional['Vector'] = None

        self.dip: Optional[float] = None
        self.dipdir: Optional[float] = None

    def setN0(self, n0: np.ndarray) -> None:
        self.n0 = n0

    def setN1(self, n1: np.ndarray) -> None:
        self.n1 = n1

    def setDimensions(self, dimensions: Literal[2, 3]) -> None:
        self.dimensions = dimensions

    def setLength(self, length: float) -> None:
        self.length = length

    def setUnitary(self, unitary: bool) -> None:
        self.unitary = unitary

    def setNormalizedVector(self, normalized_vector: 'Vector') -> None:
        self.normalized_vector = normalized_vector

    def setDip(self, dip: float) -> None:
        self.dip = dip

    def setDipdir(self, dipdir: float) -> None:
        self.dipdir = dipdir

    def getN0(self) -> np.ndarray:
        return self.n0

    def getN1(self) -> np.ndarray:
        return self.n1

    def getNodes(self) -> np.ndarray:
        return np.array([self.n0, self.n1])

    def getLength(self) -> float:
        return self.length

    def isUnitary(self) -> bool:
        return self.unitary

    def getNormalizedVector(self) -> 'Vector':
        return self.normalized_vector

    def getDip(self) -> float:
        return self.dip

    def getDipdir(self) -> float:
        return self.dipdir
