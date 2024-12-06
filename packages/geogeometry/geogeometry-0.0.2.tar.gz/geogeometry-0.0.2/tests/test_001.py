import unittest
from geogeometry import Triangulation


class TestBaseGeometry(unittest.TestCase):

    def setUp(self):
        pass

    def test_creation(self):
        t = Triangulation()
        self.assertIsNotNone(t)
        self.assertIsInstance(t, Triangulation)


if __name__ == "__main__":
    unittest.main()
