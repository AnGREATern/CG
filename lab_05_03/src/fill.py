from PyQt5.QtGui import QColor, QPainter, QImage
from PyQt5.QtCore import QPoint, QPointF
from time import sleep
import consts

BACK_COLOR = QColor(*consts.BACK_COLOR_DEFAULT)
LINE_COLOR = QColor(*consts.LINE_COLOR_DEFAULT)


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
            
            
def row_fill(plot: QImage, start: QPoint, x_bar: int, direction: int, color: QColor) -> QPoint:
    cur = QPoint(start)
    # step = QPoint(direction, 0)
    # if direction:
    #     while plot.pixelColor(start + step) == LINE_COLOR:
    #         start += step
    #     if abs(cur.x() - x_bar) > abs(x_bar - start.x()):
    #         cur = QPoint(start)
    step = QPoint(sign(x_bar - cur.x()), 0)
    while cur.x() != x_bar:
        if plot.pixelColor(cur) == BACK_COLOR:
            plot.setPixelColor(cur, color)
        elif plot.pixelColor(cur) == color:
            plot.setPixelColor(cur, BACK_COLOR)
        cur += step

            
def edge_fill(plot: QImage, a: QPoint, b: QPoint, x_bar: int, color: QColor, save) -> None:    
    if a.y() == b.y():
        return
    if a.y() > b.y():
        a, b = b, a
    # print("Edge points:", a, b)
    d = QPointF(b - a)
    d /= d.y()
    direction = sign(d.x())
    cur_left = a
    while cur_left.y() <= b.y():
        # print(cur_left)
        row_fill(plot, QPoint(round(cur_left.x()), round(cur_left.y())), x_bar, direction, color)
        save()
        cur_left += d
        # coercion_border(plot, cur_left, direction)
        # if plot.pixelColor(QPoint(round(cur_left.x() + 1), round(cur_left.y()))) == LINE_COLOR:
        #     cur_left += QPoint(1, 0)
        # elif plot.pixelColor(QPoint(round(cur_left.x() - 1), round(cur_left.y()))) == LINE_COLOR:
        #     cur_left += QPoint(-1, 0)
        # sleep(consts.DELAY)
        # cur_left += d
        # cur_left = QPoint(round(cur_left.x()), round(cur_left.y()))
        # plot.pixelColor(start + step) == LINE_COLOR:
        # align_border(plot, cur_left, direction)
        # print(cur_left)
            
            
# def coercion_border(plot: QImage, cur_left: QPoint, direction: int) -> None:
#     if plot.pixelColor(QPoint(round(cur_left.x()), round(cur_left.y()))) == LINE_COLOR:
#         return
#     print(QPoint(round(cur_left.x()), round(cur_left.y())))
#     if not direction:
#         direction = 1
#     while plot.pixelColor(QPoint(round(cur_left.x() + direction), round(cur_left.y()))) != LINE_COLOR:
#         print(QPoint(round(cur_left.x() + direction), round(cur_left.y())))
#         direction *= -1
#         if direction > 0:
#             direction += 1
#         if direction > 20:
#             break
#     else:
#         cur_left += QPoint(direction, 0)


# def align_border(plot: QImage, cur_left: QPointF, direction: int) -> None:
#     cur_left = QPoint(round(cur_left.x()), round(cur_left.y()))
#     # if direction:
#     #     while plot.pixelColor(cur_left) == LINE_COLOR:
#     #         cur_left += QPoint(direction, 0)


def barrier_fill(plot: QImage, polygon: list[list[QPoint]], color: QColor, save) -> None:
    x_bar = get_x_barrier(polygon)
    for polyline in polygon:
        for i in range(len(polyline)):
            edge_fill(plot, QPoint(polyline[i - 1]), QPoint(polyline[i]), x_bar, color, save)
            # break
            # sleep(consts.DELAY)
