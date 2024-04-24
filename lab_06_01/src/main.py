import consts
from fill import seed_fill
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
    QColorDialog,
)
from PyQt5.QtCore import QSize, QPoint, Qt

SCREEN_START_SIZE = (1250, 950)
FIGURE_SIZE = (1230, 628)
GRAPH_LOCATION = (0, 0)
PB_CLOSE_POLYLINE_LOCATION = (1, 0)
PB_FILL_LOCATION = (2, 0)
PB_SLOW_FILL_LOCATION = (3, 0)
PB_EDIT_BACKGROUND_LOCATION = (4, 0)
PB_RESET_LOCATION = (5, 0)
GRAPH_BORDER = QPoint(10, 33)


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.points = [[]]
        self.base_point = None
        self.fill_color = QColor(*consts.FILL_COLOR_DEFAULT)
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Задача №6")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.col_dlg = QColorDialog(self)
        self.col_dlg.setCurrentColor(QColor(*consts.FILL_COLOR_DEFAULT))

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
        self.pb_close_polyline = QPushButton("Замкнуть текущую ломанную")
        self.pb_fill = QPushButton("Залить")
        self.pb_slow_fill = QPushButton("Залить с задержкой")
        self.pb_edit_background = QPushButton("Изменить цвет заливки")
        self.pb_reset = QPushButton("Очистить экран")
        for pb in (
            self.pb_close_polyline,
            self.pb_fill,
            self.pb_slow_fill,
            self.pb_reset,
            self.pb_edit_background,
        ):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.graph, *GRAPH_LOCATION)
        self.layout.addWidget(self.pb_close_polyline, *PB_CLOSE_POLYLINE_LOCATION)
        self.layout.addWidget(self.pb_fill, *PB_FILL_LOCATION)
        self.layout.addWidget(self.pb_slow_fill, *PB_SLOW_FILL_LOCATION)
        self.layout.addWidget(self.pb_edit_background, *PB_EDIT_BACKGROUND_LOCATION)
        self.layout.addWidget(self.pb_reset, *PB_RESET_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.show_about)
        self.task.triggered.connect(self.show_task)
        self.instruction.triggered.connect(self.show_instruction)
        self.pb_close_polyline.clicked.connect(self.close_polyline)
        self.pb_fill.clicked.connect(self.fill_polygon)
        self.pb_slow_fill.clicked.connect(self.slow_fill_polygon)
        self.pb_edit_background.clicked.connect(self.edit_fill_color)
        self.pb_reset.clicked.connect(self.reset)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.graph.rect().contains(event.pos() - GRAPH_BORDER):
            if event.button() == Qt.MouseButton.LeftButton:
                self.points[-1].append(event.pos() - GRAPH_BORDER)
                self.front_img.setPixel(
                    self.points[-1][-1], QColor(*consts.LINE_COLOR_DEFAULT).rgba()
                )
                if len(self.points[-1]) > 1:
                    self.print_line(self.points[-1][-2], self.points[-1][-1])
            elif event.button() == Qt.MouseButton.RightButton:
                if self.base_point:
                    self.front_img.setPixel(
                        self.base_point, QColor(*consts.BACK_COLOR_DEFAULT).rgba()
                    )
                self.base_point = event.pos() - GRAPH_BORDER
                self.front_img.setPixel(self.base_point, self.fill_color.rgba())
            self.output_foreground()

    def fill_polygon(self) -> None:
        if not self.base_point_is_ok():
            return
        if self.points[0] and not self.points[-1] or self.close_polyline():
            seed_fill(
                self.front_img, self.base_point, self.fill_color, self.output_foreground
            )

    def slow_fill_polygon(self) -> None:
        if not self.base_point_is_ok():
            return
        if self.points[0] and not self.points[-1] or self.close_polyline():
            seed_fill(
                self.front_img,
                self.base_point,
                self.fill_color,
                self.output_foreground,
                consts.DELAY,
            )

    def base_point_is_ok(self) -> bool:
        is_ok = True
        if not self.base_point:
            self.msg_box.setWindowTitle("Ничего не получится")
            self.msg_box.setText(
                "Чтобы залить многоугольник, необходимо отметить затравочную точку.\n"
                + "(точка, которая лежит внутри многоугольника).\n"
                + "Нажмите на полотно правой кнопкой мыши, чтобы отметить такую точку"
            )
            self.msg_box.show()
            is_ok = False
        return is_ok

    def print_line(self, a: QPoint, b: QPoint) -> None:
        painter = QPainter(self.front_img)
        painter.setPen(QColor(*consts.LINE_COLOR_DEFAULT))
        painter.drawLine(a.x(), a.y(), b.x(), b.y())
        painter.end()

    def reset(self) -> None:
        self.points = [[]]
        self.scene.clear()
        self.front_img.fill(QColor(*consts.BACK_COLOR_DEFAULT))

    def close_polyline(self) -> bool:
        rc = False
        if len(self.points[-1]) < 3:
            self.msg_box.setWindowTitle("Ничего не получится")
            self.msg_box.setText(
                "Чтобы получить многоугольник, необходимо поставить как минимум 3 вершины на экране.\n"
                + "Нажмите на полотно левой кнопкой мыши, чтобы добавить вершину"
            )
            self.msg_box.show()
        else:
            self.print_line(self.points[-1][0], self.points[-1][-1])
            self.points.append([])
            self.output_foreground()
            rc = True
        return rc

    def edit_fill_color(self) -> None:
        self.col_dlg.exec()
        if self.col_dlg.currentColor() != consts.LINE_COLOR_DEFAULT:
            self.fill_color = self.col_dlg.currentColor()
        else:
            self.msg_box.setWindowTitle("Ничего не получится")
            self.msg_box.setText("Цвет заливки должен отличаться от цвета границ")
            self.msg_box.show()

    def output_foreground(self, is_slow: bool = False) -> None:
        self.scene.clear()
        self.front_pix.convertFromImage(self.front_img)
        self.scene.addPixmap(self.front_pix)
        if is_slow:
            QApplication.processEvents()

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
        self.msg_box.setText("Реализация алгоритма построчного затравочного заполнения")
        self.msg_box.show()

    def show_instruction(self) -> None:
        self.msg_box.setWindowTitle("Помощь")
        self.msg_box.setText(
            "Нажмите на полотно левой кнопкой мыши, чтобы поставить вершину.\n"
            + "Вершины последовательно соединяются рёбрами (в порядке, в котором Вы их вводите).\n"
            + "Когда Вы добавили все вершины многоугольника, нажмите на кнопку"
            + ' "Замкнуть текущую ломанную".\n'
            + "Чтобы поставить затравочную точку надо нажать на полотно правой кнопкой мыши."
        )
        self.msg_box.show()


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())
