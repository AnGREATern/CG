import consts
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QSize, QPoint
from math import radians, cos, sin


CANVAS_SIZE = QSize(930, 740)
INVISIBLE = 0
ABOVE = 1
BELOW = -1
OX = 0
OY = 1
OZ = 2


def f(func: str, x: int, z: int) -> int:
    return round(eval(func.replace("x", str(x)).replace("z", str(z))))


def sign(x: float) -> int:
    ans = 0
    if x > 0:
        ans = 1
    elif x < 0:
        ans = -1
    return ans


class Canvas(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.initImage()
        self.initMessageBox()
        self.points: list[QPoint] = []

    def initImage(self) -> None:
        self.picture = QGraphicsScene()
        self.setScene(self.picture)
        self.front_pix = QPixmap(CANVAS_SIZE)
        self.front_img = QImage(CANVAS_SIZE, QImage.Format_ARGB32)
        self.clearImage()
        self.updateImage()

    def initMessageBox(self) -> None:
        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Critical)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
        self.msg_box.setWindowTitle("Не получилось отсечь")

    def clearImage(self) -> None:
        self.front_img.fill(QColor(*consts.BACK_COLOR_DEFAULT))

    def updateImage(self) -> None:
        self.picture.clear()
        self.front_pix.convertFromImage(self.front_img)
        self.picture.addPixmap(self.front_pix)

    def saveImage(self, filename: str) -> None:
        image = QImage(self.picture.sceneRect().size().toSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        self.picture.render(painter)
        painter.end()
        image.save(filename + ".png")

    def clearAll(self) -> None:
        self.points.clear()
        self.clearImage()
        self.updateImage()

    def rotateFigure(self, point: QPoint, z: int, axis: int, phi: int) -> None:
        phi = radians(phi)
        if axis == OX:
            pr_y = point.y()
            point.setY(round(cos(phi) * pr_y - sin(phi) * z))
            z = round(cos(phi) * z + sin(phi) * pr_y)
        elif axis == OY:
            pr_x = point.x()
            point.setX(round(cos(phi) * pr_x - sin(phi) * z))
            z = round(cos(phi) * z + sin(phi) * pr_x)
        elif axis == OZ:
            pr_x = point.x()
            point.setX(round(cos(phi) * pr_x - sin(phi) * point.y()))
            point.setY(round(cos(phi) * point.y() + sin(phi) * pr_x))
            
    def updateHorizons(self, start: QPoint, end: QPoint) -> None:
        if not (1 <= start.x() < len(self.top)):
            if not (1 <= end.x() < len(self.top)):
                return
            else:
                start, end = end, start
        if start == end and 1 <= start.x() < len(self.top):
            if start.y() > self.top[start.x()]:
                self.top[start.x()] = start.y()
                # self.front_img.setPixel(start, QColor(*consts.SEGMENT_COLOR_DEFAULT).rgba())
                self.points.append(start)
            if start.y() < self.bottom[start.x()]:
                self.bottom[start.x()] = start.y()
                # self.front_img.setPixel(start, QColor(*consts.SEGMENT_COLOR_DEFAULT).rgba())
                self.points.append(start)
        else:
            d: QPoint = end - start          
            if abs(d.x()) < abs(d.y()):
                step = QPoint(sign(d.x()), 0)
                d = QPoint(abs(d.y()), abs(d.x()))
                is_changed = True
            else:
                step = QPoint(0, sign(d.y()))
                d = QPoint(abs(d.x()), abs(d.y()))
                is_changed = False
            e = 2 * d.y() - d.x()
            if 1 <= start.x() < len(self.top):
                y_top = self.top[start.x()]
                y_bottom = self.bottom[start.x()]
            i = 0
            while i < d.x() and 1 < start.x() < len(self.top):
                if start.y() > self.top[start.x()]:
                    # self.front_img.setPixel(start, QColor(*consts.SEGMENT_COLOR_DEFAULT).rgba())
                    self.points.append(start)
                    y_top = max(y_top, start.y())
                if start.y() < self.bottom[start.x()]:
                    # self.front_img.setPixel(start, QColor(*consts.SEGMENT_COLOR_DEFAULT).rgba())
                    self.points.append(start)
                    y_bottom = min(y_bottom, start.y())
                if e >= 0:
                    if is_changed:
                        self.top[start.x()] = y_top
                        self.bottom[start.x()] = y_bottom
                        y_top = self.top[start.x()]
                        y_bottom = self.bottom[start.x()]
                    start += step
                    e -= 2 * d.x()
                else:
                    if not is_changed:
                        self.top[start.x()] = y_top
                        self.bottom[start.x()] = y_bottom
                        y_top = self.top[start.x()]
                        y_bottom = self.bottom[start.x()]
                    start += step
                    e += 2 * d.y()
                i += 1

    def buildFigure(
        self, x_range: range, z_range: range, func: str, axis: int, phi: int
    ) -> None:
        self.top = [0] * CANVAS_SIZE.width()
        self.bottom = [CANVAS_SIZE.height()] * CANVAS_SIZE.width()
        left = QPoint(-1, -1)
        right = QPoint(-1, -1)
        for z in z_range:
            pr = QPoint(x_range.start, f(func, x_range.start, z))
            self.rotateFigure(pr, z, axis, phi)
            if left.x() != -1:
                self.updateHorizons(pr, left)
            left = pr
            for x in x_range:
                y = f(func, x, z)
                cur = QPoint(x, y)
                self.rotateFigure(cur, z, axis, phi)
                self.updateHorizons(pr, cur)
                pr = cur
            if left.x() != -1:
                self.updateHorizons(pr, right)
            right = pr
        self.printPoints()
        
    def printPoints(self) -> None:
        left_top = QPoint(self.points[0])
        right_bottom = QPoint(self.points[0])
        for point in self.points:
            left_top.setX(min(left_top.x(), point.x()))
            left_top.setY(min(left_top.y(), point.y()))
            right_bottom.setX(max(right_bottom.x(), point.x()))
            right_bottom.setY(max(right_bottom.y(), point.y()))
        d = right_bottom - left_top
        k = max(d.x() / (CANVAS_SIZE.width() - 1), d.y() / (CANVAS_SIZE.height() - 1))
        for point in self.points:
            self.front_img.setPixel((point - left_top) / k, QColor(*consts.SEGMENT_COLOR_DEFAULT).rgba())
        self.updateImage()
