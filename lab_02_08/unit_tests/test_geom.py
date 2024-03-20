import unittest
import sys

sys.path.append("./src")
from geom import Point


class TestFigure(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_rotate(self):
        gr = Point(23, 56)
        for _ in range(4):
            gr.rotate(90)
        self.assertEqual(gr, Point(23, 56))

    def test_move(self):
        gr = Point(0, 0)
        gr.move(Point(5, 0))
        gr.move(Point(0, 5))
        gr.move(Point(10, 10))
        self.assertEqual(gr, Point(15, 15))

    def test_scale(self):
        gr = Point(1, 2)
        gr.scale(Point(2, 1))
        gr.scale(Point(1, 4))
        gr.scale(Point(0.25, 0.25))
        self.assertEqual(gr, Point(0.5, 2))


if __name__ == "__main__":
    unittest.main()
