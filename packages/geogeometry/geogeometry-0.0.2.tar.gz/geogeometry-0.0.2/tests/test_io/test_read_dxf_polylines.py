import os
import unittest
from geogeometry import CadReader


class TestReadDxfPolylines(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_dir, 'resources', 'dxf_files')

        self.extension = "dxf"

        self.file_003_path = os.path.join(self.resource_dir, "file_003." + self.extension)
        self.file_004_path = os.path.join(self.resource_dir, "file_004." + self.extension)
        self.file_005_path = os.path.join(self.resource_dir, "file_005." + self.extension)

    def test_file_003(self):
        """
        :case: Multiple 2-points 3D polylines (segments)
        """
        models_collection = CadReader.readFile(self.file_003_path)
        self.assertEqual(len(models_collection), 15)  # Layers

        n_polylines = len([m.getPolylines() for m in models_collection])
        self.assertEqual(n_polylines, 15)

    def test_file_004(self):
        """
        :case: Multiple 3D polylines
        """
        models_collection = CadReader.readFile(self.file_004_path)
        self.assertEqual(len(models_collection), 47)  # Layers

        n_polylines = sum([len(m.getPolylines()) for m in models_collection])
        self.assertEqual(n_polylines, 47)

    def test_file_005(self):
        """
        :case: Multiple 3D polylines
        """
        models_collection = CadReader.readFile(self.file_005_path)
        self.assertEqual(len(models_collection), 16)  # Layers

        n_polylines = sum([len(m.getPolylines()) for m in models_collection])
        self.assertEqual(n_polylines, 16)


if __name__ == "__main__":
    unittest.main()