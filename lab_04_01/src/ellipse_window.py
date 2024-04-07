import consts
from base_form import BaseForm
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow
from PyQt5.QtCore import QPoint


L_OY_LEN_LOCATION = (5, 0)
LE_OY_LEN_LOCATION = (5, 1, 1, 2)
L_OX_LEN_LOCATION = (4, 0)
LE_OX_LEN_LOCATION = (4, 1, 1, 2)
L_COUNT_LOCATION = (6, 0)
LE_COUNT_LOCATION = (6, 1, 1, 2)


class EllipseWindow(BaseForm):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setWindowTitle("Построение эллипса")

    def ui_line_edits(self) -> None:
        super().ui_line_edits()
        self.le_ox_len = QLineEdit()
        self.le_oy_len = QLineEdit()
        self.le_list.extend([self.le_ox_len, self.le_oy_len])
        for le in self.le_list:
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(self.validator_int)

    def ui_labels(self) -> None:
        super().ui_labels()
        self.l_ox_len = QLabel("Длина полуоси OX: ")
        self.l_oy_len = QLabel("Длина полуоси OY: ")
        for label in (self.l_ox_len, self.l_oy_len):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_layout(self) -> None:
        super().ui_layout()
        self.layout.addWidget(self.l_ox_len, *L_OX_LEN_LOCATION)
        self.layout.addWidget(self.le_ox_len, *LE_OX_LEN_LOCATION)
        self.layout.addWidget(self.l_oy_len, *L_OY_LEN_LOCATION)
        self.layout.addWidget(self.le_oy_len, *LE_OY_LEN_LOCATION)

    def connecter(self) -> None:
        super().connecter()
        self.pb_print.clicked.connect(self.make_ellipse)

    def make_ellipse(self) -> None:
        if not self.le_is_valid():
            return
        center = QPoint(int(self.le_x_center.text()), int(self.le_y_center.text()))
        self.algs[self.cb_build.currentText()](
            self.parent.front_img,
            center,
            int(self.le_ox_len.text()),
            int(self.le_oy_len.text()),
            self.col_dlg.currentColor(),
        )
        self.parent.output_foreground()
        self.close()
