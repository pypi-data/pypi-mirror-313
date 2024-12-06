from typing import TYPE_CHECKING, Union, List, Optional

import numpy as np
import shapely.geometry as shageo

from geogeometry.geometry.vector.Vector import Vector

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline


class PolylineQuerier(object):

    def __init__(self, polyline: 'Polyline'):
        self.polyline = polyline

    def arePointsInside(self, test_nodes: Union[List, np.ndarray]) -> List[bool]:
        if self.polyline.getDimensions() != 2:
            raise ValueError("Inclusion queries only works on 2D.")

        poly = self.polyline.getNodes()
        if not self.polyline.isClosed():
            poly = np.array(list(poly) + [poly[0]])

        polygon = shageo.Polygon((poly))
        shageo_nodes = shageo.MultiPoint(np.array(test_nodes)[:, :2]).geoms

        results = []
        for n in shageo_nodes:
            results += [polygon.contains(n)]

        return results

    def isPointInside(self, test_node: np.ndarray) -> bool:
        results = self.arePointsInside(np.array([test_node]))
        return results[0]

    def getPointDistanceFromOrigin(self, point: np.ndarray) -> Optional[float]:
        """
        Point must be a point within the polyline. Typically coming from an intersection process.
        :param point: Numpy array 2D or 3D
        :return: Distance from the origin along the polyline.
        """
        distance = 0
        for i, n in enumerate(self.polyline.getNodes()[:-1]):
            segment = Vector(n0=n, n1=self.polyline.getNodes()[i+1])
            if self.checkNodeWithinSegment(point=point, segment=segment.getNodes()):
                distance += Vector(n0=n, n1=point).getLength()
                break
            else:
                distance += segment.getLength()
        else:
            raise ValueError("Point not along polyline.")

        return float(distance)

    def getPointAtDistanceFromOrigin(self, distance: float) -> Optional[np.ndarray]:

        if distance > self.polyline.getLength():
            raise ValueError("Distance is greater than polyline length.")
        elif distance == self.polyline.getLength():
            return self.polyline.getNodes()[-1]

        current_distance = 0
        for i, n in enumerate(self.polyline.getNodes()[:-1]):
            segment = Vector(n0=n, n1=self.polyline.getNodes()[i + 1])

            if current_distance + segment.getLength() > distance:
                out_point = n + segment.getNormalizedVector().getN1() * (distance - current_distance)
                return out_point
            elif current_distance + segment.getLength() < distance:
                current_distance += segment.getLength()
            else:
                return self.polyline.getNodes()[i + 1]

    @staticmethod
    def checkNodeWithinSegment(point: np.ndarray, segment: Union[List[float], np.ndarray],
                               cross_tolerance: float = 1e-6, dot_tolerance: float = 1e-12) -> bool:
        segment = np.array(segment)

        segment_vector = Vector(n0=segment[0], n1=segment[1])
        test_vector = Vector(n0=segment[0], n1=point)

        if test_vector.getLength() > segment_vector.getLength():
            return False

        cross_vector = Vector(n0=np.cross(segment_vector.getNormalizedVector(), test_vector.getNormalizedVector()))

        # Si colinean checkeo que node esta en segment
        if cross_vector.getLength() < cross_tolerance:
            # Debe ser mayor que 0 para que el punto este dentro del segment.
            dot = np.dot(segment_vector.getNormalizedVector(), test_vector.getNormalizedVector())
            if dot >= -dot_tolerance:  # - toleran ya que puede estar muy cerca por el otro lado
                return True

        return False
