import consts
from PyQt5.QtGui import QColor, QImage, QPainter
from PyQt5.QtCore import QPoint, QLine

BACK = -1


class SegmentList:
    def __init__(self, image: QImage) -> None:
        self.segments: list[QLine] = []
        self.image = image

    def addPoint(self, point: QPoint) -> None:
        self.image.setPixelColor(point, QColor(*consts.SEGMENT_COLOR_DEFAULT))
        if not self.segments or self.segments[BACK].p2():
            self.segments.append(QLine())
        if not self.segments[BACK].p1():
            self.segments[BACK].setP1(point)
        elif not self.segments[BACK].p2():
            self.segments[BACK].setP2(point)
            self.draw(BACK)

    def draw(self, index: int | None = None) -> None:
        painter = QPainter(self.image)
        painter.setPen(QColor(*consts.SEGMENT_COLOR_DEFAULT))
        if index is None:
            for segment in self.segments:
                painter.drawLine(segment)
        else:
            painter.drawLine(self.segments[index])
        painter.end()

    def clear(self) -> None:
        self.segments: list[QLine] = []
