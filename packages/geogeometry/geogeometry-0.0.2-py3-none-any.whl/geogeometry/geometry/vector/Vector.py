import math
from typing import Optional, Tuple, Any, Callable, List

import numpy as np

from geogeometry.geometry.vector.components.VectorMetrics import VectorMetrics
from geogeometry.geometry.vector.components.VectorProperties import VectorProperties
from geogeometry.geometry.vector.components.VectorTransformer import VectorTransformer


def nodesToVector(func: Callable[..., List[np.ndarray]]) -> Callable[..., 'Vector']:
    def inner(vector: 'Vector', *args, **kwargs) -> 'Vector':
        nodes = func(vector, *args, **kwargs)
        return Vector(n0=nodes[0], n1=nodes[1])

    return inner


class Vector(VectorProperties):

    def __init__(self, n0: np.ndarray, n1: Optional[np.ndarray] = None):
        super().__init__()

        if n1 is None:
            self.setN0(n0=np.zeros(n0.shape[0]))
            self.setN1(n1=n0)
        else:
            self.setN0(n0=n0)
            self.setN1(n1=n1)

        self.metrics: VectorMetrics = VectorMetrics(self)
        self.transformer: VectorTransformer = VectorTransformer(self)

        self.metrics.calculateMetrics()

    def createNormalizedVector(self, n: np.ndarray) -> None:
        self.setNormalizedVector(normalized_vector=Vector(n0=n))

    @nodesToVector
    def reverse(self) -> List[np.ndarray]:
        return self.transformer.reverse()

    @nodesToVector
    def rotate2d(self, angle: float) -> List[np.ndarray]:
        return self.transformer.rotate2d(angle=angle)
