from PyQt5.QtGui import QColor, QPainter, QImage
from PyQt5.QtCore import QPoint, QPointF
from math import cos, sin, pi


RESOLUTION = 1080


def plot_pixel(
    plot: QImage, point: QPoint | QPointF, color: QColor, alpha: float = 1.0
) -> QPoint:
    pix_p = QPoint(round(point.x()), round(point.y()))
    if plot.rect().contains(pix_p):
        if 0 <= alpha <= 1:
            color.setAlphaF(alpha)
        plot.setPixel(pix_p, color.rgba())
    return pix_p


def plot_near(
    plot: QImage, point: QPoint | QPointF, col: int, row: int, color: QColor
) -> None:
    plot_pixel(plot, QPointF(point.x() + col, point.y() + row), color)
    plot_pixel(plot, QPointF(point.x() + col, point.y() - row), color)
    plot_pixel(plot, QPointF(point.x() - col, point.y() + row), color)
    plot_pixel(plot, QPointF(point.x() - col, point.y() - row), color)


def internal_impl(
    plot: QImage, center: QPoint, rx: int, ry: int, color: QColor
) -> None:
    painter = QPainter(plot)
    painter.setPen(color)
    painter.drawEllipse(center, rx, ry)
    painter.end()


def canonical_impl(
    plot: QImage, center: QPoint, rx: int, ry: int, color: QColor
) -> None:
    for x in range(center.x() - rx, center.x() + rx + 1):
        y = center.y() + (ry * ((1 - (x - center.x()) ** 2 / rx**2) ** 0.5))
        plot_pixel(plot, QPointF(x, y), color)
        plot_pixel(plot, QPointF(x, 2 * center.y() - y), color)
    for y in range(center.y() - ry, center.y() + ry + 1):
        x = center.x() + (rx * ((1 - (y - center.y()) ** 2 / ry**2) ** 0.5))
        plot_pixel(plot, QPointF(x, y), color)
        plot_pixel(plot, QPointF(2 * center.x() - x, y), color)


def parametric_impl(
    plot: QImage, center: QPoint, rx: int, ry: int, color: QColor
) -> None:
    for i in range(RESOLUTION):
        t = 2 * pi * i / RESOLUTION
        x = center.x() + rx * cos(t)
        y = center.y() + ry * sin(t)
        plot_pixel(plot, QPointF(x, y), color)


def bresenham_impl(
    plot: QImage, center: QPoint, rx: int, ry: int, color: QColor
) -> None:
    row = ry
    col = 0
    d = 2 * rx**2 * (row - 1) * row + rx**2 + 2 * ry**2 * (1 - rx * rx)
    while rx * rx * row > ry * ry * col:
        plot_near(plot, center, col, row, color)
        if d >= 0:
            row -= 1
            d -= 4 * rx * rx * row
        d += 2 * ry * ry * (3 + col * 2)
        col += 1
    d = (
        2 * ry * ry * (col + 1) * col
        + 2 * rx * rx * (row * (row - 2) + 1)
        + (1 - 2 * rx * rx) * ry * ry
    )
    while row + 1:
        plot_near(plot, center, col, row, color)
        if d <= 0:
            col += 1
            d += 4 * ry * ry * col
        row -= 1
        d += 2 * rx * rx * (3 - 2 * row)
