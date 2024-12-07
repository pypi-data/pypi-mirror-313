from abc import ABC
from typing import List

from svgpathtools import CubicBezier as SvgPathToolsCubicBezier
from svgpathtools import QuadraticBezier as SvgPathToolsQuadraticBezier

from .linebase import CurveLineBase
from .point import Point, PointType


class Bezier(CurveLineBase, ABC):
    """A class representing a Bézier curve."""

    #: The start point of the quadratic Bézier curve.
    start: Point
    #: The control point of the quadratic Bézier curve.
    controls: List[Point]
    #: The end point of the quadratic Bézier curve.
    end: Point

    def __init__(self, start: PointType, controls: List[PointType], end: PointType):
        self.start = Point.aspoint(start)
        self.controls = [Point.aspoint(control) for control in controls]
        self.end = Point.aspoint(end)

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start}, controls={self.controls}, end={self.end})"

    def __iter__(self):
        yield self.start
        for control in self.controls:
            yield control
        yield self.end


class QuadraticBezier(Bezier):
    def __init__(self, start: PointType, control: PointType, end: PointType):
        super().__init__(start, [control], end)

    @classmethod
    def fromSvgPathToolsQuadraticBezier(cls, bezier: SvgPathToolsQuadraticBezier):
        return cls(Point(bezier.start), Point(bezier.control), Point(bezier.end))


class CubicBezier(Bezier):
    def __init__(self, start: PointType, control1: PointType, control2: PointType, end: PointType):
        super().__init__(start, [control1, control2], end)

    @classmethod
    def fromSvgPathToolsCubicBezier(cls, bezier: SvgPathToolsCubicBezier):
        return cls(Point(bezier.start), Point(bezier.control1), Point(bezier.control2), Point(bezier.end))
