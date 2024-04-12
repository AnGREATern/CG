import unittest
import sys
from PyQt5.QtCore import QPoint

sys.path.append("./src")
from fill import get_x_barrier, sign


class TestFigure(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_sign_positive(self):
        self.assertEqual(sign(12.32), 1)

    def test_sign_zero(self):
        self.assertEqual(sign(0), 0)

    def test_sign_negative(self):
        self.assertEqual(sign(-4), -1)

    def test_barrier_pos(self):
        ans = get_x_barrier([[QPoint(1, 1), QPoint(2, 1), QPoint(9, 10)]])
        self.assertEqual(ans, 4)


if __name__ == "__main__":
    unittest.main()
