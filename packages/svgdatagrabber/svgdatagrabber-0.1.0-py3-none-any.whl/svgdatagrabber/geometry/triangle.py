from __future__ import annotations

from .point import Point, PointType
from .polygon import Polygon


class Triangle(Polygon):
    """A class representing a triangle."""

    def __init__(self, *points: PointType):
        """Initialize a triangle.

        >>> Triangle(Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0))
        Triangle(Point(x=0.0, y=0.0), Point(x=1.0, y=0.0), Point(x=0.0, y=1.0))

        Args:
            *points: The points of the triangle.
        """
        if len(points) != 3:
            raise ValueError("A triangle must have exactly three points.")
        super().__init__(*points)

    @property
    def circumcenter(self) -> Point:
        """Return the circumcenter of the triangle.

        >>> Triangle(Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)).circumcenter
        Point(x=0.5, y=0.5)
        """
        a, b, c = self.vertices  # type: Point
        x = a.x * a.x + a.y * a.y
        y = b.x * b.x + b.y * b.y
        z = c.x * c.x + c.y * c.y
        s = a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)
        if abs(s) < self.tolerance:
            raise ValueError("The triangle is degenerate.")
        return Point(
            (x * (b.y - c.y) + y * (c.y - a.y) + z * (a.y - b.y)) / (2 * s),
            (x * (c.x - b.x) + y * (a.x - c.x) + z * (b.x - a.x)) / (2 * s),
        )
