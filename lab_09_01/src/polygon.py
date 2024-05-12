import consts
from segmentList import SegmentList
from PyQt5.QtGui import QColor, QImage, QPainter, QPolygon
from PyQt5.QtCore import QPoint, QLineF, QPointF


class Polygon(QPolygon):
    def __init__(self, image: QImage, color: QColor = QColor(*consts.POLYGON_COLOR_DEFAULT)) -> None:
        super().__init__()
        self.image = image
        self.color = color
        self.is_closed = False

    def addPoint(self, point: QPoint | QPointF) -> None:
        if not self.is_closed:
            if isinstance(point, QPointF):
                point = QPoint(int(point.x()), int(point.y()))
            self.image.setPixelColor(point, self.color)
            self.putPoints(self.size(), point.x(), point.y())
            self.drawLine(self.pointAt(-2), self.pointAt(-1))

    def closePolygon(self) -> None:
        if not self.is_closed and self.size():
            self.is_closed = self.drawLine(self.pointAt(0), self.pointAt(-1))

    def clear(self) -> None:
        super().clear()
        self.is_closed = False

    def isConvex(self) -> bool:
        if not self.is_closed:
            return False
        ans = True
        for cur_point in range(self.size()):
            a = QLineF(self.pointAt(cur_point), self.pointAt(cur_point + 1))
            b = QLineF(self.pointAt(cur_point - 1), self.pointAt(cur_point + 2))
            if a.intersect(b, QPoint()) == 1:
                ans = False
        return ans

    def pointAt(self, index: int) -> QPoint:
        return self.point((index + self.size()) % self.size())

    def edges(self) -> SegmentList:
        ans = SegmentList(self.image)
        for cur_point in range(self.size()):
            ans.addPoint(self.pointAt(cur_point))
            ans.addPoint(self.pointAt(cur_point + 1))
        return ans

    def center(self) -> QPoint:
        center = QPoint(0, 0)
        for cur_point in range(self.size()):
            center += self.pointAt(cur_point)
        if self.size():
            center /= self.size()
        return center

    def drawLine(self, p1: QPoint, p2: QPoint) -> bool:
        is_ok = False
        if self.size() > 1:
            painter = QPainter(self.image)
            painter.setPen(self.color)
            painter.drawLine(p1, p2)
            painter.end()
            is_ok = True
        return is_ok

    def draw(self) -> None:
        self.is_closed = True
        painter = QPainter(self.image)
        painter.setPen(self.color)
        painter.drawPolygon(self)
        painter.end()
