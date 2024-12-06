from typing import Optional, Union

import ezdxf
import ezdxf.entities

import numpy as np

from geogeometry.geometry.triangulation.Triangulation import Triangulation
from geogeometry.geometry.polyline.Polyline import Polyline


class DxfEntityHandler(object):

    @staticmethod
    def handlePolyline(entity: ezdxf.entities.Polyline) -> Optional[Union[Triangulation, Polyline]]:

        if entity.is_poly_face_mesh:
            return DxfEntityHandler.handlePolyfaceMesh(entity=entity)
        else:
            return DxfEntityHandler.handleActualPolyline(entity=entity)

    @staticmethod
    def handlePolyfaceMesh(entity: ezdxf.entities.Polyline) -> Optional[Triangulation]:

        vertices = []
        faces = []
        for vertex in entity.vertices:
            if vertex.is_face_record:
                # Just considers triangulations
                indices = [vertex.get_dxf_attrib(name, 0) for name in ('vtx0', 'vtx1', 'vtx2')]
                # indices = [vertex.dxf.vtx0, vertex.dxf.vtx1, vertex.dxf.vtx2, vertex.dxf.vtx3]

                indices = [idx - 1 for idx in indices if idx != 0]
                faces += [indices]

            elif vertex.is_poly_face_mesh_vertex:
                x, y, z = vertex.dxf.location
                vertices += [[x, y, z]]

        vertices = np.array(vertices)

        t = Triangulation()
        t.setNodes(nodes=vertices)
        t.setFaces(faces=faces)

        return t

    @staticmethod
    def handleActualPolyline(entity: ezdxf.entities.Polyline) -> Optional[Polyline]:

        nodes = [list(p) for p in entity.points()]
        if entity.is_closed:
            nodes += [nodes[0]]

        p = Polyline()
        p.setNodes(nodes=nodes)
        return p

    @staticmethod
    def handleLine(entity: ezdxf.entities.Line) -> Optional[Polyline]:
        n0 = np.array(entity.dxf.start)
        n1 = np.array(entity.dxf.end)

        p = Polyline()
        p.setNodes(nodes=[n0, n1])
        return p
