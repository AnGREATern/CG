from PyQt5.QtGui import QColor, QPainter, QImage
from PyQt5.QtCore import QPoint, QPointF
from consts import EPS
from math import radians, cos, sin, floor


def rotate(point: QPoint, center: QPoint, phi: float):
    point -= center
    phi = radians(phi)
    x1 = point.x() * cos(phi) - point.y() * sin(phi)
    y1 = point.x() * sin(phi) + point.y() * cos(phi)
    point.setX(round(x1))
    point.setY(round(y1))
    point += center
    

def plot_pixel(plot: QImage, point: QPoint | QPointF, color: QColor, alpha: float = 1.0):
    pix_p = QPoint(round(point.x()), round(point.y()))
    if plot.rect().contains(pix_p):
        if 0 <= alpha <= 1:
            color.setAlphaF(alpha)
        plot.setPixel(pix_p, color.rgba())


def internal_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    painter = QPainter(plot)
    painter.setPen(color)
    painter.drawLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())
    painter.end()


def dda_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    if start_point == end_point:
        plot.setPixel(start_point, color.rgb())
    else:
        cur = QPointF(start_point)
        d = end_point - start_point
        l = max(abs(d.x()), abs(d.y()))
        d = QPointF(d.x() / l, d.y() / l)
        for _ in range(l):
            plot_pixel(plot, cur, color)
            cur += d


def sign(x: int | float) -> int:
    ans = 1
    if abs(x) < EPS:
        ans = 0
    elif x < -EPS:
        ans = -1
    return ans


def bresenham_real_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    if start_point == end_point:
        plot.setPixel(start_point, color.rgb())
    else:
        cur = QPointF(start_point)
        d = end_point - start_point
        sp = QPoint(sign(d.x()), sign(d.y()))
        d = QPoint(abs(d.x()), abs(d.y()))
        if d.y() >= d.x():
            is_changed = True
            d = d.transposed()
        else:
            is_changed = False
        m = d.y() / d.x()
        e = m - 0.5
        while cur != end_point:
            plot_pixel(plot, cur, color)
            if e >= 0:
                if not is_changed:
                    cur.setY(cur.y() + sp.y())
                else:
                    cur.setX(cur.x() + sp.x())
                e -= 1
            else:
                if not is_changed:
                    cur.setX(cur.x() + sp.x())
                else:
                    cur.setY(cur.y() + sp.y())
                e += m


def bresenham_int_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    if start_point == end_point:
        plot.setPixel(start_point, color.rgb())
    else:
        cur = QPointF(start_point)
        d = end_point - start_point
        sp = QPoint(sign(d.x()), sign(d.y()))
        d = QPoint(abs(d.x()), abs(d.y()))
        if d.y() >= d.x():
            is_changed = True
            d = d.transposed()
        else:
            is_changed = False
        e = 2 * d.y() - d.x()
        while cur != end_point:
            plot_pixel(plot, cur, color)
            if e >= 0:
                if not is_changed:
                    cur.setY(cur.y() + sp.y())
                else:
                    cur.setX(cur.x() + sp.x())
                e -= 2 * d.x()
            else:
                if not is_changed:
                    cur.setX(cur.x() + sp.x())
                else:
                    cur.setY(cur.y() + sp.y())
                e += 2 * d.y()


def bresenham_classic_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    if start_point == end_point:
        plot.setPixel(start_point, color.rgb())
    else:
        i = 256
        cur = QPointF(start_point)
        d = end_point - start_point
        sp = QPoint(sign(d.x()), sign(d.y()))
        d = QPoint(abs(d.x()), abs(d.y()))
        if d.y() >= d.x():
            is_changed = True
            d = d.transposed()
        else:
            is_changed = False
        m = i * d.y() / d.x()
        w = i - m
        e = 0.5
        for _ in range(d.x() + 1):
            plot_pixel(plot, cur, color, 1 - e / i + int(e / i))
            if e < w:
                if is_changed:
                    cur.setY(cur.y() + sp.y())
                else:
                    cur.setX(cur.x() + sp.x())
                e += m
            else:
                cur.setX(cur.x() + sp.x())
                cur.setY(cur.y() + sp.y())
                e -= w


def wu_impl(
    plot: QImage, start_point: QPoint, end_point: QPoint, color: QColor
) -> None:
    pass
    d = end_point - start_point
    cur = start_point
    is_changed = abs(d.x()) < abs(d.y())
    if is_changed:
        cur = cur.transposed()
        end_point = end_point.transposed()
        d = d.transposed()
    if end_point.x() < cur.x():
        cur, end_point = end_point, cur
    gradient = d.y() / d.x()
    
    pend = QPointF()
    pend.setX(round(cur.x()))
    pend.setY(cur.y() + gradient * (pend.x() - cur.x()))
    xgap = -cur.x() - 0.5 + int(cur.x() + 0.5)
    pxl1 = QPointF(pend.x(), floor(pend.y()))
    plot_pixel(plot, pxl1, color, (1 - pend.y() + int(pend.y())) * xgap)
    plot_pixel(plot, pxl1 + QPointF(0, 1), color, (pend.y() - int(pend.y())) * xgap)
    intery = pend.y() + gradient

    pend = QPointF()
    pend.setX(round(end_point.x()))
    pend.setY(end_point.y() + gradient * (pend.x() - end_point.x()))
    xgap = -end_point.x() - 0.5 + int(end_point.x() + 0.5)
    pxl2 = QPointF(pend.x(), floor(pend.y()))
    plot_pixel(plot, pxl2, color, (1 - pend.y() + int(pend.y())) * xgap)
    plot_pixel(plot, pxl2 + QPointF(0, 1), color, (pend.y() - int(pend.y())) * xgap)
    
    for x in range(round(pxl1.x()) + 1, round(pxl2.x())):
        if not is_changed:
            plot_pixel(plot, QPointF(x, floor(intery)), color, 1 - intery + int(intery))
            plot_pixel(plot, QPointF(x, floor(intery) + 1), color, intery - int(intery))
        else:
            plot_pixel(plot, QPointF(floor(intery), x), color, 1 - intery + int(intery))
            plot_pixel(plot, QPointF(floor(intery) + 1, x), color, intery - int(intery))
        intery += gradient
