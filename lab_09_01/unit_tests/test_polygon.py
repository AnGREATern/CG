import unittest
import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage

sys.path.append("./src")
from polygon import Polygon


class TestPolygon(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def testAddPoint(self):
        polygon = Polygon(QImage(100, 100, QImage.Format_ARGB32))
        polygon.addPoint(QPoint(1, 0))
        self.assertEqual(polygon.size(), 1)
        self.assertEqual(polygon.pointAt(0), QPoint(1, 0))

    def testCenter(self):
        polygon = Polygon(QImage(100, 100, QImage.Format_ARGB32))
        polygon.addPoint(QPoint(1, 0))
        polygon.addPoint(QPoint(2, 0))
        polygon.addPoint(QPoint(3, 9))
        self.assertEqual(polygon.center(), QPoint(2, 3))


if __name__ == "__main__":
    unittest.main()
