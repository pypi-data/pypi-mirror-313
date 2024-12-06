from typing import Optional

import numpy as np


class BaseGeometryProperties(object):

    def __init__(self, name: Optional[str] = None):
        super().__init__()

        self.name: Optional[str] = name
        self.color: str = 'red'
        self.opacity: float = 1.0

        self.id: int = id(self)

        self.limits: Optional[np.ndarray] = None
        self.centroid: Optional[np.ndarray] = None

    def setName(self, name: str) -> None:
        self.name = name

    def setColor(self, color: str) -> None:
        self.color = color

    def setOpacity(self, opacity: float) -> None:
        self.opacity = opacity

    def setLimits(self, limits: np.ndarray) -> None:
        self.limits = limits

    def setCentroid(self, centroid: np.ndarray) -> None:
        self.centroid = centroid

    def getName(self) -> str:
        return self.name

    def getColor(self) -> str:
        return self.color

    def getOpacity(self) -> float:
        return self.opacity

    def getLimits(self) -> Optional[np.ndarray]:
        return self.limits

    def getCentroid(self) -> Optional[np.ndarray]:
        return self.centroid
