import consts
from PyQt5.QtGui import QColor, QImage, QPainter, QPolygon
from PyQt5.QtCore import QPoint


class Polygon(QPolygon):
    def __init__(self, image: QImage) -> None:
        super().__init__()
        self.image = image
        self.is_closed = False

    def addPoint(self, point: QPoint) -> None:
        if not self.is_closed:
            self.image.setPixelColor(point, QColor(*consts.POLYGON_COLOR_DEFAULT))
            self.putPoints(self.size(), point.x(), point.y())
            self.drawLine(self.point(self.size() - 2), self.point(self.size() - 1))

    def closePolygon(self) -> None:
        if not self.is_closed:
            self.is_closed = self.drawLine(self.point(0), self.point(self.size() - 1))
            
    def clear(self) -> None:
        super().clear()
        self.is_closed = False

    def drawLine(self, p1: QPoint, p2: QPoint) -> bool:
        is_ok = False
        if self.size() > 1:
            painter = QPainter(self.image)
            painter.setPen(QColor(*consts.POLYGON_COLOR_DEFAULT))
            painter.drawLine(p1, p2)
            painter.end()
            is_ok = True
        return is_ok

    def draw(self) -> None:
        painter = QPainter(self.image)
        painter.setPen(QColor(*consts.POLYGON_COLOR_DEFAULT))
        painter.drawPolygon(self)
        painter.end()
