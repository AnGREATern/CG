from PyQt5.QtGui import QVector2D
from math import cos, sin, radians


class Point(QVector2D):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def rotate(self: "Point", phi: float):
        phi = radians(phi)
        x1 = self.x() * cos(phi) - self.y() * sin(phi)
        y1 = self.x() * sin(phi) + self.y() * cos(phi)
        self.setX(x1)
        self.setY(y1)

    def move(self: "Point", edit: "Point"):
        self += edit

    def scale(self: "Point", edit: "Point"):
        self *= edit
