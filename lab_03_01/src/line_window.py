import consts
from algorithms import (
    internal_impl,
    dda_impl,
    bresenham_real_impl,
    bresenham_int_impl,
    bresenham_classic_impl,
    wu_impl,
)
from PyQt5.QtGui import QFont, QRegExpValidator, QColor, QVector2D
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QMessageBox,
    QLineEdit,
    QMainWindow,
    QComboBox,
    QColorDialog,
)
from PyQt5.QtCore import QRegExp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

FORBIDDEN_STR = "-"
SCREEN_START_SIZE = (660, 550)
L_BUILD_LOCATION = (0, 0)
CB_BUILD_LOCATION = (0, 1, 1, 2)
L_LINE_COLOR_LOCATION = (1, 0)
L_LINE_CURRENT_COLOR_LOCATION = (1, 1)
PB_EDIT_COLOR_LOCATION = (1, 2)
L_X_START_LOCATION = (2, 0)
LE_X_START_LOCATION = (2, 1, 1, 2)
L_Y_START_LOCATION = (3, 0)
LE_Y_START_LOCATION = (3, 1, 1, 2)
L_X_END_LOCATION = (4, 0)
LE_X_END_LOCATION = (4, 1, 1, 2)
L_Y_END_LOCATION = (5, 0)
LE_Y_END_LOCATION = (5, 1, 1, 2)
PB_PRINT_LINE_LOCATION = (6, 0, 1, 3)


class LineWindow(QMainWindow):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__()
        self.parent = parent
        self.algs = {
            "Библиотечный": internal_impl,
            "Цифровой дифференциальный анализатор": dda_impl,
            "Алгоритм Брезенхема с действительными данными": bresenham_real_impl,
            "Алгоритм Брезенхема с целочисленными данными": bresenham_int_impl,
            "Алгоритм Брезенхема с устранением ступенчатости": bresenham_classic_impl,
            "Алгоритм Ву": wu_impl,
        }
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Построение отрезка")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.ui_line_edits()
        self.ui_buttons()
        self.ui_labels()
        self.ui_combo_boxes()

        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

        self.col_dlg = QColorDialog(self)
        self.col_dlg.setCurrentColor(QColor(consts.LINE_COLOR_DEFAULT))

        self.ui_layout()
        self.connecter()

    def ui_combo_boxes(self) -> None:
        self.cb_build = QComboBox()
        self.cb_build.addItems(self.algs.keys())
        self.cb_build.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_line_edits(self) -> None:
        validator_float = QRegExpValidator(QRegExp("^[+-]?[0-9][0-9]*[.]?[0-9]*$"))
        self.le_x_start = QLineEdit()
        self.le_y_start = QLineEdit()
        self.le_x_end = QLineEdit()
        self.le_y_end = QLineEdit()
        for le in (
            self.le_x_start,
            self.le_y_start,
            self.le_x_end,
            self.le_y_end,
        ):
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(validator_float)

    def ui_labels(self) -> None:
        self.l_build = QLabel("Алгоритм построения:")
        self.l_line_color = QLabel("Цвет линии: ")
        self.l_line_current_color = QLabel(consts.LINE_COLOR_DEFAULT)
        self.l_x_start = QLabel("X начальное: ")
        self.l_x_end = QLabel("X конечное: ")
        self.l_y_start = QLabel("Y начальное: ")
        self.l_y_end = QLabel("Y конечное: ")
        for label in (
            self.l_build,
            self.l_line_color,
            self.l_line_current_color,
            self.l_x_start,
            self.l_x_end,
            self.l_y_start,
            self.l_y_end,
        ):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_buttons(self) -> None:
        self.pb_print_line = QPushButton("Построить отрезок")
        self.pb_edit_color = QPushButton("Изменить цвет")
        self.pb_edit_color.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))
        self.pb_print_line.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
        self.pb_print_line.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.l_build, *L_BUILD_LOCATION)
        self.layout.addWidget(self.cb_build, *CB_BUILD_LOCATION)
        self.layout.addWidget(self.l_line_color, *L_LINE_COLOR_LOCATION)
        self.layout.addWidget(self.l_line_current_color, *L_LINE_CURRENT_COLOR_LOCATION)
        self.layout.addWidget(self.pb_edit_color, *PB_EDIT_COLOR_LOCATION)
        self.layout.addWidget(self.l_x_start, *L_X_START_LOCATION)
        self.layout.addWidget(self.l_y_start, *L_Y_START_LOCATION)
        self.layout.addWidget(self.le_x_start, *LE_X_START_LOCATION)
        self.layout.addWidget(self.le_y_start, *LE_Y_START_LOCATION)
        self.layout.addWidget(self.l_x_end, *L_X_END_LOCATION)
        self.layout.addWidget(self.l_y_end, *L_Y_END_LOCATION)
        self.layout.addWidget(self.le_x_end, *LE_X_END_LOCATION)
        self.layout.addWidget(self.le_y_end, *LE_Y_END_LOCATION)
        self.layout.addWidget(self.pb_print_line, *PB_PRINT_LINE_LOCATION)

    def connecter(self) -> None:
        self.pb_print_line.clicked.connect(self.make_line)
        self.pb_edit_color.clicked.connect(self.edit_color)

    def edit_color(self):
        self.col_dlg.exec()
        self.l_line_current_color.setText(self.col_dlg.currentColor().name())

    def make_line(self) -> None:
        if not self.le_is_valid():
            return
        start_point = QVector2D(
            float(self.le_x_start.text()), float(self.le_y_start.text())
        )
        end_point = QVector2D(float(self.le_x_end.text()), float(self.le_y_end.text()))
        self.algs[self.cb_build.currentText()](
            self.parent.plot, start_point, end_point, self.col_dlg.currentColor().name()
        )
        self.parent.scene.addWidget(FigureCanvas(self.parent.model))
        self.close()

    def le_is_valid(self) -> bool:
        is_valid = True
        for le in (
            self.le_x_start,
            self.le_y_start,
            self.le_x_end,
            self.le_y_end,
        ):
            if (not le.text() or le.text() == FORBIDDEN_STR) and is_valid:
                is_valid = False
                self.msg_box.setWindowTitle("Инфо")
                if le.text():
                    self.msg_box.setText(f'"{FORBIDDEN_STR}" не число')
                else:
                    self.msg_box.setText("Необходимо заполнить все поля")
                self.msg_box.show()
        return is_valid
