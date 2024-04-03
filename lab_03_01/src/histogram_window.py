from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QImage
from PyQt5.QtCore import QSize, QPoint
from algorithms import (
    internal_impl,
    dda_impl,
    bresenham_real_impl,
    bresenham_int_impl,
    bresenham_classic_impl,
    wu_impl,
    rotate,
)


SCREEN_START_SIZE = (1400, 900)
LABELS_ROTATION = 8
TEST_START_POINT = QPoint(0, 0)
TEST_END_POINT = QPoint(1000, 1000)
TEST_LINE_LENGTH = 1000
DEGREES_STEP = 10
LAST_DEGREE = 90


class HistogramWindow(QMainWindow):
    def __init__(self, is_time: bool = True) -> None:
        super().__init__()
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Сравнение времени работы")
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        self.im = QImage(QSize(*SCREEN_START_SIZE), QImage.Format_ARGB32)

        self.algs = {
            "Библиотечный": internal_impl,
            "Цифровой дифференциальный анализатор": dda_impl,
            "Брезенхема с действительными данными": bresenham_real_impl,
            "Брезенхема с целочисленными данными": bresenham_int_impl,
            "Брезенхема с устранением ступенчатости": bresenham_classic_impl,
            "Ву": wu_impl,
        }
        if is_time:
            self.plot_time()
        else:
            self.plot_stepwise()
        self.canvas.draw()

    def plot_time(self) -> None:
        data = []
        for alg in self.algs.values():
            start_time = datetime.now()
            alg(self.im, TEST_START_POINT, TEST_END_POINT, QColor())
            data.append((datetime.now() - start_time).microseconds)
        self.ax.bar(self.algs.keys(), data)
        self.ax.set_xticklabels(self.algs, rotation=LABELS_ROTATION)
        self.ax.set_xlabel("Алгоритм")
        self.ax.set_ylabel("Время (мкс)")

    def plot_stepwise(self) -> None:
        degrees = [i for i in range(DEGREES_STEP, LAST_DEGREE + 1, DEGREES_STEP)]
        for alg in list(self.algs.values())[1:]:
            res = []
            end_point = TEST_START_POINT + QPoint(TEST_LINE_LENGTH, 0)
            for _ in degrees:
                rotate(end_point, TEST_START_POINT, -DEGREES_STEP)
                res.append(alg(self.im, TEST_START_POINT, end_point, QColor()))
            self.ax.plot(degrees, res)
        self.ax.legend(list(self.algs.keys())[1:])
        self.ax.set_xlabel("Наклон линии")
        self.ax.set_ylabel("Количество ступеней")
