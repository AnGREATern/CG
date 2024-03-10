from PyQt5.QtGui import QVector2D
from math import cos, sin, radians

TYPE_INDEX = 0
POINTS_INDEX = 1

class Grasshopper():
    def __init__(self) -> None:
        mustache = ("polyline", [QVector2D(-2, 8), QVector2D(-1, 8), QVector2D(0, 5), QVector2D(1, 8), QVector2D(2, 8)])
        left_leg = ("polyline", [QVector2D(-2, -4), QVector2D(-1, -4), QVector2D(-1, -2.598)])
        right_leg = ("polyline", [QVector2D(2, -4), QVector2D(1, -4), QVector2D(1, -2.598)])
        head = ("ellipse", [QVector2D(0, 5), QVector2D(2, 5), QVector2D(0, 7)])
        left_eye = ("ellipse", [QVector2D(-0.75, 5.25), QVector2D(-0.25, 5.25), QVector2D(-0.75, 5.75)])
        right_eye = ("ellipse", [QVector2D(0.75, 5.25), QVector2D(1.25, 5.25), QVector2D(0.75, 5.75)])
        body = ("ellipse", [QVector2D(0, 0), QVector2D(2, 0), QVector2D(0, 3)])
        left_arm = ("triangle", [QVector2D(-1, -0.5), QVector2D(-1, 0.5), QVector2D(-5, 3)])
        right_arm = ("triangle", [QVector2D(1, -0.5), QVector2D(1, 0.5), QVector2D(5, 3)])
        self.anchor_pts: tuple[tuple[str, list[QVector2D]]] = (mustache, left_leg, right_leg,
                                                            head, left_eye, right_eye,
                                                            body, left_arm, right_arm)

    def rotate(self, phi: float, center: QVector2D) -> None:
        phi = radians(phi)
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                x1 = center.x() + (point.x() - center.x()) * cos(phi) - (point.y() - center.y()) * sin(phi)
                y1 = center.y() + (point.x() - center.x()) * sin(phi) + (point.y() - center.y()) * cos(phi)
                point.setX(x1)
                point.setY(y1)

    def move(self, dx: float, dy: float) -> None:
        av = QVector2D(dx, dy)
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                point += av
        

    def scale(self, kx: float, ky: float, center: QVector2D) -> None:
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                point.setX((point.x() - center.x()) * kx + center.x())
                point.setY((point.y() - center.y()) * ky + center.y())
