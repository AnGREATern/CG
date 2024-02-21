import unittest
from PyQt5.QtCore import QPointF
import sys
sys.path.append("../src")
from calc import get_solve

class TestSolve(unittest.TestCase):
    def test_no_points(self):
        ans = get_solve([])
        self.assertEqual(ans, None)
    
    def test_two_points(self):
        a = QPointF(0, 0)
        b = QPointF(1, 1)
        ans = get_solve([a, b])
        self.assertEqual(ans, None)

    def test_one_line(self):
        a = QPointF(0, 0)
        b = QPointF(1, 1)
        c = QPointF(2, 2)
        ans = get_solve([a, b, c])
        self.assertEqual(ans, None)

    def test_m_equal_center(self):
        a = QPointF(-1, 0)
        b = QPointF(0.5, 0.86602540378)
        c = QPointF(0.5, -0.86602540378)
        ans = get_solve([a, b, c])
        self.assertAlmostEqual(ans[0], 90)

    def test_first_quarter(self):
        ans = get_solve([QPointF(1.0, 3.0),
                        QPointF(12.3, 5.0),
                        QPointF(1.0, 2.0),
                        QPointF(12.6, 11.0),
                        QPointF(5.0, 5.0)])
        self.assertAlmostEqual(ans[0], 85.13768831248262)

    def test_second_quarter(self):
        ans = get_solve([QPointF(-3.672017031888, 1.3547104541704105),
                        QPointF(-6.76024383541401, 2.190584997514419),
                        QPointF(-2.221486260534874, 4.166288463600258),
                        QPointF(-4.8417999120114885, 2.0386078078155077)])
        self.assertAlmostEqual(ans[0], 83.35987790606629)

    def test_third_quarter(self):
        ans = get_solve([QPointF(-6.081769764942382, -6.826728257954285),
                        QPointF(-3.157312564633661, -3.913832122058496),
                        QPointF(-8.772270389226406, -3.5085596161947343),
                        QPointF(-5.356504379265819, -6.294808094008097),
                        QPointF(-6.077898703409508, -3.255264300029885),
                        QPointF(-4.02971214624047, -5.408274487431119),
                        QPointF(-7.113763169104196, -5.256297297732208),
                        QPointF(-4.500559630647146, -3.1792757051804283),
                        QPointF(-15.451890554273113, -15.702801013984587),
                        QPointF(-20.78942802188425, -7.860588457450255),
                        QPointF(-18.551105858047322, -12.55356605033694)])
        self.assertAlmostEqual(ans[0], 86.3444028413453)
    
    def test_forth_quarter(self):
        ans = get_solve([QPointF(15.769833987452262, -18.66678686212356),
                        QPointF(12.039297047724045, -14.035558974406436),
                        QPointF(8.423545859987467, -17.49354246390189),
                        QPointF(6.644366704117087, -10.268826959063178),
                        QPointF(20.074299687138662, -14.838305141610737)])
        self.assertAlmostEqual(ans[0], 67.42842975517135)
    
    def test_multi(self):
        ans = get_solve([QPointF(12.147925133263051, -18.73219907520989),
                        QPointF(-27.727982135449345, -14.818242836192795),
                        QPointF(-18.353646040699413, 9.869788825299587),
                        QPointF(14.80631895117721, -14.216095722497869),
                        QPointF(-14.01626665357631, -16.022537063582675),
                        QPointF(10.46893956405411, 18.60092197387616),
                        QPointF(-18.073815112497922, -23.248302427921914),
                        QPointF(-24.509926461132203, 6.557979699977437),
                        QPointF(18.72395194599808, 17.246090968062553),
                        QPointF(101.6751530380079, 87.4133110558165),
                        QPointF(-5.5645850636023795, 129.39615446293368),
                        QPointF(-73.34381347414394, -70.14583067207033),
                        QPointF(84.07428110141414, -28.960021035474966),
                        QPointF(42.29834248548423, 56.93308825542567),
                        QPointF(82.02392828590838, 19.57640262731968),
                        QPointF(71.77216420837956, 29.66543451228261),
                        QPointF(91.76310415956075, 31.574170274302624),
                        QPointF(84.33057520335237, 34.846288723479795),
                        QPointF(77.92322265489685, 11.94145957923962),
                        QPointF(61.520400130850746, -25.415226048866373)])
        self.assertAlmostEqual(ans[0], 89.96665209456705)


if __name__ == "__main__":
  unittest.main()
    