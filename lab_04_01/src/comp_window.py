from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QImage
from PyQt5.QtCore import QSize, QPoint
from algorithms import (
    internal_impl,
    bresenham_impl,
    canonical_impl,
    parametric_impl,
)


SCREEN_START_SIZE = (1400, 900)
LABELS_ROTATION = 8
TEST_CENTER_POINT = QPoint(0, 0)
TEST_RX = 2000
TEST_RY = 1000


class CompWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(*SCREEN_START_SIZE)
        self.setWindowTitle("Сравнение времени работы")
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        self.im = QImage(QSize(*SCREEN_START_SIZE), QImage.Format_ARGB32)

        self.algs = {
            "Библиотечный": internal_impl,
            "Параметрическое уравнение": parametric_impl,
            "Алгоритм Брезенхема": bresenham_impl,
            "Каноническое уравнение": canonical_impl,
        }
        self.plot_time()
        self.canvas.draw()

    def plot_time(self) -> None:
        data = []
        for alg in self.algs.values():
            start_time = datetime.now()
            alg(self.im, TEST_CENTER_POINT, TEST_RX, TEST_RY, QColor())
            data.append((datetime.now() - start_time).microseconds)
        self.ax.bar(self.algs.keys(), data)
        self.ax.set_xticklabels(self.algs, rotation=LABELS_ROTATION)
        self.ax.set_xlabel("Алгоритм")
        self.ax.set_ylabel("Время (мкс)")
