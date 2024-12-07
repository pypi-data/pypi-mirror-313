from __future__ import annotations

from typing import Iterable

from .point import Point
from .straightline import ExtendedLineSegment


class Axis(ExtendedLineSegment):
    pass


class XAxis(Axis):
    #: X value of the first point.
    xstart: float
    #: X value of the second point.
    xend: float
    #: Y value of the axis.
    y: float

    def __init__(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(1.0, 0.0),
        xstart: float = 0.0,
        xend: float = 1.0,
        y: float = 0.0,
    ):
        super().__init__(start=start, end=end)
        self.setup(start=start, end=end, xstart=xstart, xend=xend, y=y)

    def setup(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(1.0, 0.0),
        xstart: float = 0.0,
        xend: float = 1.0,
        y: float = 0.0,
    ):
        """Set up the axis.

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            xstart: X value of the first point.
            xend: X value of the second point.
            y: Y value of the axis.
        """
        start, end = Point.aspoint(start), Point.aspoint(end)
        self.A, self.B, self.C = self.coefficientsFromTwoPoints(start, end)
        self.start, self.end = start, end
        self.xstart, self.xend = xstart, xend
        self.y = y


class YAxis(Axis):
    #: Y value of the first point.
    ystart: float
    #: Y value of the second point.
    yend: float
    #: X value of the axis.
    x: float

    def __init__(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(0.0, 1.0),
        ystart: float = 0.0,
        yend: float = 1.0,
        x: float = 0.0,
    ):
        super().__init__(start=start, end=end)
        self.setup(start=start, end=end, ystart=ystart, yend=yend, x=x)

    def setup(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(0.0, 1.0),
        ystart: float = 0.0,
        yend: float = 1.0,
        x: float = 0.0,
    ):
        """Set up the axis.

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            ystart: Y value of the first point.
            yend: Y value of the second point.
            x: X value of the axis.
        """
        start, end = Point.aspoint(start), Point.aspoint(end)
        self.A, self.B, self.C = self.coefficientsFromTwoPoints(start, end)
        self.start, self.end = start, end
        self.ystart, self.yend = ystart, yend
        self.x = x


class CoordinateSystem:
    #: The x-axis of the coordinate system.
    xaxis: XAxis
    #: The y-axis of the coordinate system.
    yaxis: YAxis

    def __init__(self):
        self.xaxis = XAxis()
        self.yaxis = YAxis()

    def transform(self, p: Point | Iterable[float] | complex) -> Point:
        """Transform the coordinate to the coordinate system.

        >>> csys = CoordinateSystem()
        >>> csys.transform(Point(0.0, 0.0))
        Point(x=0.0, y=0.0)
        >>> csys.transform(Point(1.0, 1.0))
        Point(x=1.0, y=1.0)

        >>> csys = CoordinateSystem()
        >>> csys.setup_xaxis(start=(0.0, 0.0), end=(2.0, 0.0), xstart=0.0, xend=1.0, y=0.0, check=False)
        >>> csys.setup_yaxis(start=(0.0, 0.0), end=(0.0, 2.0), ystart=0.0, yend=1.0, x=0.0, check=True)
        >>> csys.transform(Point(2.0, 0.0))
        Point(x=1.0, y=0.0)
        >>> csys.transform(Point(0.0, 2.0))
        Point(x=0.0, y=1.0)

        >>> csys = CoordinateSystem()
        >>> csys.setup_xaxis(start=(1.0, 0.0), end=(2.0, 0.0), xstart=0.0, xend=1.0, y=0.0, check=False)
        >>> csys.setup_yaxis(start=(0.0, 1.0), end=(0.0, 2.0), ystart=0.0, yend=1.0, x=0.0, perpendicular=True)
        >>> csys.transform(Point(2.0, 1.0))
        Point(x=1.0, y=0.0)
        >>> csys.transform(Point(1.0, 2.0))
        Point(x=0.0, y=1.0)

        >>> csys = CoordinateSystem()
        >>> csys.setup_xaxis(start=(0.0, 0.0), end=(1.0, 0.0), xstart=0.0, xend=1.0, y=0.0)
        >>> csys.setup_yaxis(start=(0.0, 0.0), end=(1.0, 1.0), ystart=0.0, yend=1.0, x=0.0, check=True)
        Traceback (most recent call last):
        ...
        ValueError: The x-axis and y-axis must be perpendicular.
        >>> csys.setup_yaxis(start=(0.0, 0.0), end=(0.0, 1.0), ystart=0.0, yend=1.0, x=0.0)
        >>> csys.setup_xaxis(start=(0.0, 0.0), end=(1.0, 1.0), xstart=0.0, xend=1.0, y=0.0, check=True)
        Traceback (most recent call last):
        ...
        ValueError: The x-axis and y-axis must be perpendicular.

        Args:
            p: The point to convert.

        Returns:
            The coordinate in the coordinate system.
        """
        xp = self.yaxis.parallel(p).intersect(self.xaxis)
        yp = self.xaxis.parallel(p).intersect(self.yaxis)
        rx = (xp.x - self.xaxis.start.x) / (self.xaxis.end.x - self.xaxis.start.x)
        ry = (yp.y - self.yaxis.start.y) / (self.yaxis.end.y - self.yaxis.start.y)
        x = self.xaxis.xstart + rx * (self.xaxis.xend - self.xaxis.xstart)
        y = self.yaxis.ystart + ry * (self.yaxis.yend - self.yaxis.ystart)
        x, y = round(x + 0.0, 10), round(y + 0.0, 10)
        return Point(x, y)

    def setup_xaxis(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(1.0, 0.0),
        xstart: float = 0.0,
        xend: float = 1.0,
        y: float = 0.0,
        perpendicular: bool = False,
        check: bool = False,
    ):
        """Set up the x-axis.

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            xstart: X value of the first point.
            xend: X value of the second point.
            y: Y value of the axis.
            perpendicular: If the axis should be perpendicular to the y-axis. If True, the y value of `end` will be
                           updated.
            check: Check if the axis is perpendicular to the y-axis.
        """
        start, end = Point.aspoint(start), Point.aspoint(end)
        if perpendicular:
            end = self.yaxis.perpendicular(start).intersect(self.yaxis.parallel(end))
        self.xaxis.setup(start=start, end=end, xstart=xstart, xend=xend, y=y)
        if check and not perpendicular and not self.xaxis.isPerpendicular(self.yaxis):
            raise ValueError("The x-axis and y-axis must be perpendicular.")

    def setup_yaxis(
        self,
        start: Point | Iterable[float] | complex = Point(0.0, 0.0),
        end: Point | Iterable[float] | complex = Point(0.0, 1.0),
        ystart: float = 0.0,
        yend: float = 1.0,
        x: float = 0.0,
        perpendicular: bool = False,
        check: bool = False,
    ):
        """Set up the y-axis.

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            ystart: Y value of the first point.
            yend: Y value of the second point.
            x: X value of the axis.
            perpendicular: If the axis should be perpendicular to the y-axis. If True, the x value of `end` will be
                           updated.
            check: Check if the axis is perpendicular to the y-axis.
        """
        start, end = Point.aspoint(start), Point.aspoint(end)
        if perpendicular:
            end = self.xaxis.perpendicular(start).intersect(self.xaxis.parallel(end))
        self.yaxis.setup(start=start, end=end, ystart=ystart, yend=yend, x=x)
        if check and not perpendicular and not self.yaxis.isPerpendicular(self.xaxis):
            raise ValueError("The x-axis and y-axis must be perpendicular.")
