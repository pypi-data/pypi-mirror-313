from __future__ import annotations

from typing import Iterator

import numpy as np
from qtpy.QtCore import QLineF
from svgpathtools import Line as SvgPathToolsLine

from .exceptions import NotDrawableGeometryError
from .linebase import StraightLineBase
from .point import Point, PointType, Vector


class Line(StraightLineBase):
    """A class representing a line."""

    #: Coefficient of the x term.
    A: float
    #: Coefficient of the y term.
    B: float
    #: Constant term.
    C: float

    def __init__(
        self,
        start: PointType = None,
        end: PointType = None,
        A: float = None,
        B: float = None,
        C: float = None,
        slope: float = None,
        angle: float = None,
        intercept: float = None,
    ):
        """Create a line. Possible ways to create a line (in order of precedence):

        - start and end points (start and end)
        - coefficients A, B, C (A, B and C)
        - start point and slope (start and slope)
        - start point and angle (start and angle)
        - slope and intercept (slope and intercept)
        - angle and intercept (angle and intercept)

        >>> Line(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(A=1.0, B=-1.0, C=0.0)
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(start=Point(0.0, 0.0), slope=1.0)
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(start=Point(0.0, 0.0), angle=np.pi / 4.0)
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(slope=1.0, intercept=0.0)
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(angle=np.pi / 4.0, intercept=0.0)
        Line(A=1.0, B=-1.0, C=0.0)

        >>> Line(start=Point(0.0, 0.0))
        Traceback (most recent call last):
        ...
        ValueError: Not enough information to create a line.

        Args:
            start: The start point of the line.
            end: The end point of the line.
            A: The coefficient of the x term.
            B: The coefficient of the y term.
            C: The constant term.
            slope: The slope of the line.
            intercept: The y-intercept of the line.
        """
        if start is not None and end is not None:
            A, B, C = self.coefficientsFromTwoPoints(start, end)
        elif A is not None and B is not None and C is not None:
            A, B, C = self.standardizeCoefficients(A, B, C)
        elif start is not None and slope is not None:
            A, B, C = self.coefficientsFromPointAndSlope(start, slope)
        elif start is not None and angle is not None:
            A, B, C = self.coefficientsFromPointAndAngle(start, angle)
        elif slope is not None and intercept is not None:
            A, B, C = self.coefficientsFromSlopeAndIntercept(slope, intercept)
        elif angle is not None and intercept is not None:
            A, B, C = self.coefficientsFromAngleAndIntercept(angle, intercept)
        else:
            raise ValueError("Not enough information to create a line.")
        self.A, self.B, self.C = A, B, C

    def __repr__(self) -> str:
        """Return the representation of the line.

        >>> Line(A=1.0, B=-1.0, C=0.0)
        Line(A=1.0, B=-1.0, C=0.0)
        """
        A, B, C = round(self.A, 10), round(self.B, 10), round(self.C, 10)
        return f"{self.__class__.__name__}(A={A}, B={B}, C={C})"

    def __eq__(self, other: Line) -> bool:
        """Return whether the line is equal to another line.

        >>> Line(A=1.0, B=1.0, C=0.0) == Line(A=-1.0, B=-1.0, C=0.0)
        True
        >>> Line(A=1.0, B=1.0, C=0.0) == Line(A=1.0, B=2.0, C=1.0)
        False
        """
        return np.allclose([self.A, self.B, self.C], [other.A, other.B, other.C], atol=self.tolerance)

    def __contains__(self, p: PointType) -> bool:
        """Check if a point is on this line.

        >>> Point(0.0, 0.0) in Line(A=-1.0, B=1.0, C=0.0)
        True
        >>> Point(0.0, 0.0) not in Line(A=-1.0, B=1.0, C=0.0)
        False
        >>> Point(1.0, 0.0) in Line(A=-1.0, B=1.0, C=0.0)
        False
        >>> Point(1.0, 0.0) not in Line(A=-1.0, B=1.0, C=0.0)
        True

        Returns:
            True if the point is on this line, otherwise False.
        """
        p = Point.aspoint(p)
        return self.distance(p) < self.tolerance

    @classmethod
    def standardizeCoefficients(cls, A: float, B: float, C: float) -> tuple[float, float, float]:
        """Standardize the coefficients of a line.

        >>> Line.standardizeCoefficients(1.0, -1.0, 0.0)
        (1.0, -1.0, 0.0)
        >>> Line.standardizeCoefficients(-1.0, -1.0, 1.0)
        (1.0, 1.0, -1.0)

        Args:
            A: The coefficient of the x term.
            B: The coefficient of the y term.
            C: The constant term.

        Returns:
            The standardized coefficients.
        """
        if A != 0.0:
            A, B, C = 1.0, B / A, C / A
        elif B != 0.0:
            B, C = 1.0, C / B
        A, B, C = round(A + 0.0, 10), round(B + 0.0, 10), round(C + 0.0, 10)  # Prevent -0.0 and convert to float
        return A, B, C

    @classmethod
    def fromCoefficients(cls, A: float, B: float, C: float) -> Line:
        """Create a line from the coefficients.

        >>> Line.fromCoefficients(1.0, -1.0, 0.0)
        Line(A=1.0, B=-1.0, C=0.0)

        Args:
            A: The coefficient of the x term.
            B: The coefficient of the y term.
            C: The constant term.

        Returns:
            The created line.
        """
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return cls(A=A, B=B, C=C)

    @classmethod
    def coefficientsFromTwoPoints(cls, p1: PointType, p2: PointType) -> tuple[float, float, float]:
        """Get the coefficients of a line from two points.

        >>> Line.coefficientsFromTwoPoints(Point(0.0, 0.0), Point(1.0, 1.0))
        (1.0, -1.0, 0.0)

        Args:
            p1: The first point.
            p2: The second point.

        Returns:
            The coefficients of the line.
        """
        p1, p2 = Point.aspoint(p1), Point.aspoint(p2)
        A = p1.y - p2.y
        B = p2.x - p1.x
        C = p1.x * p2.y - p2.x * p1.y
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return A, B, C

    @classmethod
    def fromTwoPoints(cls, start: PointType, end: PointType) -> Line:
        """Create a line from two points.

        >>> Line.fromTwoPoints(Point(0.0, 0.0), Point(1.0, 1.0))
        Line(A=1.0, B=-1.0, C=0.0)

        Args:
            start: The first point.
            end: The second point.

        Returns:
            The created line.
        """
        start, end = Point.aspoint(start), Point.aspoint(end)
        A, B, C = cls.coefficientsFromTwoPoints(start, end)
        return cls.fromCoefficients(A=A, B=B, C=C)

    @classmethod
    def coefficientsFromPointAndSlope(cls, p: PointType, slope: float) -> tuple[float, float, float]:
        """Get the coefficients of a line from a point and a slope.

        >>> Line.coefficientsFromPointAndSlope(Point(0.0, 0.0), 1.0)
        (1.0, -1.0, 0.0)

        Args:
            p: The point.
            slope: The slope.

        Returns:
            The coefficients of the line.
        """
        p = Point.aspoint(p)
        A = slope
        B = -1.0
        C = p.y - slope * p.x
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return A, B, C

    @classmethod
    def fromPointAndSlope(cls, start: PointType, slope: float) -> Line:
        """Create a line from a point and a slope.

        >>> Line.fromPointAndSlope(Point(0.0, 0.0), 1.0)
        Line(A=1.0, B=-1.0, C=0.0)

        Args:
            start: The point.
            slope: The slope.

        Returns:
            The created line.
        """
        start = Point.aspoint(start)
        A, B, C = cls.coefficientsFromPointAndSlope(start, slope)
        return cls.fromCoefficients(A=A, B=B, C=C)

    @classmethod
    def coefficientsFromPointAndAngle(cls, p: PointType, angle: float) -> tuple[float, float, float]:
        """Get the coefficients of a line from a point and an angle.

        >>> assert Line.coefficientsFromPointAndAngle(Point(0.0, 0.0), np.pi / 4.0) == (1.0, -1.0, 0.0)

        Args:
            p: The point.
            angle: The angle.

        Returns:
            The coefficients of the line.
        """
        p = Point.aspoint(p)
        A = np.cos(angle)
        B = -np.sin(angle)
        C = B * p.y - A * p.x
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return A, B, C

    @classmethod
    def fromPointAndAngle(cls, start: PointType, angle: float) -> Line:
        """Create a line from a point and an angle.

        >>> Line.fromPointAndAngle(Point(0.0, 0.0), np.pi / 4.0)
        Line(A=1.0, B=-1.0, C=0.0)

        Args:
            start: The point.
            angle: The angle.

        Returns:
            The created line.
        """
        start = Point.aspoint(start)
        A, B, C = cls.coefficientsFromPointAndAngle(start, angle)
        return cls.fromCoefficients(A=A, B=B, C=C)

    @classmethod
    def coefficientsFromSlopeAndIntercept(cls, slope: float, intercept: float) -> tuple[float, float, float]:
        """Get the coefficients of a line from a slope and an intercept.

        >>> Line.coefficientsFromSlopeAndIntercept(1.0, 0.0)
        (1.0, -1.0, 0.0)

        Args:
            slope: The slope.
            intercept: The intercept.

        Returns:
            The coefficients of the line.
        """
        A = slope
        B = -1.0
        C = intercept
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return A, B, C

    @classmethod
    def fromSlopeAndIntercept(cls, slope: float, intercept: float) -> Line:
        """Create a line from a slope and intercept.

        >>> Line.fromSlopeAndIntercept(1.0, 0.0)
        Line(A=1.0, B=-1.0, C=0.0)

        Args:
            slope: The slope.
            intercept: The intercept.

        Returns:
            The created line.
        """
        A, B, C = cls.coefficientsFromSlopeAndIntercept(slope, intercept)
        return cls.fromCoefficients(A=A, B=B, C=C)

    @classmethod
    def coefficientsFromAngleAndIntercept(cls, angle: float, intercept: float) -> tuple[float, float, float]:
        """Get the coefficients of a line from an angle and an intercept.

        >>> assert Line.coefficientsFromAngleAndIntercept(np.pi / 4.0, 0.0) == (1.0, -1.0, 0.0)

        Args:
            angle: The angle.
            intercept: The intercept.

        Returns:
            The coefficients of the line.
        """
        A = np.cos(angle)
        B = -np.sin(angle)
        C = intercept * np.sin(angle)
        A, B, C = cls.standardizeCoefficients(A, B, C)
        return A, B, C

    @classmethod
    def fromAngleAndIntercept(cls, angle: float, intercept: float) -> Line:
        """Create a line from an angle and intercept.

        >>> assert Line.fromAngleAndIntercept(np.pi / 4.0, 0.0) == Line(A=1.0, B=-1.0, C=0.0)

        Args:
            angle: The angle.
            intercept: The intercept.

        Returns:
            The created line.
        """
        A, B, C = cls.coefficientsFromAngleAndIntercept(angle, intercept)
        return cls.fromCoefficients(A=A, B=B, C=C)

    @property
    def maxsize(self) -> float:
        raise ValueError("Line does not have a maxsize.")

    def distance(self, p: Point) -> float:
        """Get the distance between a point and this line.

        >>> line = Line(A=1.0, B=1.0, C=0.0)
        >>> point = Point(1.0, 1.0)
        >>> assert np.isclose(line.distance(point), np.sqrt(2.0))

        Args:
            p: The point to get the distance to.

        Returns:
            The distance between the point and this line.
        """
        p = Point.aspoint(p)
        return abs(self.A * p.x + self.B * p.y + self.C) / np.sqrt(self.A**2 + self.B**2)

    @property
    def slope(self) -> float:
        """Get the slope of this line.

        >>> assert Line(A=1.0, B=-1.0, C=0.0).slope == 1.0
        >>> assert Line(A=1.0, B=1.0, C=0.0).slope == -1.0
        >>> assert Line(A=1.0, B=0.0, C=0.0).slope == np.inf

        Returns:
            The slope of this line.
        """
        if abs(self.B) < self.tolerance:
            return np.inf if self.A > 0 else -np.inf
        return -self.A / self.B

    @property
    def angle(self) -> float:
        """Get the angle of this line.

        >>> angle = Line(A=1.0, B=1.0, C=0.0).angle
        >>> assert np.isclose(angle, -np.pi / 4.0)

        Returns:
            The angle of this line.
        """
        return np.arctan2(-self.A, self.B) + 0.0

    def angleBetween(self, other: Line) -> float:
        """Get the angle between this line and another line.

        >>> line1 = Line(A=1.0, B=1.0, C=0.0)
        >>> line2 = Line(A=1.0, B=-1.0, C=0.0)
        >>> assert line1.angleBetween(line2) == np.pi / 2.0

        Args:
            other: The other line.

        Returns:
            The angle between the two lines.
        """
        return np.arctan2(self.A * other.B - self.B * other.A, self.A * other.A + self.B * other.B) % np.pi + 0.0

    @property
    def intercept(self) -> float:
        """Get the intercept of this line.

        >>> assert Line(A=1.0, B=1.0, C=1.0).intercept == -1.0
        >>> Line(A=1.0, B=0.0, C=0.0).intercept
        Traceback (most recent call last):
        ...
        ValueError: The line is vertical and has no intercept.

        Returns:
            The intercept of this line.
        """
        if abs(self.B) < self.tolerance:
            raise ValueError("The line is vertical and has no intercept.")
        return self.gety(0.0)

    def getx(self, y: float) -> float:
        """Get the x coordinate of a point on this line.

        >>> assert Line(A=1.0, B=1.0, C=0.0).getx(1.0) == -1.0
        >>> Line(A=0.0, B=1.0, C=0.0).getx(0.0)
        Traceback (most recent call last):
        ...
        ValueError: Line is vertical

        Args:
            y: The y coordinate of the point.

        Returns:
            The x coordinate of the point.
        """
        if abs(self.A) < self.tolerance:
            raise ValueError("Line is vertical")
        return -(self.B * y + self.C) / self.A

    def gety(self, x: float) -> float:
        """Get the y coordinate of a point on this line.

        >>> assert Line(A=1.0, B=1.0, C=0.0).gety(1.0) == -1.0
        >>> Line(A=1.0, B=0.0, C=0.0).gety(0.0)
        Traceback (most recent call last):
        ...
        ValueError: Line is horizontal

        Args:
            x: The x coordinate of the point.

        Returns:
            The y coordinate of the point.
        """
        if abs(self.B) < self.tolerance:
            raise ValueError("Line is horizontal")
        return -(self.A * x + self.C) / self.B

    def isParallel(self, line: "Line") -> bool:
        """Check if this line is parallel to another line.

        >>> Line(A=1.0, B=1.0, C=0.0).isParallel(Line(A=1.0, B=1.0, C=1.0))
        True
        >>> Line(A=1.0, B=1.0, C=0.0).isParallel(Line(A=-1.0, B=1.0, C=1.0))
        False

        Args:
            line: The line to check.

        Returns:
            True if the lines are parallel, otherwise False.
        """
        return abs(self.A * line.B - self.B * line.A) < self.tolerance

    def isIntersecting(self, line: "Line") -> bool:
        """Check if this line is intersecting another line.

        >>> Line(A=1.0, B=1.0, C=0.0).isIntersecting(Line(A=1.0, B=1.0, C=1.0))
        False
        >>> Line(A=1.0, B=1.0, C=0.0).isIntersecting(Line(A=-1.0, B=1.0, C=1.0))
        True

        Args:
            line: The line to check.

        Returns:
            True if the lines are intersecting, otherwise False.
        """
        try:
            self.intersect(line)
            return True
        except AssertionError:
            return False

    def isPerpendicular(self, line: "Line") -> bool:
        """Check if this line is perpendicular to another line.

        >>> Line(A=1.0, B=1.0, C=0.0).isPerpendicular(Line(A=1.0, B=1.0, C=1.0))
        False
        >>> Line(A=1.0, B=1.0, C=0.0).isPerpendicular(Line(A=-1.0, B=1.0, C=1.0))
        True

        Args:
            line: The line to check.

        Returns:
            True if the lines are perpendicular, otherwise False.
        """
        return abs(self.A * line.A + self.B * line.B) < self.tolerance

    def intersect(self, line: "Line") -> Point:
        """Get the intersection point between this line and another line.

        >>> Line(A=1.0, B=1.0, C=-1.0).intersect(Line(A=1.0, B=-1.0, C=1.0))
        Point(x=0.0, y=1.0)
        >>> Line(A=1.0, B=1.0, C=0.0).intersect(Line(A=1.0, B=1.0, C=1.0))
        Traceback (most recent call last):
        ...
        AssertionError: Lines are parallel.

        Args:
            line: The line to intersect with.

        Returns:
            The intersection point if there is one, otherwise None.
        """
        assert not self.isParallel(line), "Lines are parallel."
        A = np.asarray([[self.A, self.B], [line.A, line.B]])
        b = np.asarray([-self.C, -line.C])
        x, y = np.linalg.solve(A, b)
        p = Point(x, y)
        assert getattr(self, "extended", False) or p in self and p in line, "Lines do not intersect."
        return p

    def parallel(self, p: PointType) -> "Line":
        """Get a parallel line to this line.

        >>> assert Line(A=1.0, B=-1.0, C=0.0).parallel(Point(0.0, 1.0)) == Line(A=1.0, B=-1.0, C=1.0)

        Args:
            p: A point on the parallel line.

        Returns:
            A parallel line to this line.
        """
        p = Point.aspoint(p)
        return Line(A=self.A, B=self.B, C=-self.A * p.x - self.B * p.y)

    def perpendicular(self, p: PointType) -> "Line":
        """Get a perpendicular line to this line.

        >>> assert Line(A=1.0, B=-1.0, C=0.0).perpendicular(Point(0.0, 1.0)) == Line(A=1.0, B=1.0, C=-1.0)
        >>> assert Line(A=0.0, B=1.0, C=0.0).perpendicular(Point(0.0, 0.0)) == Line(A=1.0, B=0.0, C=0.0)
        >>> assert Line(A=1.0, B=0.0, C=0.0).perpendicular(Point(0.0, 0.0)) == Line(A=0.0, B=1.0, C=0.0)

        Args:
            p: A point on the perpendicular line.

        Returns:
            A perpendicular line to this line.
        """
        p = Point.aspoint(p)
        return Line(A=self.B, B=-self.A, C=-self.B * p.x + self.A * p.y)

    @property
    def drawArgs(self):
        raise NotDrawableGeometryError


class LineSegment(Line):
    """A class representing a line segment."""

    #: The first point to create the line.
    start: Point
    #: The second point to create the line.
    end: Point
    #: Whether to extend the segment to infinity, used to check if a point is on the extended segment.
    extended: bool

    def __init__(
        self,
        start: PointType,
        end: PointType,
        extended: bool = False,
    ):
        """Create a new line segment.

        >>> LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        LineSegment(start=Point(x=0.0, y=0.0), end=Point(x=1.0, y=1.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            extended: Whether to extend the segment to infinity, used to check if a point is on the extended segment.
        """
        super().__init__(start=start, end=end)
        self.start, self.end = Point.aspoint(start), Point.aspoint(end)
        self.extended = extended

    def __repr__(self):
        """Get the string representation of this line segment.

        >>> repr(LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0)))
        'LineSegment(start=Point(x=0.0, y=0.0), end=Point(x=1.0, y=1.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)'
        """
        return f"{self.__class__.__name__}(start={self.start}, end={self.end}) -> {super().__repr__()}"

    def __eq__(self, other: LineSegment) -> bool:
        """Check if this line segment is equal to another line segment.

        >>> segment1 = LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        >>> segment2 = LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        >>> segment1 == segment2
        True
        >>> segment3 = LineSegment(start=Point(0.0, 0.0), end=Point(2.0, 2.0))
        >>> segment1 == segment3
        False

        Args:
            other: The line segment to check.
        """
        return super().__eq__(other) and (
            (self.start == other.start and self.end == other.end)
            or (self.start == other.end and self.end == other.start)
        )

    def __contains__(self, p: PointType) -> bool:
        """Check if a point is on this segment.

        >>> Point(0.0, 0.0) in LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(1.0, 1.0) in LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(0.5, 0.5) in LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(0.0, 1.0) in LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        False

        Returns:
            True if the point is on this segment, otherwise False.
        """
        p = Point.aspoint(p)
        minx, maxx = sorted([self.start.x, self.end.x])
        miny, maxy = sorted([self.start.y, self.end.y])
        return super().__contains__(p) and (self.extended or (minx <= p.x <= maxx and miny <= p.y <= maxy))

    def __iter__(self) -> Iterator[Point]:
        """Iterate over the points of this segment.

        >>> list(LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0)))
        [Point(x=0.0, y=0.0), Point(x=1.0, y=1.0)]
        """
        yield self.start
        yield self.end

    @classmethod
    def fromSvgPathToolsLine(cls, line: SvgPathToolsLine):
        """Create a new line segment from a SvgPathTools line.

        >>> LineSegment.fromSvgPathToolsLine(SvgPathToolsLine(start=.0j, end=1.0+1.0j))
        LineSegment(start=Point(x=0.0, y=0.0), end=Point(x=1.0, y=1.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)

        Args:
            line: The SvgPathTools line to create the line segment from.

        Returns:
            A new line segment.
        """
        return cls(start=line.start, end=line.end)

    @property
    def maxsize(self) -> float:
        """Get the maximal size of this segment.

        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(3.0, 4.0)).maxsize == 5.0
        """
        return self.length

    @property
    def length(self) -> float:
        """Get the length of this segment.

        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(3.0, 4.0)).length == 5.0

        Returns:
            The length of this segment.
        """
        return self.start.distance(self.end)

    @property
    def direction(self) -> float:
        """Get the direction of this segment.

        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0)).direction - np.pi / 4 == 0.0
        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(-1.0, 1.0)).direction - 3.0 * np.pi / 4 == 0.0
        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(-1.0, -1.0)).direction + 3.0 * np.pi / 4.0 == 0.0
        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(1.0, -1.0)).direction + np.pi / 4.0 == 0.0

        Returns:
            The direction of this segment.
        """
        return self.start.direction(self.end)

    @property
    def midpoint(self) -> Point:
        """Get the midpoint of this segment.

        >>> assert LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0)).midpoint == Point(x=0.5, y=0.5)

        Returns:
            The midpoint of this segment.
        """
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    def reverse(self) -> "LineSegment":
        """Reverse the direction of this segment.

        >>> LineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0)).reverse()
        LineSegment(start=Point(x=1.0, y=1.0), end=Point(x=0.0, y=0.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)
        """
        self.start, self.end = self.end, self.start
        return self

    @property
    def drawArgs(self) -> QLineF:
        """Get the Qt representation of this line segment."""
        return QLineF(self.start.x, self.start.y, self.end.x, self.end.y)


class ExtendedLineSegment(LineSegment):
    """A class representing an extended line segment."""

    def __init__(self, start: PointType, end: PointType):
        """Create a new extended line segment.

        >>> segment = ExtendedLineSegment(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        >>> assert segment.extended

        Args:
            start: The start point of the segment.
            end: The end point of the segment.
        """
        super().__init__(start=start, end=end, extended=True)


class LineRay(Line):
    """A class representing a line ray."""

    #: The first point to create the line.
    start: Point
    #: The second point to create the line.
    end: Point
    #: Whether to extend the ray to infinity, used to check if a point is on the extended ray.
    extended: bool

    def __init__(
        self,
        start: PointType,
        end: PointType,
        extended: bool = False,
    ):
        """Create a ray.

        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        LineRay(start=Point(x=0.0, y=0.0), slope=1.0) -> LineRay(A=1.0, B=-1.0, C=0.0)

        Args:
            start: The first point to create the line.
            end: The second point to create the line.
            extended: Whether to extend the ray to infinity, used to check if a point is on the extended ray.
        """
        super().__init__(start=start, end=end)
        self.start, self.end = Point.aspoint(start), Point.aspoint(end)
        self.direction = self.end - self.start
        self.extended = extended

    def __repr__(self):
        """Get the string representation of this ray.

        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        LineRay(start=Point(x=0.0, y=0.0), slope=1.0) -> LineRay(A=1.0, B=-1.0, C=0.0)
        """
        slope = round(self.slope, 10)
        return f"{self.__class__.__name__}(start={self.start}, slope={slope}) -> {super().__repr__()}"

    def __eq__(self, other: LineRay) -> bool:
        """Check if two rays are equal.

        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0)) == LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0)) == LineRay(start=Point(0.0, 0.0), end=Point(2.0, 2.0))
        True
        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0)) == LineRay(start=Point(-1.0, -1.0), end=Point(1.0, 1.0))
        False
        """
        return super().__eq__(other) and self.start == other.start

    def __contains__(self, p: PointType):
        """Check if a point is on this ray.

        >>> Point(0.0, 0.0) in LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(0.5, 0.5) in LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(1.0, 1.0) in LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(2.0, 2.0) in LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        True
        >>> Point(-1.0, -1.0) in LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        False

        Returns:
            True if the point is on this ray, otherwise False.
        """
        return super().__contains__(p) and (self.extended or self.start.vector(p) @ self.slope_vector >= 0)

    @property
    def slope_vector(self) -> Vector:
        """Get the slope vector of this ray.

        >>> LineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0)).slope_vector
        Vector(x=1.0, y=1.0)

        Returns:
            The slope vector of this ray.
        """
        return Vector.asvector(self.end - self.start)


class ExtendedLineRay(LineRay):
    """A class representing an extended line ray."""

    def __init__(self, start: PointType, end: PointType):
        """Create an extended ray.

        >>> ray = ExtendedLineRay(start=Point(0.0, 0.0), end=Point(1.0, 1.0))
        >>> assert ray.extended

        Args:
            start: The first point to create the ray.
            end: The second point to create the ray.
        """
        super().__init__(start=start, end=end, extended=True)
