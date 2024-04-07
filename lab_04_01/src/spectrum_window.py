import consts
from base_form import BaseForm
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow
from PyQt5.QtCore import QPoint


L_STEP_LOCATION = (5, 0)
LE_STEP_LOCATION = (5, 1, 1, 2)
L_RADIUS_LOCATION = (4, 0)
LE_RADIUS_LOCATION = (4, 1, 1, 2)
L_COUNT_LOCATION = (6, 0)
LE_COUNT_LOCATION = (6, 1, 1, 2)


class SpectrumWindow(BaseForm):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setWindowTitle("Построение спектра концентрических окружностей")

    def ui_line_edits(self) -> None:
        super().ui_line_edits()
        self.le_step = QLineEdit()
        self.le_radius = QLineEdit()
        self.le_count = QLineEdit()
        self.le_list.extend([self.le_step, self.le_radius, self.le_count])
        for le in self.le_list:
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(self.validator_int)

    def ui_labels(self) -> None:
        super().ui_labels()
        self.l_step = QLabel("Шаг: ")
        self.l_radius = QLabel("Начальный радиус: ")
        self.l_count = QLabel("Количество окружностей: ")
        for label in (self.l_step, self.l_radius, self.l_count):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_layout(self) -> None:
        super().ui_layout()
        self.layout.addWidget(self.l_step, *L_STEP_LOCATION)
        self.layout.addWidget(self.le_step, *LE_STEP_LOCATION)
        self.layout.addWidget(self.l_radius, *L_RADIUS_LOCATION)
        self.layout.addWidget(self.le_radius, *LE_RADIUS_LOCATION)
        self.layout.addWidget(self.l_count, *L_COUNT_LOCATION)
        self.layout.addWidget(self.le_count, *LE_COUNT_LOCATION)

    def connecter(self) -> None:
        super().connecter()
        self.pb_print.clicked.connect(self.make_spectrum)

    def make_spectrum(self) -> None:
        if not self.le_is_valid():
            return
        center = QPoint(int(self.le_x_center.text()), int(self.le_y_center.text()))
        cur_radius = int(self.le_radius.text())
        step = int(self.le_step.text())
        for _ in range(int(self.le_count.text())):
            self.algs[self.cb_build.currentText()](
                self.parent.front_img,
                center,
                cur_radius,
                cur_radius,
                self.col_dlg.currentColor(),
            )
            cur_radius += step
        self.parent.output_foreground()
        self.close()
