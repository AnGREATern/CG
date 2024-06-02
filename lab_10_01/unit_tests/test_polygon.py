import unittest
import sys

sys.path.append("./src")
from canvas import f, sign


class TestPolygon(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def testSignPositive(self):
        self.assertEqual(sign(12.32), 1)

    def testSignZero(self):
        self.assertEqual(sign(0), 0)

    def testSignNegative(self):
        self.assertEqual(sign(-4), -1)

    def testFunc(self):
        self.assertAlmostEqual(f("x**2+3*z", 3, 2), 15)


if __name__ == "__main__":
    unittest.main()
