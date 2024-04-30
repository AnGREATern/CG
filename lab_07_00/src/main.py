import consts
from clipping import clip
from sys import argv
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QMenuBar,
    QMainWindow,
    QAction,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5.QtCore import QSize, QPoint, Qt, QLine, QRect

SCREEN_START_SIZE = (1250, 950)
FIGURE_SIZE = (1230, 796)
GRAPH_LOCATION = (0, 0)
PB_CLIP_SEGMENT_LOCATION = (1, 0)
PB_RESET_LOCATION = (2, 0)
GRAPH_BORDER = QPoint(10, 33)
RECT_NULL_POINT = QPoint(-1, -1)


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_figures()
        self.init_ui()

    def init_figures(self) -> None:
        self.segment = QLine()
        self.rectangle = QRect()
        self.rectangle.setTopLeft(RECT_NULL_POINT)
        self.rectangle.setBottomRight(RECT_NULL_POINT)

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Задача №7")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.ui_graph()
        self.ui_buttons()
        self.ui_menu_bar()

        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

        self.ui_layout()
        self.connecter()

    def ui_graph(self) -> None:
        self.scene = QGraphicsScene()
        self.graph = QGraphicsView(self.scene)
        self.front_pix = QPixmap(QSize(*FIGURE_SIZE))
        self.front_img = QImage(QSize(*FIGURE_SIZE), QImage.Format_ARGB32)
        self.front_pix.convertFromImage(self.front_img)
        self.reset()

    def ui_menu_bar(self) -> None:
        self.mb = QMenuBar(self)
        self.setMenuBar(self.mb)

        self.info = self.mb.addMenu("Информация")
        self.about = QAction("Об авторе", self)
        self.task = QAction("Условие задачи", self)
        self.instruction = QAction("Инструкция", self)
        self.info.addAction(self.about)
        self.info.addAction(self.task)
        self.info.addAction(self.instruction)

    def ui_buttons(self) -> None:
        self.pb_clip_segment = QPushButton("Отсечь отрезок")
        self.pb_reset = QPushButton("Очистить экран")
        for pb in (self.pb_clip_segment, self.pb_reset):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.graph, *GRAPH_LOCATION)
        self.layout.addWidget(self.pb_clip_segment, *PB_CLIP_SEGMENT_LOCATION)
        self.layout.addWidget(self.pb_reset, *PB_RESET_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.show_about)
        self.task.triggered.connect(self.show_task)
        self.instruction.triggered.connect(self.show_instruction)
        self.pb_clip_segment.clicked.connect(self.clip_segment)
        self.pb_reset.clicked.connect(self.reset)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        cur_point = event.pos() - GRAPH_BORDER
        if self.graph.rect().contains(cur_point):
            if event.button() == Qt.MouseButton.LeftButton:
                if not self.segment.p1():
                    self.segment.setP1(cur_point)
                elif not self.segment.p2():
                    self.segment.setP2(cur_point)
                    self.print_figure(self.segment)
                else:
                    self.reset(True)
                    self.segment.setP1(cur_point)
                    self.segment.setP2(QPoint())
                    self.print_figure(self.rectangle)
            elif event.button() == Qt.MouseButton.RightButton:
                if self.rectangle.topLeft() == RECT_NULL_POINT:
                    self.rectangle.setTopLeft(cur_point)
                elif (
                    self.rectangle.bottomRight() == RECT_NULL_POINT
                    and self.rectangle.topLeft() != cur_point
                ):
                    self.rectangle.setBottomRight(cur_point)
                    self.print_figure(self.rectangle)
                elif self.rectangle.topLeft() != cur_point:
                    self.reset(True)
                    self.rectangle.setTopLeft(cur_point)
                    self.rectangle.setBottomRight(RECT_NULL_POINT)
                    self.print_figure(self.segment)
            self.front_img.setPixel(
                cur_point, QColor(*consts.LINE_COLOR_DEFAULT).rgba()
            )
            self.output_foreground()

    def clip_segment(self) -> None:
        if self.rectangle.bottomRight() == RECT_NULL_POINT or not self.segment.p2():
            self.msg_box.setWindowTitle("Это никуда не годится")
            if self.rectangle.bottomRight() == RECT_NULL_POINT:
                self.msg_box.setText("Вы не закончили ввод прямоугольной области")
            else:
                self.msg_box.setText("Вы не закончили ввод отрезка")
            self.msg_box.show()
        else:
            self.reset(True)
            clip(self.print_figure, QLine(self.segment), self.rectangle)
            self.print_figure(self.rectangle)
            self.output_foreground()

    def print_figure(self, figure: QLine | QRect) -> None:
        painter = QPainter(self.front_img)
        painter.setPen(QColor(*consts.LINE_COLOR_DEFAULT))
        if isinstance(figure, QLine):
            painter.drawLine(figure)
        elif isinstance(figure, QRect):
            painter.drawRect(figure)
        painter.end()

    def reset(self, is_not_clear_figures: bool = False) -> None:
        if not is_not_clear_figures:
            self.init_figures()
        self.scene.clear()
        self.front_img.fill(QColor(*consts.BACK_COLOR_DEFAULT))

    def output_foreground(self) -> None:
        self.scene.clear()
        self.front_pix.convertFromImage(self.front_img)
        self.scene.addPixmap(self.front_pix)

    def draw_picture(self, filename: str) -> None:
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(filename + ".png")

    def show_about(self) -> None:
        self.msg_box.setWindowTitle("Об авторе")
        self.msg_box.setText("Выполнил Романов Владислав\nГруппа ИУ7-45Б")
        self.msg_box.show()

    def show_task(self) -> None:
        self.msg_box.setWindowTitle("Условие задачи")
        self.msg_box.setText(
            "Реализация алгоритма отсечения отрезка методом средней точки"
        )
        self.msg_box.show()

    def show_instruction(self) -> None:
        self.msg_box.setWindowTitle("Помощь")
        self.msg_box.setText(
            "Отрезок задаётся нажатием левой кнопки мыши, прямоугольник задаётся нажатием "
            + "на правую кнопку мыши.\n"
        )
        self.msg_box.show()


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())
