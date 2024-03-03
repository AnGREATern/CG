import consts
from sys import argv
import calc
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QMessageBox, QTableWidget, \
    QHeaderView, QLineEdit, QMenuBar, QMainWindow, QTableWidgetItem, QAction
from PyQt5.QtCore import QRegExp, Qt, QPointF
from pyqtgraph import PlotWidget, ScatterPlotItem, Point, InfiniteLine, TextItem


def draw_point(graph: PlotWidget, table: QTableWidget, point: QPointF) -> None:
    graph.clear()
    row_pos = table.rowCount()
    x_coords = [point.x()]
    y_coords = [point.y()]
    for i in range(row_pos):
        x_coords.append(float(table.item(i, consts.TABLE_POS_X).text()))
        y_coords.append(float(table.item(i, consts.TABLE_POS_Y).text()))
    table.insertRow(row_pos)
    table.setItem(row_pos, consts.TABLE_POS_X, QTableWidgetItem(str(point.x())))
    table.setItem(row_pos, consts.TABLE_POS_Y, QTableWidgetItem(str(point.y())))
    scatter = ScatterPlotItem(x=x_coords, y=y_coords, size=consts.POINT_SIZE)
    graph.addItem(scatter)


def get_points_list(table: QTableWidget) -> list[Point]:
    points = list()
    for i in range(table.rowCount()):
        points.append(Point(float(table.item(i, consts.TABLE_POS_X).text()),
                            float(table.item(i, consts.TABLE_POS_Y).text())))
    return points


class InputPoint(QWidget):
    def __init__(self: QWidget, tw: QTableWidget, graph: PlotWidget, start_point: QPointF) -> None:
        super().__init__()
        self.tw = tw
        self.graph = graph
        self.start_point = start_point

        self.init_ui()

    def init_ui(self: QWidget) -> None:
        self.resize(*consts.SCREEN_INPUT_POINT_SIZE)
        self.setMinimumSize(*consts.SCREEN_INPUT_POINT_SIZE)
        self.setMaximumSize(*consts.SCREEN_INPUT_POINT_SIZE)
        if self.start_point:
            self.setWindowTitle('Изменение точки')
        else:
            self.setWindowTitle('Добавление точки')

        standard_font_size_elems = []

        self.l_points = QLabel(self)
        if self.start_point:
            self.l_points.setText("Введите новые координаты точки:")
        else:
            self.l_points.setText("Введите координаты добавляемой точки:")
        standard_font_size_elems.append(self.l_points)

        validator_float = QRegExpValidator(QRegExp('^[+-]?[0-9][0-9]*[.,]?[0-9]*$'))

        self.le_x = QLineEdit()
        standard_font_size_elems.append(self.le_x)
        self.le_y = QLineEdit()
        standard_font_size_elems.append(self.le_y)
        self.le_x.setValidator(validator_float)
        self.le_y.setValidator(validator_float)
        if self.start_point:
            self.le_x.setText(str(self.start_point.x()))
            self.le_y.setText(str(self.start_point.y()))

        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Critical)
        self.msgBox.setWindowTitle("Ошибка")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        standard_font_size_elems.append(self.msgBox)

        self.pb_add_point = QPushButton("Добавить точку")
        standard_font_size_elems.append(self.pb_add_point)

        for x in standard_font_size_elems:
            x.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.l_points, *consts.ADD_POINT_WINDOW_L_POINTS_LOCATION)
        self.layout.addWidget(self.le_x, *consts.ADD_POINT_WINDOW_LE_X_LOCATION)
        self.layout.addWidget(self.le_y, *consts.ADD_POINT_WINDOW_LE_Y_LOCATION)
        self.layout.addWidget(self.pb_add_point, *consts.ADD_POINT_WINDOW_PB_ADD_POINT_LOCATION)

        self.pb_add_point.clicked.connect(self.add_point)

    def add_point(self: QWidget) -> None:
        if not self.le_x.text():
            self.msgBox.setText("Не введена координата x")
            self.msgBox.show()
            return
        if not self.le_y.text():
            self.msgBox.setText("Не введена координата y")
            self.msgBox.show()
            return
        self.prepare_coords()
        added_point = QPointF(float(self.le_x.text()), float(self.le_y.text()))
        if added_point in get_points_list(self.tw):
            self.msgBox.setText("Такая точка уже есть")
            self.msgBox.show()
            return
        draw_point(self.graph, self.tw, added_point)
        self.close()

    def prepare_coords(self: QWidget) -> None:
        self.le_x.setText(self.le_x.text().replace(',', '.'))
        self.le_y.setText(self.le_y.text().replace(',', '.'))


class Main(QMainWindow):
    def __init__(self: QMainWindow) -> None:
        super().__init__()
        self.init_ui()
        self.input_point = None
        self.solve_created = False
        self.last_added_point_by_click = None

    def init_ui(self: QMainWindow) -> None:
        self.resize(*consts.SCREEN_START_SIZE)
        self.setWindowTitle('Задача №1')
        self.setMinimumSize(*consts.SCREEN_START_SIZE)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        standard_font_size_elems = []
        big_font_size_elems = []

        self.tw = QTableWidget(self.main_widget)
        self.tw.setColumnCount(len(consts.HEADERS))
        self.tw.setHorizontalHeaderLabels(consts.HEADERS)
        tw_header = self.tw.horizontalHeader()
        tw_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        standard_font_size_elems.append(tw_header)
        self.tw.setEditTriggers(QTableWidget.NoEditTriggers)
        standard_font_size_elems.append(self.tw)

        self.graph = PlotWidget()
        self.graph.showGrid(x=True, y=True)
        self.graph.setMenuEnabled(False)
        self.graph.hideButtons()
        standard_font_size_elems.append(self.graph)

        self.pb_add_point = QPushButton("Добавить точку")
        standard_font_size_elems.append(self.pb_add_point)
        self.pb_edit_point = QPushButton("Изменить точку")
        standard_font_size_elems.append(self.pb_edit_point)
        self.pb_del_point = QPushButton("Удалить точку")
        standard_font_size_elems.append(self.pb_del_point)
        self.pb_clear_graph = QPushButton("Очистить всё")
        standard_font_size_elems.append(self.pb_clear_graph)
        self.pb_solve = QPushButton("Построить решение")
        self.pb_solve.setMinimumHeight(consts.BIG_ELEMS_MINIMUM_SIZE)
        big_font_size_elems.append(self.pb_solve)

        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        standard_font_size_elems.append(self.msgBox)

        self.l_points = QLabel(self)
        self.l_points.setText("Множество точек:")
        standard_font_size_elems.append(self.l_points)

        self.mb = QMenuBar(self)
        self.setMenuBar(self.mb)
        self.info = self.mb.addMenu("Информация")
        self.about = QAction("Об авторе", self)
        self.task = QAction("Условие задачи", self)
        self.instruction = QAction("Инструкция", self)
        self.info.addAction(self.about)
        self.info.addAction(self.task)
        self.info.addAction(self.instruction)
        self.about.triggered.connect(self.show_about)
        self.task.triggered.connect(self.show_task)
        self.instruction.triggered.connect(self.show_instruction)

        for x in standard_font_size_elems:
            x.setFont(QFont(consts.FONT_TYPE, consts.FONT_STANDARD_SIZE))

        for x in big_font_size_elems:
            x.setFont(QFont(consts.FONT_TYPE, consts.FONT_BIG_SIZE))

        self.layout = QGridLayout(self.main_widget)
        self.layout.addWidget(self.graph, *consts.MAIN_WINDOW_GRAPH_LOCATION)
        self.layout.addWidget(self.l_points, *consts.MAIN_WINDOW_L_POINTS_LOCATION)
        self.layout.addWidget(self.tw, *consts.MAIN_WINDOW_TABLE_LOCATION)
        self.layout.addWidget(self.pb_add_point, *consts.MAIN_WINDOW_PB_ADD_POINT_LOCATION)
        self.layout.addWidget(self.pb_edit_point, *consts.MAIN_WINDOW_PB_EDIT_POINT_LOCATION)
        self.layout.addWidget(self.pb_del_point, *consts.MAIN_WINDOW_PB_DEL_POINT_LOCATION)
        self.layout.addWidget(self.pb_clear_graph, *consts.MAIN_WINDOW_PB_CLEAR_LOCATION)
        self.layout.addWidget(self.pb_solve, *consts.MAIN_WINDOW_PB_SOLVE_LOCATION)

        self.pb_add_point.clicked.connect(self.add_point)
        self.pb_edit_point.clicked.connect(self.edit_point)
        self.pb_del_point.clicked.connect(self.del_point)
        self.pb_clear_graph.clicked.connect(self.clear_graph)
        self.pb_solve.clicked.connect(self.print_solve)
        self.tw.cellClicked.connect(self.highlight_line)
        self.graph.scene().sigMouseClicked.connect(self.graph_clicked)

    def graph_clicked(self: QMainWindow, ev) -> None:
        if ev.button() == Qt.MouseButton.RightButton:
            self.graph.autoRange()
        elif ev.button() == Qt.MouseButton.LeftButton:
            self.solve_created = False
            pos = ev.pos()
            if self.last_added_point_by_click is not None and pos == self.last_added_point_by_click:
                self.msgBox.setWindowTitle("Инфо")
                self.msgBox.setText("Данная точка была добавлена в множество ранее")
                self.msgBox.show()
                return
            pos = self.graph.plotItem.vb.mapToView(pos)
            added_point = QPointF(pos.x(), pos.y())
            self.last_added_point_by_click = Point(pos.x(), pos.y())
            if added_point in get_points_list(self.tw):
                self.msgBox.setWindowTitle("Инфо")
                self.msgBox.setText("Данная точка была добавлена в множество ранее")
                self.msgBox.show()
            else:
                draw_point(self.graph, self.tw, added_point)

    def show_about(self: QMainWindow) -> None:
        self.msgBox.setWindowTitle("Об авторе")
        self.msgBox.setText("Выполнил Романов Владислав\nГруппа ИУ7-45Б")
        self.msgBox.show()

    def show_task(self: QMainWindow) -> None:
        self.msgBox.setWindowTitle("Условие задачи")
        self.msgBox.setText(
            "34. На плоскости дано множество точек. Найти такой треугольник" +
            ", с вершинами в этих точках, у которого угол, образованный прямой" +
            ", соединяющий точку пересечения высот и начала координат, и осью ординат максимален.\n\n" +
            "Вывести изображение в графическом режиме.")
        self.msgBox.show()

    def show_instruction(self: QMainWindow) -> None:
        self.msgBox.setWindowTitle("Помощь")
        self.msgBox.setText("Для добавления точки можно либо поставить точку мышью на графике, либо вбить координаты " +
                            "вручную после нажатия на кнопку \"Добавить точку\".\n\n" +
                            "Для изменения (удаления) точки необходимо выбрать " +
                            "её в списке, после чего нажать на кнопку \"Изменить точку\" (\"Удалить точку\").\n\n" +
                            "Колёсиком мыши можно изменять масштаб графика. Поставить автомасштабирование можно " +
                            "нажатием на правую кнопку мыши в области графика. " +
                            "Режим автомасштабирования выбран изначально.\n\n" +
                            "Для отображения решения необходимо нажать на кнопку \"Построить решение\".")
        self.msgBox.show()

    def add_point(self: QMainWindow, added_point: QPointF=None) -> None:
        self.solve_created = False
        self.input_point = InputPoint(self.tw, self.graph, added_point)
        self.input_point.show()

    def edit_point(self: QMainWindow) -> None:
        if self.tw.currentRow() == consts.TABLE_NOT_SELECTED_ROW:
            self.msgBox.setWindowTitle("Инфо")
            self.msgBox.setText(
                "Для изменения необходимо нажать в списке на любую координату изменяемой точки в списке")
            self.msgBox.show()
            return
        added_point = QPointF(float(self.tw.item(self.tw.currentRow(), consts.TABLE_POS_X).text()), 
                              float(self.tw.item(self.tw.currentRow(), consts.TABLE_POS_Y).text()))
        self.del_point()
        self.add_point(added_point)

    def del_point(self: QMainWindow) -> None:
        if self.tw.currentRow() == consts.TABLE_NOT_SELECTED_ROW:
            self.msgBox.setWindowTitle("Инфо")
            self.msgBox.setText("Для удаления необходимо нажать в списке на любую координату удаляемой точки в списке")
            self.msgBox.show()
            return
        self.solve_created = False
        self.tw.removeRow(self.tw.currentRow())
        self.tw.setCurrentItem(None)
        self.graph.clear()
        x_coords = []
        y_coords = []
        for i in range(self.tw.rowCount()):
            x_coords.append(float(self.tw.item(i, consts.TABLE_POS_X).text()))
            y_coords.append(float(self.tw.item(i, consts.TABLE_POS_Y).text()))
        scatter = ScatterPlotItem(x=x_coords, y=y_coords, size=consts.POINT_SIZE)
        self.graph.addItem(scatter)

    def clear_graph(self: QMainWindow) -> None:
        self.solve_created = False
        self.graph.clear()
        self.tw.setRowCount(0)

    def print_solve(self: QMainWindow) -> None:
        if self.tw.rowCount() < consts.NODE_COUNT:
            self.msgBox.setWindowTitle("Инфо")
            self.msgBox.setText("Введено слишком мало точек для поиска треугольника." +
                                "\nВведите хотя бы 3 точки, не лежащих на одной прямой.")
            self.msgBox.show()
            return
        if self.solve_created:
            self.msgBox.setWindowTitle("Инфо")
            self.msgBox.setText("Решение для данного множество точек уже построено")
            self.msgBox.show()
            return
        ans = calc.get_solution(get_points_list(self.tw))
        if ans is None:
            self.msgBox.setWindowTitle("Инфо")
            self.msgBox.setText("Не удалось построить ни одного треугольника." +
                                "\nВведите хотя бы 3 точки, не лежащих на одной прямой.")
            self.msgBox.show()
            return
        angle, source_angle, m, a, b, c, a_h, b_h, c_h = ans
        self.graph.plot([a.x(), b.x(), c.x(), a.x()], [a.y(), b.y(), c.y(), a.y()], symbolSize=consts.POINT_SIZE)
        self.graph.plot([a.x(), a_h.x()], [a.y(), a_h.y()], pen='g')
        self.graph.plot([b.x(), b_h.x()], [b.y(), b_h.y()], pen='g')
        self.graph.plot([c.x(), c_h.x()], [c.y(), c_h.y()], pen='g')
        self.graph.plot([a.x(), m.x()], [a.y(), m.y()], pen='g')
        self.graph.plot([b.x(), m.x()], [b.y(), m.y()], pen='g')
        self.graph.plot([c.x(), m.x()], [c.y(), m.y()], pen='g')
        self.graph.addItem(InfiniteLine(pos=consts.CENTER, pen='r'))
        self.graph.addItem(InfiniteLine(pos=consts.CENTER, angle=source_angle + consts.RIGHT_ANGLE, pen='r'))
        self.solve_created = True
        angle_text = TextItem(f"Угол: {round(angle)}°", color='r')
        self.graph.addItem(angle_text)

    def highlight_line(self: QMainWindow) -> None:
        if isinstance(self.tw.currentRow(), int):
            self.tw.selectRow(self.tw.currentRow())


if __name__ == '__main__':
    app = QApplication(argv)

    window = Main()
    window.show()

    exit(app.exec_())
