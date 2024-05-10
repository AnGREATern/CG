import consts
from canvas import Canvas
from sys import argv
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QMenuBar,
    QMainWindow,
    QAction,
)

SCREEN_START_SIZE = (1250, 950)
CANVAS_LOCATION = (0, 0)
PB_CLIP_LOCATION = (1, 0)
PB_CLOSE_POLYGON_LOCATION = (2, 0)
PB_CLEAR_SEGMENTS_LOCATION = (3, 0)
PB_CLEAR_POLYGON_LOCATION = (4, 0)
PB_CLEAR_ALL_LOCATION = (5, 0)


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUi()

    def initUi(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Задача №8")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.canvas = Canvas()
        self.uiButtons()
        self.uiMenuBar()
        self.uiMessageBox()

        self.uiLayout()
        self.connecter()

    def uiMessageBox(self) -> None:
        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def uiMenuBar(self) -> None:
        self.mb = QMenuBar(self)
        self.setMenuBar(self.mb)

        self.info = self.mb.addMenu("Информация")
        self.about = QAction("Об авторе", self)
        self.task = QAction("Условие задачи", self)
        self.instruction = QAction("Инструкция", self)
        self.info.addAction(self.about)
        self.info.addAction(self.task)
        self.info.addAction(self.instruction)

    def uiButtons(self) -> None:
        self.pb_clip = QPushButton("Отсечь отрезки")
        self.pb_close_polygon = QPushButton("Замкнуть многоугольник")
        self.pb_clear_segments = QPushButton("Очистить отрезки")
        self.pb_clear_polygon = QPushButton("Очистить многоугольник")
        self.pb_clear_all = QPushButton("Очистить экран")
        for pb in (
            self.pb_clip,
            self.pb_close_polygon,
            self.pb_clear_segments,
            self.pb_clear_polygon,
            self.pb_clear_all,
        ):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def uiLayout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.canvas, *CANVAS_LOCATION)
        self.layout.addWidget(self.pb_clip, *PB_CLIP_LOCATION)
        self.layout.addWidget(self.pb_close_polygon, *PB_CLOSE_POLYGON_LOCATION)
        self.layout.addWidget(self.pb_clear_segments, *PB_CLEAR_SEGMENTS_LOCATION)
        self.layout.addWidget(self.pb_clear_polygon, *PB_CLEAR_POLYGON_LOCATION)
        self.layout.addWidget(self.pb_clear_all, *PB_CLEAR_ALL_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.showAbout)
        self.task.triggered.connect(self.showTask)
        self.instruction.triggered.connect(self.showInstruction)
        self.pb_clip.clicked.connect(self.canvas.clipSegments)
        self.pb_close_polygon.clicked.connect(self.canvas.closePolygon)
        self.pb_clear_segments.clicked.connect(self.canvas.clearSegments)
        self.pb_clear_polygon.clicked.connect(self.canvas.clearPolygon)
        self.pb_clear_all.clicked.connect(self.canvas.clearAll)

    def savePicture(self, filename: str) -> None:
        self.canvas.saveImage(filename)

    def showAbout(self) -> None:
        self.msg_box.setWindowTitle("Об авторе")
        self.msg_box.setText("Выполнил Романов Владислав\nГруппа ИУ7-45Б")
        self.msg_box.show()

    def showTask(self) -> None:
        self.msg_box.setWindowTitle("Условие задачи")
        self.msg_box.setText(
            "Реализация алгоритма отсечения отрезка произвольным выпуклым отсекателем"
        )
        self.msg_box.show()

    def showInstruction(self) -> None:
        self.msg_box.setWindowTitle("Помощь")
        self.msg_box.setText(
            "Концы отрезков задаются нажатием левой кнопки мыши.\n"
            + "Вершины многоугольника задаются нажатием на правую кнопку мыши.\n"
        )
        self.msg_box.show()


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())
