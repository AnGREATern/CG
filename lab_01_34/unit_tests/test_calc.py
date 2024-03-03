import unittest
from pyqtgraph import Point
import sys
sys.path.append("../src")
from calc import get_solution

class TestSolve(unittest.TestCase):
    def test_no_points(self):
        ans = get_solution([])
        self.assertEqual(ans, None)
    
    def test_two_points(self):
        a = Point(0, 0)
        b = Point(1, 1)
        ans = get_solution([a, b])
        self.assertEqual(ans, None)

    def test_one_line(self):
        a = Point(0, 0)
        b = Point(1, 1)
        c = Point(2, 2)
        ans = get_solution([a, b, c])
        self.assertEqual(ans, None)

    def test_m_equal_center(self):
        a = Point(-1, 0)
        b = Point(0.5, 0.86602540378)
        c = Point(0.5, -0.86602540378)
        ans = get_solution([a, b, c])
        self.assertAlmostEqual(ans[0], 90)

    def test_m_ox(self):
        a = Point(0, 0)
        b = Point(1.5, 0.86602540378)
        c = Point(1.5, -0.86602540378)
        ans = get_solution([a, b, c])
        self.assertAlmostEqual(ans[0], 90)
    
    def test_m_oy(self):
        a = Point(-1, 1)
        b = Point(0.5, 1.86602540378)
        c = Point(0.5, 0.13397459622)
        ans = get_solution([a, b, c])
        self.assertAlmostEqual(ans[0], 0)

    def test_first_quarter(self):
        ans = get_solution([Point(1.0, 3.0),
                            Point(12.3, 5.0),
                            Point(1.0, 2.0),
                            Point(12.6, 11.0),
                            Point(5.0, 5.0)])
        self.assertAlmostEqual(ans[0], 85.1376883124826)

    def test_second_quarter(self):
        ans = get_solution([Point(-1.0, 3.0),
                            Point(-4.0, 7.0),
                            Point(-8.0, 1.0),
                            Point(-5.0, 5.0)])
        self.assertAlmostEqual(ans[0], 58.73626830562256)

    def test_third_quarter(self):
        ans = get_solution([Point(-1.0, -3.0),
                            Point(-12.3, -5.0),
                            Point(-1.0, -2.0),
                            Point(-12.6, -11.0),
                            Point(-5.0, -5.0)])
        self.assertAlmostEqual(ans[0], 85.13768831248257)
    
    def test_forth_quarter(self):
        ans = get_solution([Point(3.0, -4.0),
                            Point(5.0, -11.0),
                            Point(20.0, -10.0),
                            Point(6.644366704117087, -10.268826959063178),
                            Point(20.074299687138662, -14.838305141610737)])
        self.assertAlmostEqual(ans[0], 81.29364180547769)


if __name__ == "__main__":
    unittest.main()
    