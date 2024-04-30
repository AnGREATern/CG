import unittest
import sys
from PyQt5.QtCore import QPoint, QRect

sys.path.append("./src")
from clipping import get_point_code


class TestFigure(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_get_point_code(self):
        t, s = get_point_code(QPoint(30, 30), QRect(QPoint(340, 80), QPoint(350, 1000)))
        self.assertEqual(t, 9)
        self.assertEqual(s, 2)


if __name__ == "__main__":
    unittest.main()
