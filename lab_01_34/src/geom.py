from pyqtgraph import Point

UNFOLDED_ANGLE = 180
OY = Point(0, 1)

"""
a, b, c - vertices of the triangle
m - orthocenter
Solving a system of two dot products:
am * bc = 0
cm * ab = 0
"""
def orthocenter(a: Point, b: Point, c: Point) -> Point:
    if b.y() != a.y():
        k_ba = (b.x() - a.x()) / (b.y() - a.y())
    if c.y() != b.y():
        k_cb = (c.x() - b.x()) / (c.y() - b.y())

    if b.y() == a.y():
        m_x = c.x()
        m_y = -k_cb * (m_x - a.x()) + a.y()
    elif c.y() == b.y():
        m_x = a.x()
        m_y = -k_ba * (m_x - c.x()) + c.y()
    else:
        m_x = (k_ba * c.x() + c.y() - k_cb * a.x() - a.y()) / (k_ba - k_cb)
        m_y = -k_cb * (m_x - a.x()) + a.y()
    return Point(m_x, m_y)


"""
Vector projection a on b
"""
def projection(a: Point, b: Point) -> Point:
    return b * (Point.dotProduct(a, b) / b.length()**2)


"""
Finding the maximum angle between OY and the straight line connecting the orthocenter to (0, 0)
"""
def find_max_angle(points: list[Point]):
    ans = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                a = points[i]
                b = points[j]
                c = points[k]
                ab = b - a
                bc = c - b
                if ab != bc:
                    ac = c - a
                    m = orthocenter(a, b, c)
                    a_h = c + projection(-ac, bc)
                    b_h = a + projection(ab, ac)
                    c_h = a + projection(ac, ab)
                    source_angle = m.angle(OY)
                    angle = source_angle
                    if m.y() < 0:
                        angle += UNFOLDED_ANGLE
                    if (m.x() >= 0) == (m.y() >= 0):
                        angle *= -1
                    if ans is None or ans[0] < angle:
                        ans = (angle, source_angle, m, a, b, c, a_h, b_h, c_h)
    return ans
