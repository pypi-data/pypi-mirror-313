from __future__ import annotations

from typing import Iterable, List, Tuple

import numpy as np
from svgpathtools import Arc as SvgPathToolsArc

from .ellipse import Ellipse
from .linebase import CurveLineBase, LineBase
from .point import Point, PointType


class Arc(CurveLineBase, Ellipse):
    """A class representing an arc."""

    #: The start point of the arc.
    start: Point
    #: The end point of the arc.
    end: Point
    #: Whether the arc is the large arc determined by the start and end points.
    large_arc: bool
    #: Whether the arc is the sweep arc determined by the start and end points.
    sweep: bool
    #: Whether to automatically scale the radius to fit the start and end points.
    autoscale_radius: bool

    def __init__(
        self,
        center: PointType,
        ra: float,
        rb: float,
        theta: float,
        start: PointType,
        end: PointType,
        large_arc: bool,
        sweep: bool,
        autoscale_radius: bool = True,
    ):
        """Create an arc.

        >>> Arc(center=Point(0.0, 0.0), ra=1.0, rb=1.0, theta=0.0, start=Point(1.0, 0.0), end=Point(0.0, 1.0), large_arc=False, sweep=True)
        Arc(center=Point(x=0.0, y=0.0), ra=1.0, rb=1.0, theta=0.0, start=Point(x=1.0, y=0.0), end=Point(x=0.0, y=1.0), large_arc=False, sweep=True)

        Args:
            center: The center of the arc.
            ra: The radius in the x direction.
            rb: The radius in the y direction.
            theta: The rotation of the arc in radians.
            start: The start point of the arc.
            end: The end point of the arc.
            large_arc: Whether the arc is the large arc determined by the start and end points.
            sweep: Whether the arc is the sweep arc determined by the start and end points.
            autoscale_radius: Whether to automatically scale the radius to fit the start and end points.
        """
        Ellipse.__init__(self, center, ra, rb, theta)
        self.start = Point.aspoint(start)
        self.end = Point.aspoint(end)
        self.large_arc = large_arc
        self.sweep = sweep
        self.autoscale_radius = autoscale_radius

    def __repr__(self) -> str:
        """Return a string representation of the arc."""
        return (
            f"{self.__class__.__name__}(center={self.center}, ra={self.ra}, rb={self.rb}, theta={self.theta}, "
            f"start={self.start}, end={self.end}, large_arc={self.large_arc}, sweep={self.sweep})"
        )

    def __eq__(self, other: "Arc") -> bool:
        """Return whether the arc is equal to another arc.

        >>> arc1 = Arc(Point(0.0, 0.0), 1.0, 1.0, 0.0, Point(1.0, 0.0), Point(0.0, 1.0), False, True)
        >>> arc2 = Arc(Point(0.0, 0.0), 1.0, 1.0, 0.0, Point(1.0, 0.0), Point(0.0, 1.0), False, True)
        >>> arc1 == arc2
        True
        """
        return (
            Ellipse.__eq__(self, other)
            and self.start == other.start
            and self.end == other.end
            and self.large_arc == other.large_arc
            and self.sweep == other.sweep
        )

    def __iter__(self):
        """Return an iterator over the arc.

        >>> arc = Arc(Point(0.0, 0.0), 1.0, 1.0, 0.0, Point(1.0, 0.0), Point(0.0, 1.0), False, True)
        >>> list(arc)
        [Point(x=1.0, y=0.0), Point(x=0.0, y=1.0)]
        """
        yield self.start
        yield self.end

    @classmethod
    def fromSvgPathToolsArc(cls, arc: SvgPathToolsArc) -> Arc:
        """Create an arc from a svgpathtools Arc."""
        return cls(
            center=Point(arc.center),
            ra=arc.radius.real,
            rb=arc.radius.imag,
            theta=np.deg2rad(arc.rotation),
            start=Point(arc.start),
            end=Point(arc.end),
            large_arc=arc.large_arc,
            sweep=arc.sweep,
        )

    @property
    def bbox(self) -> Tuple[Point, Point]:
        raise NotImplementedError

    def containsLine(self, line: LineBase | Iterable[LineBase]) -> bool:
        raise TypeError("Arc does not contain a line.")

    @property
    def boundaries(self) -> List[LineBase]:
        raise NotImplementedError
