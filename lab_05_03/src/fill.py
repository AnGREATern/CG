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
            
            
def row_fill(plot: QImage, start: QPoint, x_bar: int, color: QColor) -> QPoint:
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
    if step.x() > 0:
        if plot.pixelColor(cur) == BACK_COLOR:
            plot.setPixelColor(cur, color)
        elif plot.pixelColor(cur) == color:
            plot.setPixelColor(cur, BACK_COLOR)

            
def edge_fill(plot: QImage, a: QPoint, b: QPoint, extr: int, x_bar: int, color: QColor) -> None:    
    if a.y() == b.y():
        return
    if a.y() > b.y():
        a, b = b, a
        if 1 <= extr <= 2:
            extr ^= 3
    # print("Edge points:", a, b)
    d = QPointF(b - a)
    d /= d.y()
    direction = sign(d.x())
    cur_left = a + d
    # row_fill(plot, cur_left, x_bar, color, False)
    adjust_border(plot, cur_left, direction)
    # if extr & 1:
    #     cur_left += d
    #     adjust_border(plot, cur_left, direction)
    while cur_left.y() <= b.y():
        # print(cur_left)
        # is_inverse = True
        # if cur_left.y() == a.y() and extr
        row_fill(plot, QPoint(int(cur_left.x()), int(cur_left.y())), x_bar, color)
        cur_left += d
        adjust_border(plot, cur_left, direction)
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
    # if extr ^ 2:
    #     row_fill(plot, QPoint(int(cur_left.x()), int(cur_left.y())), x_bar, color)
            
            
def adjust_border(plot: QImage, cur_left: QPoint, direction: int) -> None:
    if plot.pixelColor(QPoint(int(cur_left.x()), int(cur_left.y()))) == LINE_COLOR:
        return
    if not direction:
        direction = 1
    while (plot.pixelColor(QPoint(int(cur_left.x() + direction), int(cur_left.y()))) != LINE_COLOR 
            and direction < MAX_ADJUSTMENT):
        direction *= -1
        if direction > 0:
            direction += 1
    if direction < MAX_ADJUSTMENT:
        cur_left += QPoint(direction, 0)


# def align_border(plot: QImage, cur_left: QPointF, direction: int) -> None:
#     cur_left = QPoint(round(cur_left.x()), round(cur_left.y()))
#     # if direction:
#     #     while plot.pixelColor(cur_left) == LINE_COLOR:
#     #         cur_left += QPoint(direction, 0)

def is_extremum(a: QPoint, b: QPoint, c: QPoint) -> bool:
    ans = False
    if b.y() < min(a.y(), c.y()) or b.y() > max(a.y(), c.y()):
        ans = True
    return ans


def barrier_fill(plot: QImage, polygon: list[list[QPoint]], color: QColor, save) -> None:
    x_bar = get_x_barrier(polygon)
    for polyline in polygon:
        for i in range(len(polyline)):
            extr = is_extremum(polyline[i - 2], polyline[i - 1], polyline[i - 1])
            extr += 2 * is_extremum(polyline[i - 1], polyline[i], polyline[(i + 1) % len(polyline)])
            edge_fill(plot, QPoint(polyline[i - 1]), QPoint(polyline[i]), extr, x_bar, color)
            save()
            # break
            # sleep(consts.DELAY)
    
