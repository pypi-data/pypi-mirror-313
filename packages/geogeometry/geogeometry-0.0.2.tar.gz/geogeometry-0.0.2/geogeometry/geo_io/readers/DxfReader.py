from typing import Optional, Union

import ezdxf
import ezdxf.entities

from geogeometry.geo_io.readers.dxf_components.EntityHandlerRegistry import EntityHandlerRegistry

from geogeometry.geometry.model.GeometryModel import GeometryModel
from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection

from geogeometry.geometry.polyline.Polyline import Polyline
from geogeometry.geometry.triangulation.Triangulation import Triangulation


class DxfReader(object):

    @staticmethod
    def readFile(filepath: str) -> Optional[GeometryModelsCollection]:
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()
        groups = msp.groupby(dxfattrib="layer")

        handlers_registry = EntityHandlerRegistry()

        models_collection = GeometryModelsCollection()
        for layer, entities in groups.items():

            model = GeometryModel(name=layer)

            for entity in entities:
                handler = handlers_registry.getHandler(entity.dxftype())

                if handler:
                    result = handler(entity)
                    if isinstance(result, Polyline):
                        model.addPolyline(result)
                    elif isinstance(result, Triangulation):
                        model.addTriangulation(result)
                else:
                    raise ValueError(f"Entity type '{entity.dxftype()}' not supported.")

            if len(model):
                models_collection.addElement(model)

        return models_collection
