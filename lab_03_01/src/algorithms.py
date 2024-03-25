from PyQt5.QtGui import QVector2D


def internal_impl(
    plot, start_point: QVector2D, end_point: QVector2D, color: str
) -> None:
    # plot.plot([start_point.x(), end_point.x()], [start_point.y(), end_point.y()], color)
    plot[start_point.x(), start_point.y()] = color


def dda_impl(plot, start_point: QVector2D, end_point: QVector2D, color: str) -> None:
    if start_point == end_point:
        pass
    else:
        pass


def bresenham_real_impl(
    plot, start_point: QVector2D, end_point: QVector2D, color: str
) -> None:
    pass


def bresenham_int_impl(
    plot, start_point: QVector2D, end_point: QVector2D, color: str
) -> None:
    pass


def bresenham_classic_impl(
    plot, start_point: QVector2D, end_point: QVector2D, color: str
) -> None:
    pass


def wu_impl(plot, start_point: QVector2D, end_point: QVector2D, color: str) -> None:
    pass
