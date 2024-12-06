from typing import Union, List, Optional

import numpy as np

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.model.components.GeometryModelProperties import GeometryModelProperties


class GeometryModel(BaseGeometry, GeometryModelProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

    def __len__(self) -> int:
        total = 0
        total += len(self.getTriangulations())
        total += len(self.getPolylines())
        return total

    def translate(self, translation_vector: Union[List, np.ndarray]) -> None: ...
    def calculateLimits(self) -> None: ...
    def calculateCentroid(self) -> None: ...
