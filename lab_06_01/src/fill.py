from PyQt5.QtGui import QColor, QImage
from PyQt5.QtCore import QPoint
from time import sleep
import consts

BACK_COLOR = QColor(*consts.BACK_COLOR_DEFAULT)
LINE_COLOR = QColor(*consts.LINE_COLOR_DEFAULT)
STEP_RIGHT = QPoint(1, 0)
STEP_LEFT = QPoint(-1, 0)
STEP_UP = QPoint(0, -1)
STEP_DOWN = QPoint(0, 1)


def find_seed_point(plot: QImage, start: QPoint, end: QPoint) -> list[QPoint]:
    if not plot.rect().contains(start):
        return
    res = []
    cur = None
    while start != end:
        if cur is not None and plot.pixelColor(start) == LINE_COLOR:
            res.append(cur)
            cur = None
        elif plot.pixelColor(start) == BACK_COLOR:
            cur = QPoint(start)
        start += STEP_RIGHT
    if cur is not None:
        res.append(cur)
    return res


def row_fill(plot: QImage, start: QPoint, step: QPoint, color: QColor) -> QPoint:
    cur = QPoint(start)
    while plot.rect().contains(cur) and plot.pixelColor(cur) != LINE_COLOR:
        plot.setPixelColor(cur, color)
        cur += step
    if step == STEP_LEFT:
        cur += STEP_RIGHT
    return cur


def seed_fill(
    plot: QImage, base_point: QPoint, color: QColor, save, delay: float = 0
) -> None:
    stack = [base_point]
    while len(stack):
        cur = stack.pop()
        right_side = row_fill(plot, cur, STEP_RIGHT, color)
        left_side = row_fill(plot, cur, STEP_LEFT, color)
        if res := find_seed_point(plot, left_side + STEP_UP, right_side + STEP_UP):
            stack.extend(res)
        if res := find_seed_point(plot, left_side + STEP_DOWN, right_side + STEP_DOWN):
            stack.extend(res)
        save(delay)
        sleep(delay)
