from typing import TYPE_CHECKING, Union, Optional, Callable, Dict

import ezdxf.entities

from geogeometry.geo_io.readers.dxf_components.DxfEntityHandler import DxfEntityHandler

if TYPE_CHECKING:
    from geogeometry.geometry.triangulation.Triangulation import Triangulation
    from geogeometry.geometry.polyline.Polyline import Polyline

output_types = Optional[Union['Triangulation', 'Polyline']]
handler_method = Callable[..., output_types]


class EntityHandlerRegistry:

    def __init__(self):
        self.handlers: Dict[str, handler_method] = {}
        self.setHandlers()

    def setHandlers(self) -> None:
        self.handlers["POLYLINE"] = DxfEntityHandler.handlePolyline
        self.handlers["LINE"] = DxfEntityHandler.handleLine

    def getHandler(self, entity_type: str) -> handler_method:
        return self.handlers.get(entity_type)
