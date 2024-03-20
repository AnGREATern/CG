from geom import Point

TYPE_INDEX = 0
POINTS_INDEX = 1


class Grasshopper:
    def __init__(self) -> None:
        mustache = (
            "polyline",
            [
                Point(-2, 8),
                Point(-1, 8),
                Point(0, 5),
                Point(1, 8),
                Point(2, 8),
            ],
        )
        left_leg = (
            "polyline",
            [Point(-2, -4), Point(-1, -4), Point(-1, -2.598)],
        )
        right_leg = (
            "polyline",
            [Point(2, -4), Point(1, -4), Point(1, -2.598)],
        )
        head = ("ellipse", [Point(0, 5), Point(2, 5), Point(0, 7)])
        left_eye = (
            "ellipse",
            [Point(-0.75, 5.25), Point(-0.25, 5.25), Point(-0.75, 5.75)],
        )
        right_eye = (
            "ellipse",
            [Point(0.75, 5.25), Point(1.25, 5.25), Point(0.75, 5.75)],
        )
        body = ("ellipse", [Point(0, 0), Point(2, 0), Point(0, 3)])
        left_arm = (
            "triangle",
            [Point(-1, -0.5), Point(-1, 0.5), Point(-5, 3)],
        )
        right_arm = (
            "triangle",
            [Point(1, -0.5), Point(1, 0.5), Point(5, 3)],
        )
        self.anchor_pts: tuple[tuple[str, list[Point]]] = (
            mustache,
            left_leg,
            right_leg,
            head,
            left_eye,
            right_eye,
            body,
            left_arm,
            right_arm,
        )

    def rotate(self, phi: float, center: Point) -> None:
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                point.move(-center)
                point.rotate(phi)
                point.move(center)

    def move(self, dx: float, dy: float) -> None:
        av = Point(dx, dy)
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                point.move(av)

    def scale(self, kx: float, ky: float, center: Point) -> None:
        for parts in self.anchor_pts:
            for point in parts[POINTS_INDEX]:
                point.move(-center)
                point.scale(Point(kx, ky))
                point.move(center)
