import unittest
import sys
from PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import QImage, QColor

sys.path.append("./src")
from algorithms import plot_pixel


class TestGeom(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def testAddPoint(self):
        res = plot_pixel(QImage(), QPointF(1.1, 245.2), QColor("r"))
        self.assertEqual(res, QPoint(1, 245))


if __name__ == "__main__":
    unittest.main()
