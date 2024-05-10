import consts
from segmentList import SegmentList
from polygon import Polygon
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter, QMouseEvent, QVector2D
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QSize, QPoint, Qt, QLineF


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

    def saveImage(self, filename: str) -> None:
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
        if not self.polygon.is_closed:
            self.msg_box.setText("Многоугольник должен быть замкнутым")
            self.msg_box.show()
            return
        if not self.polygon.isConvex():
            self.msg_box.setText("Многоугольник должен быть выпуклым")
            self.msg_box.show()
            return
        temp_list = SegmentList(self.front_img)
        center = self.polygon.center()
        for segment in self.segment_list.segments:
            t = self.__get_visible_segment(segment, center)
            if t is not None:
                temp_list.addPoint(segment.pointAt(t[0]))
                temp_list.addPoint(segment.pointAt(t[1]))
        self.clearSegments()
        self.segment_list = temp_list
        self.segment_list.draw()
        self.updateImage()

    def __get_visible_segment(
        self, segment: QLineF, center: QPoint
    ) -> tuple[float, float] | None:
        t_min = 0.0
        t_max = 1.0
        is_visible = True
        for edge in self.polygon.edges().segments:
            w = QLineF(edge.p1(), segment.p1())
            w_vec = QVector2D(w.dx(), w.dy())
            n = edge.normalVector()
            if 90 < n.angleTo(QLineF(edge.p1(), center)) < 270:
                n_vec = QVector2D(-n.dx(), -n.dy())
            else:
                n_vec = QVector2D(n.dx(), n.dy())
            w_sc = QVector2D.dotProduct(w_vec, n_vec)
            d_vec = QVector2D(segment.dx(), segment.dy())
            d_sc = QVector2D.dotProduct(n_vec, d_vec)
            if d_sc == 0 and w_sc < 0:
                is_visible = False
            else:
                t = -w_sc / d_sc
                if d_sc > 0:
                    if t > 1:
                        is_visible = False
                    else:
                        t_min = max(t, t_min)
                else:
                    if t < 0:
                        is_visible = False
                    else:
                        t_max = min(t, t_max)
        if t_min <= t_max and is_visible:
            ans = (t_min, t_max)
        else:
            ans = None
        return ans

    def mousePressEvent(self, event: QMouseEvent) -> None:
        cur_point = event.pos()
        if self.rect().contains(cur_point):
            if event.button() == Qt.MouseButton.LeftButton:
                self.segment_list.addPoint(cur_point)
            elif event.button() == Qt.MouseButton.RightButton:
                self.polygon.addPoint(cur_point)
            self.updateImage()
