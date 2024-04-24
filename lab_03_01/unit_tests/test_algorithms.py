import unittest
import sys
from PyQt5.QtCore import QPoint

sys.path.append("./src")
from algorithms import is_step, sign


class TestFigure(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_sign_positive(self):
        self.assertEqual(sign(12.32), 1)

    def test_sign_zero(self):
        self.assertEqual(sign(0), 0)

    def test_sign_negative(self):
        self.assertEqual(sign(-4), -1)

    def test_is_step(self):
        ans = is_step(QPoint(1, 1))
        self.assertEqual(ans, True)


if __name__ == "__main__":
    unittest.main()
