import consts
from pyqtgraph import Point

def orthocenter(a: Point, b: Point, c: Point) -> Point:
    if b.y() != a.y():
        k_ba = (b.x() - a.x()) / (b.y() - a.y())
    if c.y() != b.y():
        k_cb = (c.x() - b.x()) / (c.y() - b.y())

    if b.y() == a.y():
        x = c.x()
        y = -k_cb * (x - a.x()) + a.y()
    elif c.y() == b.y():
        x = a.x()
        y = -k_ba * (x - c.x()) + c.y()
    else:
        x = (k_ba * c.x() + c.y() - k_cb * a.x() - a.y()) / (k_ba - k_cb)
        y = -k_cb * (x - a.x()) + a.y()
    return Point(x, y)


def projection(a: Point, b: Point) -> Point:
    return b * (Point.dotProduct(a, b) / b.length()**2)


def get_solution(points: list[Point]):
    ans = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                a = points[i]
                b = points[j]
                c = points[k]
                ab = b - a
                bc = c - b
                if ab == bc:
                    continue
                ac = c - a
                m = orthocenter(a, b, c)
                a_h = c + projection(-ac, bc)
                b_h = a + projection(ab, ac)
                c_h = a + projection(ac, ab)
                source_angle = m.angle(Point(*consts.OY))
                angle = source_angle
                if m.y() < 0:
                    angle += consts.UNFOLDED_ANGLE
                if (m.x() >= 0) == (m.y() >= 0):
                    angle *= -1
                if ans is None or ans[0] < angle:
                    ans = (angle, source_angle, m, a, b, c, a_h, b_h, c_h)
    return ans
