from PyQt5.QtCore import QPointF, QLineF
import consts

def get_solve(points: list[QPointF]):
    ans = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                a = points[i]
                b = points[j]
                c = points[k]
                ab = QLineF(a, b)
                bc = QLineF(b, c)
                if ab == bc:
                    continue
                ca = QLineF(c, a)
                normal = bc.normalVector()
                ha = QLineF(a, QPointF(a.x() + normal.dx(), a.y() + normal.dy()))
                a_h = ha.intersects(bc)[1]
                normal = ca.normalVector()
                hb = QLineF(b, QPointF(b.x() + normal.dx(), b.y() + normal.dy()))
                b_h = hb.intersects(ca)[1]
                normal = ab.normalVector()
                hc = QLineF(c, QPointF(c.x() + normal.dx(), c.y() + normal.dy()))
                c_h = hc.intersects(ab)[1]
                m = QLineF.intersects(ha, hb)[1]
                source_angle = QLineF(QPointF(*consts.CENTER), m).angle()
                angle = abs(source_angle % 180 - 90)
                if ans is None or ans[0] < angle:
                    ans = (angle, source_angle, m, a, b, c, a_h, b_h, c_h)
    return ans
