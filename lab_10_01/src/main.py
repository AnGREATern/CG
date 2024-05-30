import consts
from canvas import Canvas
from sys import argv
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QMenuBar,
    QMainWindow,
    QAction,
    QLabel,
    QComboBox,
    QLineEdit,
)
from PyQt5.QtCore import QRegExp

SCREEN_START_SIZE = (1550, 950)

CANVAS_LOCATION = (0, 0, 10, 1)
L_FUNC_LOCATION = (0, 1)
CB_FUNC_LOCATION = (0, 2, 1, 2)
L_X_LOCATION = (1, 2)
L_Z_LOCATION = (1, 3)
L_FROM_LOCATION = (2, 1)
LE_X_FROM_LOCATION = (2, 2)
LE_Z_FROM_LOCATION = (2, 3)
L_TO_LOCATION = (3, 1)
LE_X_TO_LOCATION = (3, 2)
LE_Z_TO_LOCATION = (3, 3)
L_STEP_LOCATION = (4, 1)
LE_X_STEP_LOCATION = (4, 2)
LE_Z_STEP_LOCATION = (4, 3)
L_ROTATE_LOCATION = (8, 1)
CB_AXIS_LOCATION = (8, 2, 1, 2)
L_PHI_LOCATION = (9, 1)
LE_PHI_LOCATION = (9, 2, 1, 2)
PB_BUILD_LOCATION = (10, 0, 1, 4)
PB_CLEAR_ALL_LOCATION = (11, 0, 1, 4)

OX = 0
OY = 1
OZ = 2

FORBIDDEN_STR = "-"


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUi()

    def initUi(self) -> None:
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Задача №10")
        self.setMinimumSize(*SCREEN_START_SIZE)
        self.setMaximumSize(*SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.validator_int = QRegExpValidator(QRegExp("^[+-]?[0-9][0-9]*$"))

        self.canvas = Canvas()
        self.uiButtons()
        self.uiMenuBar()
        self.uiMessageBox()
        self.uiLabels()
        self.uiComboBoxes()
        self.uiLineEdits()

        self.uiLayout()
        self.connecter()

    def uiLineEdits(self) -> None:
        self.le_x_from = QLineEdit()
        self.le_x_to = QLineEdit()
        self.le_x_step = QLineEdit()
        self.le_z_from = QLineEdit()
        self.le_z_to = QLineEdit()
        self.le_z_step = QLineEdit()
        self.le_phi = QLineEdit()
        self.build_le = (
            self.le_x_from,
            self.le_x_to,
            self.le_x_step,
            self.le_z_from,
            self.le_z_to,
            self.le_z_step,
        )
        for le in (*self.build_le, self.le_phi):
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(self.validator_int)

    def uiLabels(self) -> None:
        self.l_rotate = QLabel("Поворот по оси:")
        self.l_x = QLabel("X:")
        self.l_z = QLabel("Z:")
        self.l_from = QLabel("От:")
        self.l_to = QLabel("До:")
        self.l_step = QLabel("Шаг:")
        self.l_func = QLabel("Уравнение:\ty =")
        self.l_phi = QLabel("φ (°):")
        for label in (
            self.l_rotate,
            self.l_x,
            self.l_z,
            self.l_from,
            self.l_to,
            self.l_step,
            self.l_func,
            self.l_phi,
        ):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def uiComboBoxes(self) -> None:
        self.cb_axis = QComboBox()
        self.cb_axis.addItems(("X", "Y", "Z"))
        self.cb_func = QComboBox()
        self.cb_func.addItems(consts.FUNCS)
        for cb in (self.cb_axis, self.cb_func):
            cb.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

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
        self.pb_build = QPushButton("Построить поверхность")
        self.pb_clear_all = QPushButton("Очистить экран")
        for pb in (
            self.pb_build,
            self.pb_clear_all,
        ):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def uiLayout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.canvas, *CANVAS_LOCATION)
        self.layout.addWidget(self.l_func, *L_FUNC_LOCATION)
        self.layout.addWidget(self.cb_func, *CB_FUNC_LOCATION)
        self.layout.addWidget(self.l_x, *L_X_LOCATION)
        self.layout.addWidget(self.l_z, *L_Z_LOCATION)
        self.layout.addWidget(self.l_from, *L_FROM_LOCATION)
        self.layout.addWidget(self.le_x_from, *LE_X_FROM_LOCATION)
        self.layout.addWidget(self.le_z_from, *LE_Z_FROM_LOCATION)
        self.layout.addWidget(self.l_to, *L_TO_LOCATION)
        self.layout.addWidget(self.le_x_to, *LE_X_TO_LOCATION)
        self.layout.addWidget(self.le_z_to, *LE_Z_TO_LOCATION)
        self.layout.addWidget(self.l_step, *L_STEP_LOCATION)
        self.layout.addWidget(self.le_x_step, *LE_X_STEP_LOCATION)
        self.layout.addWidget(self.le_z_step, *LE_Z_STEP_LOCATION)
        self.layout.addWidget(self.l_rotate, *L_ROTATE_LOCATION)
        self.layout.addWidget(self.cb_axis, *CB_AXIS_LOCATION)
        self.layout.addWidget(self.l_phi, *L_PHI_LOCATION)
        self.layout.addWidget(self.le_phi, *LE_PHI_LOCATION)
        self.layout.addWidget(self.pb_build, *PB_BUILD_LOCATION)
        self.layout.addWidget(self.pb_clear_all, *PB_CLEAR_ALL_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.showAbout)
        self.task.triggered.connect(self.showTask)
        self.instruction.triggered.connect(self.showInstruction)
        self.pb_build.clicked.connect(self.buildFigure)
        self.pb_clear_all.clicked.connect(self.canvas.clearAll)

    def buildFigure(self) -> None:
        if self.isLeValid(self.build_le):
            self.canvas.clearAll()
            x_range = range(
                int(self.le_x_from.text()),
                int(self.le_x_to.text()) + 1,
                int(self.le_x_step.text()),
            )
            z_range = range(
                int(self.le_z_to.text()),
                int(self.le_z_from.text()),
                -int(self.le_z_step.text()),
            )
            phi = 0
            if self.isLeValid([self.le_phi], False):
                phi = int(self.le_phi.text())
            axis = OZ
            if self.cb_axis.currentText() == "OX":
                axis = OX
            elif self.cb_axis.currentText() == "OY":
                axis = OY
            self.canvas.buildFigure(
                x_range,
                z_range,
                self.cb_func.currentText(),
                axis,
                phi
            )

    def savePicture(self, filename: str) -> None:
        self.canvas.saveImage(filename)

    def isLeValid(self, le: tuple[QLineEdit], is_verbose: bool = True) -> bool:
        is_valid = True
        for cur_le in le:
            if (not cur_le.text() or cur_le.text() == FORBIDDEN_STR) and is_valid:
                is_valid = False
                if is_verbose:
                    self.msg_box.setWindowTitle("Инфо")
                    if cur_le.text():
                        self.msg_box.setText(f'"{FORBIDDEN_STR}" не число')
                    else:
                        self.msg_box.setText("Необходимо заполнить все поля")
                    self.msg_box.show()
        return is_valid

    def showAbout(self) -> None:
        self.msg_box.setWindowTitle("Об авторе")
        self.msg_box.setText("Выполнил Романов Владислав\nГруппа ИУ7-45Б")
        self.msg_box.show()

    def showTask(self) -> None:
        self.msg_box.setWindowTitle("Условие задачи")
        self.msg_box.setText(
            "Реализация алгоритма плавающего горизонта построение трёхмерных поверхностей"
        )
        self.msg_box.show()

    def showInstruction(self) -> None:
        self.msg_box.setWindowTitle("Помощь")
        self.msg_box.setText(
            "Для поворота задайте угол, выберите ось и нажмите на кнопку 'Повернуть поверхность'.\n"
        )
        self.msg_box.show()


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    window.show()
    exit(app.exec_())
