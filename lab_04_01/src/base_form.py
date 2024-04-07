import consts
from algorithms import (
    internal_impl,
    bresenham_impl,
    canonical_impl,
    parametric_impl,
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
from PyQt5.QtCore import QRegExp

FORBIDDEN_STR = "-"
LINE_COLOR_DEFAULT = "#000000"
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
PB_PRINT_LINE_LOCATION = (7, 0, 1, 3)


class BaseForm(QMainWindow):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__()
        self.parent = parent
        self.algs = {
            "Библиотечный": internal_impl,
            "Параметрическое уравнение": parametric_impl,
            "Алгоритм Брезенхема": bresenham_impl,
            "Каноническое уравнение": canonical_impl,
        }
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(*SCREEN_START_SIZE)
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
        self.col_dlg.setCurrentColor(QColor(LINE_COLOR_DEFAULT))

        self.ui_layout()
        self.connecter()

    def ui_combo_boxes(self) -> None:
        self.cb_build = QComboBox()
        self.cb_build.addItems(self.algs.keys())
        self.cb_build.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_line_edits(self) -> None:
        self.validator_int = QRegExpValidator(QRegExp("^[+-]?[0-9][0-9]*$"))
        self.le_x_center = QLineEdit()
        self.le_y_center = QLineEdit()
        self.le_list = [self.le_x_center, self.le_y_center]
        for le in self.le_list:
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(self.validator_int)

    def ui_labels(self) -> None:
        self.l_build = QLabel("Алгоритм построения:")
        self.l_line_color = QLabel("Цвет линии: ")
        self.l_line_current_color = QLabel(LINE_COLOR_DEFAULT)
        self.l_x_start = QLabel("X центра: ")
        self.l_y_start = QLabel("Y центра: ")
        for label in (
            self.l_build,
            self.l_line_color,
            self.l_line_current_color,
            self.l_x_start,
            self.l_y_start,
        ):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_buttons(self) -> None:
        self.pb_print = QPushButton("Построить")
        self.pb_edit_color = QPushButton("Изменить цвет")
        self.pb_edit_color.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))
        self.pb_print.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.l_build, *L_BUILD_LOCATION)
        self.layout.addWidget(self.cb_build, *CB_BUILD_LOCATION)
        self.layout.addWidget(self.l_line_color, *L_LINE_COLOR_LOCATION)
        self.layout.addWidget(self.l_line_current_color, *L_LINE_CURRENT_COLOR_LOCATION)
        self.layout.addWidget(self.pb_edit_color, *PB_EDIT_COLOR_LOCATION)
        self.layout.addWidget(self.l_x_start, *L_X_START_LOCATION)
        self.layout.addWidget(self.l_y_start, *L_Y_START_LOCATION)
        self.layout.addWidget(self.le_x_center, *LE_X_START_LOCATION)
        self.layout.addWidget(self.le_y_center, *LE_Y_START_LOCATION)
        self.layout.addWidget(self.pb_print, *PB_PRINT_LINE_LOCATION)

    def connecter(self) -> None:
        self.pb_edit_color.clicked.connect(self.edit_color)

    def edit_color(self):
        self.col_dlg.exec()
        self.l_line_current_color.setText(self.col_dlg.currentColor().name())

    # def make_line(self) -> None:
    #     if not self.le_is_valid():
    #         return
    #     start_point = QPoint(int(self.le_x_start.text()), int(self.le_y_start.text()))
    #     end_point = QPoint(int(self.le_x_end.text()), int(self.le_y_end.text()))
    #     self.algs[self.cb_build.currentText()](
    #         self.parent.front_img,
    #         start_point,
    #         end_point,
    #         self.col_dlg.currentColor(),
    #     )
    #     self.parent.output_foreground()
    #     self.close()

    # def make_spectrum(self) -> None:
    #     if not self.le_is_valid():
    #         return
    #     start_point = QPoint(int(self.le_x_center.text()), int(self.le_y_center.text()))
    #     end_point = QPoint(start_point + QPoint(0, int(self.le_length.text())))
    #     step = float(self.le_step.text())
    #     cur_angle = 0
    #     while cur_angle < 360:
    #         rotate(end_point, start_point, step)
    #         self.algs[self.cb_build.currentText()](
    #             self.parent.front_img,
    #             start_point,
    #             end_point,
    #             self.col_dlg.currentColor(),
    #         )
    #         cur_angle += step
    #     self.parent.output_foreground()
    #     self.close()

    def le_is_valid(self) -> bool:
        is_valid = True
        for le in self.le_list:
            if (not le.text() or le.text() == FORBIDDEN_STR) and is_valid:
                is_valid = False
                self.msg_box.setWindowTitle("Инфо")
                if le.text():
                    self.msg_box.setText(f'"{FORBIDDEN_STR}" не число')
                else:
                    self.msg_box.setText("Необходимо заполнить все поля")
                self.msg_box.show()
        return is_valid
