import consts
from line_window import LineWindow
from spectrum_window import SpectrumWindow
from sys import argv
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter
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
from PyQt5.QtCore import QSize

SCREEN_START_SIZE = (1200, 850)
FIGURE_SIZE = (1180, 584)
GRAPH_LOCATION = (0, 0)
PB_PRINT_SPECTRUM_LOCATION = (7, 0)
PB_PRINT_LINE_LOCATION = (8, 0)
PB_EDIT_BACKGROUND_LOCATION = (9, 0)
PB_RESET_LOCATION = (10, 0)


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Задача №3")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.col_dlg = QColorDialog(self)
        self.col_dlg.setCurrentColor(QColor(*consts.BACK_COLOR_DEFAULT))

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
        self.back_pix = QPixmap(QSize(*FIGURE_SIZE))
        self.front_pix = QPixmap(QSize(*FIGURE_SIZE))
        self.back_img = QImage(QSize(*FIGURE_SIZE), QImage.Format_ARGB32)
        self.back_img.fill(QColor(*consts.BACK_COLOR_DEFAULT))
        self.back_pix.convertFromImage(self.back_img)
        self.front_img = QImage(QSize(*FIGURE_SIZE), QImage.Format_ARGB32)
        self.front_img.fill(QColor(*consts.FRONT_COLOR_DEFAULT))
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

        self.analysis = self.mb.addMenu("Графики")
        self.time_comp = QAction("Сравнение времени работы", self)
        self.stepwise_comp = QAction("Сравнение ступенчатости", self)
        self.analysis.addAction(self.time_comp)
        self.analysis.addAction(self.stepwise_comp)

    def ui_buttons(self) -> None:
        self.pb_print_spectrum = QPushButton("Построить спектр")
        self.pb_print_line = QPushButton("Построить отрезок")
        self.pb_edit_background = QPushButton("Изменить фон")
        self.pb_reset = QPushButton("Очистить экран")
        for pb in (
            self.pb_print_spectrum,
            self.pb_print_line,
            self.pb_reset,
            self.pb_edit_background,
        ):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.graph, *GRAPH_LOCATION)
        self.layout.addWidget(self.pb_print_spectrum, *PB_PRINT_SPECTRUM_LOCATION)
        self.layout.addWidget(self.pb_print_line, *PB_PRINT_LINE_LOCATION)
        self.layout.addWidget(self.pb_edit_background, *PB_EDIT_BACKGROUND_LOCATION)
        self.layout.addWidget(self.pb_reset, *PB_RESET_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.show_about)
        self.task.triggered.connect(self.show_task)
        self.instruction.triggered.connect(self.show_instruction)
        self.pb_print_spectrum.clicked.connect(self.open_spectrum_window)
        self.pb_print_line.clicked.connect(self.open_line_window)
        self.pb_edit_background.clicked.connect(self.edit_background_color)
        self.pb_reset.clicked.connect(self.reset)

    def reset(self) -> None:
        self.scene.clear()
        self.front_img.fill(QColor(*consts.FRONT_COLOR_DEFAULT))
        self.scene.addPixmap(self.back_pix)

    def open_spectrum_window(self) -> None:
        self.sw = SpectrumWindow(self)
        self.sw.show()

    def open_line_window(self) -> None:
        self.lw = LineWindow(self)
        self.lw.show()

    def edit_background_color(self) -> None:
        self.col_dlg.exec()
        self.back_img.fill(self.col_dlg.currentColor())
        self.back_pix.convertFromImage(self.back_img)
        self.scene.addPixmap(self.back_pix)
        self.scene.addPixmap(self.front_pix)

    def output_foreground(self) -> None:
        self.scene.clear()
        self.scene.addPixmap(self.back_pix)
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
        self.msg_box.setText("Реализация и исследование алгоритмов построения отрезков")
        self.msg_box.show()

    def show_instruction(self) -> None:
        self.msg_box.setWindowTitle("Помощь")
        self.msg_box.setText(
            "Для выполнения преобразований необходимо задать параметры вещественными числами"
            + "(если не задать какой-либо параметр, то будет использовано нейтральное значение)"
            + 'и нажать на кнопку "Построить решение".\n\n'
            + 'Для возврата к исходной фигуре необходимо нажать на кнопку "Сбросить всё"'
        )
        self.msg_box.show()


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())
