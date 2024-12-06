from typing import Optional, Literal, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline


class PolylineMetrics(object):

    def __init__(self, polyline: 'Polyline'):
        self.polyline: 'Polyline' = polyline

    def calculateMetrics(self) -> None:
        nodes = self.polyline.getNodes()

        self.polyline.setDimensions(dimensions=nodes.shape[1])

        closed = False
        if not np.linalg.norm(nodes[0] - nodes[-1]):
            closed = True
        self.polyline.setClosed(closed=closed)

        self.calculateLimits()
        self.calculateLength()
        self.calculateMidPoint()

        if self.polyline.getDimensions() == 2 and self.polyline.isClosed():
            self.calculate2DArea()

    def calculateLength(self):
        nodes = self.polyline.getNodes()
        ds = [np.linalg.norm(n - nodes[i + 1]) for i, n in enumerate(nodes[:-1])]
        self.polyline.setLength(length=np.sum(ds))

    def calculateLimits(self) -> None:
        mins = np.min(self.polyline.getNodes(), axis=0)
        maxs = np.max(self.polyline.getNodes(), axis=0)

        self.polyline.setLimits(np.array([mins, maxs]))

    def calculate2DArea(self) -> None:
        """
        Considers XY space, even if nodes dimensions is greater than 2.
        Gets area even if the polyline is open.
        """
        nodes = self.polyline.getNodes()
        if self.polyline.isClosed():
            x, y = nodes[:-1][:, 0], nodes[:-1][:, 1]
        else:
            x, y = nodes[:, 0], nodes[:, 1]

        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        self.polyline.setArea(area=area)

    def calculateMidPoint(self) -> None:
        """
        Mid at (total length) / 2
        """
        mid_point = self.polyline.getPointAtDistanceFromOrigin(distance=self.polyline.getLength() / 2.)
        self.polyline.setMidPoint(mid_point)