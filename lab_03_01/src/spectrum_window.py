import consts
from algorithms import (
    internal_impl,
    dda_impl,
    bresenham_real_impl,
    bresenham_int_impl,
    bresenham_classic_impl,
    wu_impl,
    rotate,
)
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
from PyQt5.QtCore import QRegExp, QPoint

L_X_CENTER_LOCATION = (2, 0)
LE_X_CENTER_LOCATION = (2, 1, 1, 2)
L_Y_CENTER_LOCATION = (3, 0)
LE_Y_CENTER_LOCATION = (3, 1, 1, 2)
L_STEP_LOCATION = (4, 0)
LE_STEP_LOCATION = (4, 1, 1, 2)
L_LENGTH_LOCATION = (5, 0)
LE_LENGTH_LOCATION = (5, 1, 1, 2)


class SpectrumWindow(QMainWindow):
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
        self.resize(*consts.SCREEN_START_SIZE)
        self.setWindowTitle("Построение спектра")
        self.setMinimumSize(*consts.SCREEN_START_SIZE)
        self.setMaximumSize(*consts.SCREEN_START_SIZE)
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
        validator_int = QRegExpValidator(QRegExp("^[+-]?[0-9][0-9]*$"))
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
            if le == self.le_step:
                le.setValidator(validator_float)
            else:
                le.setValidator(validator_int)

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
        self.pb_print_spectrum = QPushButton("Построить спектр")
        self.pb_edit_color = QPushButton("Изменить цвет")
        self.pb_edit_color.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))
        self.pb_print_spectrum.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
        self.pb_print_spectrum.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.l_build, *consts.L_BUILD_LOCATION)
        self.layout.addWidget(self.cb_build, *consts.CB_BUILD_LOCATION)
        self.layout.addWidget(self.l_line_color, *consts.L_LINE_COLOR_LOCATION)
        self.layout.addWidget(self.l_line_current_color, *consts.L_LINE_CURRENT_COLOR_LOCATION)
        self.layout.addWidget(self.pb_edit_color, *consts.PB_EDIT_COLOR_LOCATION)
        self.layout.addWidget(self.l_x_center, *L_X_CENTER_LOCATION)
        self.layout.addWidget(self.l_y_center, *L_Y_CENTER_LOCATION)
        self.layout.addWidget(self.le_x_center, *LE_X_CENTER_LOCATION)
        self.layout.addWidget(self.le_y_center, *LE_Y_CENTER_LOCATION)
        self.layout.addWidget(self.l_step, *L_STEP_LOCATION)
        self.layout.addWidget(self.l_length, *L_LENGTH_LOCATION)
        self.layout.addWidget(self.le_step, *LE_STEP_LOCATION)
        self.layout.addWidget(self.le_length, *LE_LENGTH_LOCATION)
        self.layout.addWidget(self.pb_print_spectrum, *consts.PB_PRINT_LINE_LOCATION)

    def connecter(self) -> None:
        self.pb_print_spectrum.clicked.connect(self.make_spectrum)
        self.pb_edit_color.clicked.connect(self.edit_color)

    def edit_color(self):
        self.col_dlg.exec()
        self.l_line_current_color.setText(self.col_dlg.currentColor().name())

    def make_spectrum(self) -> None:
        if not self.le_is_valid():
            return
        start_point = QPoint(int(self.le_x_center.text()), int(self.le_y_center.text()))
        end_point = QPoint(start_point + QPoint(0, int(self.le_length.text())))
        step = float(self.le_step.text())
        cur_angle = 0
        while cur_angle < 360:
            rotate(end_point, start_point, step)
            self.algs[self.cb_build.currentText()](
                self.parent.front_img,
                start_point,
                end_point,
                self.col_dlg.currentColor(),
            )
            cur_angle += step
        self.parent.output_foreground()
        self.close()

    def le_is_valid(self) -> bool:
        is_valid = True
        for le in (
            self.le_x_center,
            self.le_y_center,
            self.le_step,
            self.le_length,
        ):
            if (not le.text() or le.text() == consts.FORBIDDEN_STR) and is_valid:
                is_valid = False
                self.msg_box.setWindowTitle("Инфо")
                if le.text():
                    self.msg_box.setText(f'"{consts.FORBIDDEN_STR}" не число')
                else:
                    self.msg_box.setText("Необходимо заполнить все поля")
                self.msg_box.show()
        return is_valid
