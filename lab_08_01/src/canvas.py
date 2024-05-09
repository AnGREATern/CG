import consts
from segmentList import SegmentList
from polygon import Polygon
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter, QMouseEvent
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QSize, QPoint, Qt, QLine


FIGURE_SIZE = QSize(1230, 628)


class Canvas(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.initImage()
        self.initMessageBox()

        self.segment_list = SegmentList(self.front_img)
        self.polygon = Polygon(self.front_img)

    def initImage(self) -> None:
        self.picture = QGraphicsScene()
        self.setScene(self.picture)
        self.front_pix = QPixmap(FIGURE_SIZE)
        self.front_img = QImage(FIGURE_SIZE, QImage.Format_ARGB32)
        self.clearImage()
        self.updateImage()

    def initMessageBox(self) -> None:
        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Critical)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
        self.msg_box.setWindowTitle("Не получилось отсечь отрезки")

    def clearImage(self) -> None:
        self.front_img.fill(QColor(*consts.BACK_COLOR_DEFAULT))

    def updateImage(self) -> None:
        self.picture.clear()
        self.front_pix.convertFromImage(self.front_img)
        self.picture.addPixmap(self.front_pix)

    def save(self, filename: str) -> None:
        image = QImage(self.picture.sceneRect().size().toSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        self.picture.render(painter)
        painter.end()
        image.save(filename + ".png")

    def clearAll(self) -> None:
        self.segment_list.clear()
        self.polygon.clear()
        self.clearImage()
        self.updateImage()

    def clearSegments(self) -> None:
        self.segment_list.clear()
        self.clearImage()
        self.polygon.draw()
        self.updateImage()

    def clearPolygon(self) -> None:
        self.polygon.clear()
        self.clearImage()
        self.segment_list.draw()
        self.updateImage()

    def closePolygon(self) -> None:
        self.polygon.closePolygon()
        self.updateImage()

    def clipSegments(self) -> None:
        pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        cur_point = event.pos()
        if self.rect().contains(cur_point):
            if event.button() == Qt.MouseButton.LeftButton:
                self.segment_list.addPoint(cur_point)
            elif event.button() == Qt.MouseButton.RightButton:
                self.polygon.addPoint(cur_point)
            self.updateImage()
