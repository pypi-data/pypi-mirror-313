from typing import Optional

import numpy as np
import rhino3dm

from geogeometry.geometry.model.GeometryModel import GeometryModel
from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection
from geogeometry.geometry.polyline.Polyline import Polyline

from geogeometry.geometry.triangulation.Triangulation import Triangulation


class RhinoReader(object):

    @staticmethod
    def readFile(filepath: str) -> Optional[GeometryModelsCollection]:
        rhino_model = rhino3dm.File3dm.Read(filepath)

        # print(dir(rhino_model))

        models_collection = GeometryModelsCollection()
        for layer in rhino_model.Layers:
            layer_model = GeometryModel(name=layer.Name)
            models_collection.addElement(layer_model)

        for obj in rhino_model.Objects:
            obj_type = obj.Geometry.ObjectType.name

            layer_index = obj.Attributes.LayerIndex
            layer_name = rhino_model.Layers[layer_index].Name

            if obj_type == 'Mesh':

                nodes = np.array([[n.X, n.Y, n.Z] for n in obj.Geometry.Vertices])
                faces = np.array(obj.Geometry.Faces)[:, :3]

                t = Triangulation()
                t.setNodes(nodes=nodes)
                t.setFaces(faces=faces)

                models_collection[layer_name].addTriangulation(t)
            elif obj_type == "Curve":
                if hasattr(obj.Geometry, "Line"):
                    start = obj.Geometry.Line.From
                    end = obj.Geometry.Line.To

                    n0 = np.array([start.X, start.Y, start.Z])
                    n1 = np.array([end.X, end.Y, end.Z])

                    nodes = [n0, n1]

                else:
                    polyline = obj.Geometry.TryGetPolyline()

                    nodes = []
                    for i in range(polyline.Count):
                        point = obj.Geometry.Point(i)
                        nodes += [[point.X, point.Y, point.Z]]

                p = Polyline()
                p.setNodes(nodes=nodes)
                models_collection[layer_name].addPolyline(p)

            else:
                raise ValueError(f"obj_type: {obj_type}")

        models_collection.deleteEmptyModels()

        return models_collection
