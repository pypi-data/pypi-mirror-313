from typing import Union, List, Optional

import numpy as np

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.polyline.components.PolylineProperties import PolylineProperties

from geogeometry.geometry.polyline.components.PolylineMetrics import PolylineMetrics
from geogeometry.geometry.polyline.components.PolylineQuerier import PolylineQuerier



class Polyline(BaseGeometry, PolylineProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.metrics: PolylineMetrics = PolylineMetrics(self)
        self.querier: PolylineQuerier = PolylineQuerier(self)

    def translate(self, translation_vector: Union[List, np.ndarray]) -> None: ...

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        super().setNodes(nodes=nodes)
        self.metrics.calculateMetrics()

    def calculate2DArea(self) -> None:
        self.metrics.calculate2DArea()

    def calculateLimits(self) -> None:
        self.metrics.calculateLimits()

    def calculateCentroid(self) -> None: ...

    def getPointAtDistanceFromOrigin(self, distance: float) -> Optional[np.ndarray]:
        return self.querier.getPointAtDistanceFromOrigin(distance=distance)