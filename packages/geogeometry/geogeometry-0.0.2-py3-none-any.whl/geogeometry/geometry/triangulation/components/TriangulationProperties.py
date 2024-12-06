from typing import Optional, Union, List

import numpy as np


class TriangulationProperties(object):

    def __init__(self):
        super().__init__()

        self.nodes: Optional[np.ndarray] = None
        self.faces: Optional[np.ndarray] = None

        self.markers: Optional[np.ndarray] = None

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        if isinstance(nodes, list):
            nodes = np.array(nodes)
        self.nodes = nodes

    def setFaces(self, faces: Union[List[int], np.ndarray[int]]) -> None:
        if isinstance(faces, list):
            faces = np.array(faces).astype(int)
        self.faces = faces

    def setMarkers(self, markers: Union[List[int], np.ndarray[int]]) -> None:
        if isinstance(markers, list):
            markers = np.array(markers).astype(int)
        self.markers = markers

    def getNodes(self) -> np.ndarray:
        return self.nodes

    def getFaces(self) -> np.ndarray:
        return self.faces

    def getMarkers(self) -> np.ndarray:
        return self.markers
