import consts
from polygon import Polygon
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter, QMouseEvent, QVector2D
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QSize, QPoint, Qt, QLineF, QPointF


FIGURE_SIZE = QSize(1230, 684)


class Canvas(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.initImage()
        self.initMessageBox()

        self.clipper = Polygon(self.front_img, QColor(*consts.CLIPPER_COLOR_DEFAULT))
        self.polygon = Polygon(self.front_img, QColor(*consts.POLYGON_COLOR_DEFAULT))

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
        self.clipper.clear()
        self.polygon.clear()
        self.clearImage()
        self.updateImage()
    
    def clearClipper(self) -> None:
        self.clipper.clear()
        self.clearImage()
        self.polygon.draw()
        self.updateImage()
        
    def closeClipper(self) -> None:
        self.clipper.closePolygon()
        self.updateImage()

    def clearPolygon(self) -> None:
        self.polygon.clear()
        self.clearImage()
        self.clipper.draw()
        self.updateImage()

    def closePolygon(self) -> None:
        self.polygon.closePolygon()
        self.updateImage()
        
    def __isCorrectPolygons(self) -> bool:
        is_ok = True
        if not self.polygon.is_closed:
            self.msg_box.setText("Многоугольник должен быть замкнутым")
            is_ok = False
        elif not self.clipper.isConvex():
            self.msg_box.setText("Отсекатель должен быть выпуклым")
            is_ok = False
        if not is_ok:
            self.msg_box.show()
        return is_ok
        
    def clip(self) -> None:
        if not self.__isCorrectPolygons():
            return
        center = self.clipper.center()
        for cl_edge in self.clipper.edges().segments:
            res = Polygon(self.front_img, QColor(*consts.POLYGON_COLOR_DEFAULT))
            for p_edge in self.polygon.edges().segments:
                intersection_point = QPointF()
                if cl_edge.intersect(p_edge, intersection_point):
                    x_min = min(p_edge.x1(), p_edge.x2())
                    x_max = max(p_edge.x1(), p_edge.x2())
                    if x_min <= intersection_point.x() <= x_max:
                        res.addPoint(intersection_point)
                if self.__isPointVisible(p_edge.p2(), cl_edge, center):
                    res.addPoint(p_edge.p2())
            self.clearPolygon()
            self.polygon = res
        self.polygon.draw()
        self.updateImage()
    
    def __isPointVisible(self, point: QPoint, edge: QLineF, center: QPoint) -> bool:
        w = QLineF(edge.p1(), point)
        w_vec = QVector2D(w.dx(), w.dy())
        n = edge.normalVector()
        if 90 < n.angleTo(QLineF(edge.p1(), center)) < 270:
            n_vec = QVector2D(-n.dx(), -n.dy())
        else:
            n_vec = QVector2D(n.dx(), n.dy())
        return QVector2D.dotProduct(w_vec, n_vec) >= 0
 
    def mousePressEvent(self, event: QMouseEvent) -> None:
        cur_point = event.pos()
        if self.rect().contains(cur_point):
            if event.button() == Qt.MouseButton.LeftButton:
                self.polygon.addPoint(cur_point)
            elif event.button() == Qt.MouseButton.RightButton:
                self.clipper.addPoint(cur_point)
            self.updateImage()
