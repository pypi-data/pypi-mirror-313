from typing import Optional

from geogeometry.geo_io.readers.RhinoReader import RhinoReader
from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection
from geogeometry.geo_io.readers.DxfReader import DxfReader


class CadReader(object):

    @staticmethod
    def readFile(filepath: str) -> Optional[GeometryModelsCollection]:
        extension = filepath.split('.')[-1].lower()

        if extension == "dxf":
            return DxfReader.readFile(filepath)
        elif extension == '3dm':
            return RhinoReader.readFile(filepath)
        else:
            raise ValueError(f"File extension '.{extension}' not supported.")
