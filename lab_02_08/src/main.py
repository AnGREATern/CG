import consts
from sys import argv
from PyQt5.QtGui import QFont, QRegExpValidator, QVector2D
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QMessageBox, \
    QLineEdit, QMenuBar, QMainWindow, QAction, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRegExp
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Ellipse
from grasshopper import Grasshopper
from math import acos, degrees

OX = QVector2D(1, 0)
NEUTRAL_MOVE = 0
NEUTRAL_SCALE = 1
FORBIDDEN_STR = "-"

class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.reset()

    def init_ui(self) -> None:
        self.resize(*consts.SCREEN_START_SIZE)
        self.setWindowTitle('Задача №2')
        self.setMinimumSize(*consts.SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.ui_line_edits()
        self.ui_graph()
        self.ui_buttons()
        self.ui_menu_bar()
        self.ui_labels()

        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

        self.ui_layout()
        self.connecter()  

    def ui_labels(self) -> None:
        self.l_center = QLabel("Центр преобразования:")
        self.l_scale = QLabel("Масштабирование:")
        self.l_move = QLabel("Перемещение:")
        self.l_rotate = QLabel("Поворот:")
        self.l_x = QLabel("X:")
        self.l_y = QLabel("Y:")
        self.l_kx = QLabel("kX:")
        self.l_ky = QLabel("kY:")
        self.l_dx = QLabel("dX:")
        self.l_dy = QLabel("dY:")
        self.l_phi = QLabel("φ (°):")
        for label in (self.l_center, self.l_scale, self.l_move, self.l_rotate, self.l_x, 
                      self.l_y, self.l_kx, self.l_ky, self.l_dx, self.l_dy, self.l_phi):
            label.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

    def ui_graph(self) -> None:
        self.graph = QGraphicsView()
        self.graph.setMinimumWidth(consts.GRAPH_MINIMUM_WIDTH)
        self.scene = QGraphicsScene()
        self.graph.setScene(self.scene)
        self.model = Figure()

    def ui_line_edits(self) -> None:
        validator_float = QRegExpValidator(QRegExp('^[+-]?[0-9][0-9]*[.]?[0-9]*$'))
        self.le_x = QLineEdit()
        self.le_y = QLineEdit()
        self.le_kx = QLineEdit()
        self.le_ky = QLineEdit()
        self.le_dx = QLineEdit()
        self.le_dy = QLineEdit()
        self.le_phi = QLineEdit()
        for le in (self.le_x, self.le_y, self.le_kx, self.le_ky, self.le_dx, self.le_dy, self.le_phi):
            le.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))
            le.setValidator(validator_float)

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
        self.pb_run = QPushButton("Построить решение")
        self.pb_reset = QPushButton("Сбросить всё")
        for pb in (self.pb_run, self.pb_reset):
            pb.setMinimumHeight(consts.BIG_ELEM_MINIMUM_SIZE)
            pb.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

    def ui_layout(self) -> None:
        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.graph, *consts.MAIN_WINDOW_GRAPH_LOCATION)
        self.layout.addWidget(self.l_center, *consts.MAIN_WINDOW_L_CENTER_LOCATION)
        self.layout.addWidget(self.l_x, *consts.MAIN_WINDOW_L_X_LOCATION)
        self.layout.addWidget(self.le_x, *consts.MAIN_WINDOW_LE_X_LOCATION)
        self.layout.addWidget(self.l_y, *consts.MAIN_WINDOW_L_Y_LOCATION)
        self.layout.addWidget(self.le_y, *consts.MAIN_WINDOW_LE_Y_LOCATION)
        self.layout.addWidget(self.l_scale, *consts.MAIN_WINDOW_L_SCALE_LOCATION)
        self.layout.addWidget(self.l_kx, *consts.MAIN_WINDOW_L_KX_LOCATION)
        self.layout.addWidget(self.le_kx, *consts.MAIN_WINDOW_LE_KX_LOCATION)
        self.layout.addWidget(self.l_ky, *consts.MAIN_WINDOW_L_KY_LOCATION)
        self.layout.addWidget(self.le_ky, *consts.MAIN_WINDOW_LE_KY_LOCATION)
        self.layout.addWidget(self.l_move, *consts.MAIN_WINDOW_L_MOVE_LOCATION)
        self.layout.addWidget(self.l_dx, *consts.MAIN_WINDOW_L_DX_LOCATION)
        self.layout.addWidget(self.le_dx, *consts.MAIN_WINDOW_LE_DX_LOCATION)
        self.layout.addWidget(self.l_dy, *consts.MAIN_WINDOW_L_DY_LOCATION)
        self.layout.addWidget(self.le_dy, *consts.MAIN_WINDOW_LE_DY_LOCATION)
        self.layout.addWidget(self.l_rotate, *consts.MAIN_WINDOW_L_ROTATE_LOCATION)
        self.layout.addWidget(self.l_phi, *consts.MAIN_WINDOW_L_PHI_LOCATION)
        self.layout.addWidget(self.le_phi, *consts.MAIN_WINDOW_LE_PHI_LOCATION)
        self.layout.addWidget(self.pb_run, *consts.MAIN_WINDOW_PB_RUN_LOCATION)
        self.layout.addWidget(self.pb_reset, *consts.MAIN_WINDOW_PB_RESET_LOCATION)

    def connecter(self) -> None:
        self.about.triggered.connect(self.show_about)
        self.task.triggered.connect(self.show_task)
        self.instruction.triggered.connect(self.show_instruction)
        self.pb_run.clicked.connect(self.edit_picture)
        self.pb_reset.clicked.connect(self.reset)

    def edit_picture(self) -> None:
        if not (self.le_x.text() and self.le_y.text()):
            if self.le_kx.text() or self.le_ky.text() or self.le_phi.text():
                self.msgBox.setWindowTitle("Инфо")
                self.msgBox.setText("Для масштабирования и/или поворота необходимо задать центр преобразования")
                self.msgBox.show()
                return
        else:
            center = QVector2D(float(self.le_x.text()), float(self.le_y.text()))
        if self.le_is_valid():
            kx = ky = NEUTRAL_SCALE
            if self.le_kx.text():
                kx = float(self.le_kx.text())
            if self.le_ky.text():
                ky = float(self.le_ky.text())
            if not (kx == ky == NEUTRAL_SCALE):
                self.picture.scale(kx, ky, center)
            dx = dy = NEUTRAL_MOVE
            if self.le_dx.text():
                dx = float(self.le_dx.text())
            if self.le_dy.text():
                dy = float(self.le_dy.text())
            if not (dx == dy == NEUTRAL_MOVE):
                self.picture.move(dx, dy)
            if self.le_phi.text():
                self.picture.rotate(float(self.le_phi.text()), center)
            self.draw_picture()

    def draw_picture(self) -> None:
        self.scene.clear()
        self.model.clear()
        self.plot = self.model.gca()
        self.plot.grid(True)
        self.plot.set_xlim(*consts.FIELD_LIM)
        self.plot.set_ylim(*consts.FIELD_LIM)
        for type, pts in self.picture.anchor_pts:
            if type == "polyline":
                self.draw_polyline(pts)
            elif type == "ellipse":
                self.draw_ellipse(pts)
            elif type == "triangle":
                self.draw_polyline(pts + [pts[0]])
        self.scene.addWidget(FigureCanvas(self.model)) 

    def draw_ellipse(self, pts: list[QVector2D]) -> None:
        center_point, right_point, upper_point = pts
        axis = right_point - center_point
        k_ang = 1
        if axis.y() < 0:
            k_ang = -1
        ellipse = Ellipse(xy=center_point,
                            width= 2 * center_point.distanceToPoint(right_point), 
                            height= 2 * center_point.distanceToPoint(upper_point), 
                            angle= k_ang * degrees(acos(QVector2D.dotProduct(OX, axis) / axis.length() / OX.length())), 
                            edgecolor=consts.COLOR, 
                            fc='None', lw=consts.LINE_WIDTH)
        self.plot.add_patch(ellipse)

    def draw_polyline(self, pts: list[QVector2D]) -> None:
        x, y = [], []
        for point in pts:
            x.append(point.x())
            y.append(point.y())
        self.plot.plot(x, y, consts.COLOR, linewidth=consts.LINE_WIDTH)

    def reset(self) -> None:
        self.picture = Grasshopper()
        self.draw_picture()

    def le_is_valid(self) -> bool:
        is_valid = True
        for le in (self.le_x, self.le_y, self.le_kx, self.le_ky, self.le_dx, self.le_dy, self.le_phi):
            if le.text() == FORBIDDEN_STR and is_valid:
                is_valid = False
                self.msgBox.setWindowTitle("Инфо")
                self.msgBox.setText(f"\"{FORBIDDEN_STR}\" не число")
                self.msgBox.show()
        return is_valid

    def show_about(self) -> None:
        self.msgBox.setWindowTitle("Об авторе")
        self.msgBox.setText("Выполнил Романов Владислав\nГруппа ИУ7-45Б")
        self.msgBox.show()

    def show_task(self) -> None:
        self.msgBox.setWindowTitle("Условие задачи")
        self.msgBox.setText("8. Нарисовать кузнечика, затем осуществить его перенос, масштабирование и поворот")
        self.msgBox.show()

    def show_instruction(self) -> None:
        self.msgBox.setWindowTitle("Помощь")
        self.msgBox.setText("Для выполнения преобразований необходимо задать параметры вещественными числами" +
                            "(если не задать какой-либо параметр, то будет использовано нейтральное значение)" + 
                            "и нажать на кнопку \"Построить решение\".\n\n" +
                            "Для возврата к исходной фигуре необходимо нажать на кнопку \"Сбросить всё\"")
        self.msgBox.show()


if __name__ == '__main__':
    app = QApplication(argv)

    window = Main()
    window.show()

    exit(app.exec_())
