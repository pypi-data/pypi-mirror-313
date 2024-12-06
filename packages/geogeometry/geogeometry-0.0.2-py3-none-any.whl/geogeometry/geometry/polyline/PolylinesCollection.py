from typing import Optional

from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection


class PolylinesCollection(BaseGeometryCollection):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)
