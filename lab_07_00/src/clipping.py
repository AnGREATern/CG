from PyQt5.QtGui import QVector2D
from PyQt5.QtCore import QPoint, QLine, QRect
from consts import EPS


def get_point_code(point: QPoint, rect: QRect) -> tuple[int, int]:
    t = (1 << 3) * (point.x() < rect.left())
    t += (1 << 2) * (point.x() > rect.right())
    t += (1 << 1) * (point.y() > rect.bottom())
    t += point.y() < rect.top()
    s = (
        (point.x() < rect.left())
        + (point.x() > rect.right())
        + (point.y() > rect.bottom())
        + (point.y() < rect.top())
    )
    return t, s


def get_line_code(line: QLine, rect: QRect) -> tuple[int, int, int, int]:
    return *get_point_code(line.p1(), rect), *get_point_code(line.p2(), rect)


def clip(print_figure, line: QLine, rect: QRect) -> None:
    t1, s1, t2, s2 = get_line_code(line, rect)
    rc = True
    if QVector2D(line.p2() - line.p1()).length() < EPS:
        rc = False
    if (t1 & t2) and rc:
        rc = False
    if (not (s1 + s2)) and rc:
        print_figure(line)
        rc = False
    if rc:
        p_av = (line.p1() + line.p2()) / 2
        clip(print_figure, QLine(p_av, line.p2()), rect)
        clip(print_figure, QLine(line.p1(), p_av), rect)
