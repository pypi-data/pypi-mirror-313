from typing import Optional, List

from geogeometry.geometry.model.GeometryModel import GeometryModel
from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection


class GeometryModelsCollection(BaseGeometryCollection):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

    def deleteEmptyModels(self) -> None:

        empty_models: List[GeometryModel] = [e for e in self if not len(e)]
        for m in empty_models:
            self.deleteElement(identifier=m.getName())
