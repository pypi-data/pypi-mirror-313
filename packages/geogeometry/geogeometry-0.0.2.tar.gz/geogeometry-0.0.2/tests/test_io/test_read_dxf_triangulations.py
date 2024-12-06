import os
import unittest
from geogeometry import CadReader


class TestReadDxfTriangulations(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_dir, 'resources', 'dxf_files')

        self.extension = "dxf"

        self.file_001_path = os.path.join(self.resource_dir, "file_001." + self.extension)
        self.file_002_path = os.path.join(self.resource_dir, "file_002." + self.extension)

    def test_file_001(self):
        models_collection = CadReader.readFile(self.file_001_path)
        self.assertEqual(len(models_collection), 2)

        n_triangulations = len([m.getTriangulations() for m in models_collection])
        self.assertEqual(n_triangulations, 2)

    def test_file_002(self):
        models_collection = CadReader.readFile(self.file_002_path)
        self.assertEqual(len(models_collection), 2)

        n_triangulations = sum([len(m.getTriangulations()) for m in models_collection])
        self.assertEqual(n_triangulations, 3)


if __name__ == "__main__":
    unittest.main()
