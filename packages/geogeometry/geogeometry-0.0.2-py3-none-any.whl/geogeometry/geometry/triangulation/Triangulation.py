from typing import Union, List, Optional

import numpy as np

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.triangulation.components.TriangulationProperties import TriangulationProperties


class Triangulation(BaseGeometry, TriangulationProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

    def translate(self, translation_vector: Union[List, np.ndarray]) -> None: ...
    def calculateLimits(self) -> None: ...
    def calculateCentroid(self) -> None: ...
