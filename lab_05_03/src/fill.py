from PyQt5.QtGui import QColor, QImage
from PyQt5.QtCore import QPoint, QPointF
from time import sleep
import consts

BACK_COLOR = QColor(*consts.BACK_COLOR_DEFAULT)
LINE_COLOR = QColor(*consts.LINE_COLOR_DEFAULT)
MAX_ADJUSTMENT = 10


def get_x_barrier(polygon: list[list[QPoint]]) -> int:
    sum_x = 0
    cnt = 0
    for polyline in polygon:
        for point in polyline:
            sum_x += point.x()
        cnt += len(polyline)
    return round(sum_x / cnt)


def sign(x: int | float) -> int:
    ans = 1
    if abs(x) < consts.EPS:
        ans = 0
    elif x < -consts.EPS:
        ans = -1
    return ans


def row_fill(plot: QImage, start: QPoint, x_bar: int, color: QColor) -> None:
    cur = QPoint(start)
    step = QPoint(sign(x_bar - cur.x()), 0)
    while cur.x() != x_bar:
        if plot.pixelColor(cur) == BACK_COLOR:
            plot.setPixelColor(cur, color)
        elif plot.pixelColor(cur) != LINE_COLOR:
            plot.setPixelColor(cur, BACK_COLOR)
        cur += step
    if step.x() > 0:
        if plot.pixelColor(cur) == BACK_COLOR:
            plot.setPixelColor(cur, color)
        elif plot.pixelColor(cur) != LINE_COLOR:
            plot.setPixelColor(cur, BACK_COLOR)


def edge_fill(
    plot: QImage, a: QPoint, b: QPoint, x_bar: int, color: QColor, save, delay: float
) -> None:
    if a.y() == b.y():
        return
    if a.y() > b.y():
        a, b = b, a
    d = QPointF(b - a)
    d /= d.y()
    direction = sign(d.x())
    cur_left = a + d
    adjust_border(plot, cur_left, direction)
    while cur_left.y() <= b.y():
        row_fill(plot, QPoint(int(cur_left.x()), int(cur_left.y())), x_bar, color)
        save(delay)
        sleep(delay)
        cur_left += d
        adjust_border(plot, cur_left, direction)


def adjust_border(plot: QImage, cur_left: QPoint, direction: int) -> None:
    if plot.pixelColor(QPoint(int(cur_left.x()), int(cur_left.y()))) == LINE_COLOR:
        return
    if not direction:
        direction = 1
    while (
        plot.pixelColor(QPoint(int(cur_left.x() + direction), int(cur_left.y())))
        != LINE_COLOR
        and direction < MAX_ADJUSTMENT
    ):
        direction *= -1
        if direction > 0:
            direction += 1
    if direction < MAX_ADJUSTMENT:
        cur_left += QPoint(direction, 0)


def barrier_fill(
    plot: QImage, polygon: list[list[QPoint]], color: QColor, save, delay: float = 0
) -> None:
    x_bar = get_x_barrier(polygon)
    for polyline in polygon:
        for i in range(len(polyline)):
            edge_fill(
                plot,
                QPoint(polyline[i - 1]),
                QPoint(polyline[i]),
                x_bar,
                color,
                save,
                delay,
            )
