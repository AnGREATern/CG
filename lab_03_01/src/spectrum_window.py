import consts
from PyQt5.QtGui import QFont, QRegExpValidator, QColor
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

SCREEN_START_SIZE = (660, 550)
L_BUILD_LOCATION = (0, 0)
CB_BUILD_LOCATION = (0, 1, 1, 2)
L_LINE_COLOR_LOCATION = (1, 0)
L_LINE_CURRENT_COLOR_LOCATION = (1, 1)
PB_EDIT_COLOR_LOCATION = (1, 2)
L_X_CENTER_LOCATION = (2, 0)
LE_X_CENTER_LOCATION = (2, 1, 1, 2)
L_Y_CENTER_LOCATION = (3, 0)
LE_Y_CENTER_LOCATION = (3, 1, 1, 2)
L_STEP_LOCATION = (4, 0)
LE_STEP_LOCATION = (4, 1, 1, 2)
L_LENGTH_LOCATION = (5, 0)
LE_LENGTH_LOCATION = (5, 1, 1, 2)
PB_PRINT_LINE_LOCATION = (6, 0, 1, 3)


class SpectrumWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Построение спектра")
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
        self.cb_build.addItems(
            (
                "Библиотечный",
                "Цифровой дифференциальный анализатор",
                "Алгоритм Брезенхема с действительными данными",
                "Алгоритм Брезенхема с целочисленными данными",
                "Алгоритм Брезенхема с устранением ступенчатости",
                "Алгоритм Ву",
            )
        )
        self.cb_build.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_line_edits(self) -> None:
        validator_float = QRegExpValidator(QRegExp("^[+-]?[0-9][0-9]*[.]?[0-9]*$"))
        self.le_x_center = QLineEdit()
        self.le_y_center = QLineEdit()
        self.le_step = QLineEdit()
        self.le_length = QLineEdit()
        for le in (
            self.le_x_center,
            self.le_y_center,
            self.le_step,
            self.le_length,
        ):
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(validator_float)

    def ui_labels(self) -> None:
        self.l_build = QLabel("Алгоритм построения:")
        self.l_line_color = QLabel("Цвет линий: ")
        self.l_line_current_color = QLabel(consts.LINE_COLOR_DEFAULT)
        self.l_x_center = QLabel("X центра: ")
        self.l_step = QLabel("Шаг (°): ")
        self.l_y_center = QLabel("Y центра: ")
        self.l_length = QLabel("Длина линии: ")
        for label in (
            self.l_build,
            self.l_line_color,
            self.l_line_current_color,
            self.l_x_center,
            self.l_step,
            self.l_y_center,
            self.l_length,
        ):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_buttons(self) -> None:
        self.pb_print_line = QPushButton("Построить спектр")
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
        self.layout.addWidget(self.l_x_center, *L_X_CENTER_LOCATION)
        self.layout.addWidget(self.l_y_center, *L_Y_CENTER_LOCATION)
        self.layout.addWidget(self.le_x_center, *LE_X_CENTER_LOCATION)
        self.layout.addWidget(self.le_y_center, *LE_Y_CENTER_LOCATION)
        self.layout.addWidget(self.l_step, *L_STEP_LOCATION)
        self.layout.addWidget(self.l_length, *L_LENGTH_LOCATION)
        self.layout.addWidget(self.le_step, *LE_STEP_LOCATION)
        self.layout.addWidget(self.le_length, *LE_LENGTH_LOCATION)
        self.layout.addWidget(self.pb_print_line, *PB_PRINT_LINE_LOCATION)

    def connecter(self) -> None:
        self.pb_edit_color.clicked.connect(self.edit_color)

    def edit_color(self):
        self.col_dlg.exec()
        self.l_line_current_color.setText(self.col_dlg.currentColor().name())
