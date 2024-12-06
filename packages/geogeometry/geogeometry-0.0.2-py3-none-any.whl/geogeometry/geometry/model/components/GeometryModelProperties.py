from typing import Optional, TYPE_CHECKING

from geogeometry.geometry.polyline.PolylinesCollection import PolylinesCollection
from geogeometry.geometry.triangulation.TriangulationsCollection import TriangulationsCollection

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline
    from geogeometry.geometry.triangulation.Triangulation import Triangulation


class GeometryModelProperties(object):

    def __init__(self):
        super().__init__()
        self.triangulations: Optional[TriangulationsCollection] = TriangulationsCollection()
        self.polylines: Optional[PolylinesCollection] = PolylinesCollection()

    def getTriangulations(self) -> Optional[TriangulationsCollection]:
        return self.triangulations

    def getPolylines(self) -> Optional[PolylinesCollection]:
        return self.polylines

    def addTriangulation(self, triangulation: 'Triangulation') -> None:
        self.triangulations.addElement(triangulation)

    def addPolyline(self, polyline: 'Polyline') -> None:
        self.polylines.addElement(polyline)
