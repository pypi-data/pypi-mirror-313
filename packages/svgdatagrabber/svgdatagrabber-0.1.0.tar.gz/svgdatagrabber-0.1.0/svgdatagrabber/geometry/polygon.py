from __future__ import annotations

from typing import Iterable, List, Tuple

from qtpy.QtCore import QPointF
from qtpy.QtGui import QPolygonF
from shapely.geometry import Polygon as ShapelyPolygon

from .closedshape import ClosedShape
from .geometrybase import DrawAsPolygon
from .linebase import LineBase
from .point import Point, PointType
from .sequence import PointSequence
from .straightline import LineRay, LineSegment


class Polygon(ClosedShape, PointSequence):
    """A class representing a polygon."""

    drawAs = DrawAsPolygon

    def __init__(self, *points: PointType):
        """Create a polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        Polygon(Point(x=0.0, y=0.0), Point(x=1.0, y=0.0), Point(x=1.0, y=1.0), Point(x=0.0, y=1.0))

        Args:
            points: The vertices of the polygon.
        """
        PointSequence.__init__(self, *points)

    def __repr__(self):
        """Return a string representation of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        Polygon(Point(x=0.0, y=0.0), Point(x=1.0, y=0.0), Point(x=1.0, y=1.0), Point(x=0.0, y=1.0))
        """
        return PointSequence.__repr__(self)

    def __eq__(self, other: Polygon) -> bool:
        """Check if two polygons are equal.

        >>> polygon1 = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        >>> polygon2 = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        >>> polygon1 == polygon2
        True
        """
        return PointSequence.__eq__(self, other)

    @property
    def isSimple(self) -> bool:
        """Check if the polygon is simple.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).isSimple
        True
        """
        return self.asShapely.is_simple

    @property
    def isValid(self):
        """Check if the polygon is convex."""
        return self.asShapely.is_valid

    def check(self):
        """Check if the polygon is valid."""
        assert len(self) >= 3, "A polygon must have at least three points."
        assert self.isSimple, "The polygon must be simple."

    @property
    def ndim(self) -> int:
        """Return the number of dimensions of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)).ndim
        3
        """
        return len(self)

    @property
    def vertices(self) -> List[Point]:
        """Return the vertices of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)).vertices
        [Point(x=0.0, y=0.0), Point(x=1.0, y=0.0), Point(x=1.0, y=1.0)]
        """
        return self.points

    @property
    def edges(self) -> List[LineSegment]:
        """Return the edges of the polygon.

        >>> edges = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)).edges
        >>> edges[0]
        LineSegment(start=Point(x=0.0, y=0.0), end=Point(x=1.0, y=0.0)) -> LineSegment(A=0.0, B=1.0, C=0.0)
        >>> edges[1]
        LineSegment(start=Point(x=1.0, y=0.0), end=Point(x=1.0, y=1.0)) -> LineSegment(A=1.0, B=0.0, C=-1.0)
        >>> edges[2]
        LineSegment(start=Point(x=1.0, y=1.0), end=Point(x=0.0, y=0.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)
        """
        starts, ends = self.vertices, self.vertices[1:] + self.vertices[:1]
        return [LineSegment(start=start, end=end) for start, end in zip(starts, ends)]

    @property
    def boundaries(self) -> List[LineBase]:
        """Return the boundaries of the polygon.

        >>> lines = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)).boundaries
        >>> lines[0]
        LineSegment(start=Point(x=0.0, y=0.0), end=Point(x=1.0, y=0.0)) -> LineSegment(A=0.0, B=1.0, C=0.0)
        >>> lines[1]
        LineSegment(start=Point(x=1.0, y=0.0), end=Point(x=1.0, y=1.0)) -> LineSegment(A=1.0, B=0.0, C=-1.0)
        >>> lines[2]
        LineSegment(start=Point(x=1.0, y=1.0), end=Point(x=0.0, y=0.0)) -> LineSegment(A=1.0, B=-1.0, C=0.0)
        """
        return self.edges

    def containsPoint(self, point: PointType | Iterable[Point]) -> bool:
        """Check if a point is inside the polygon.

        >>> polygon = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        >>> (Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)) in polygon
        True
        >>> Point(0.5, 0.5) in polygon
        True
        >>> (Point(0.5, 0.0), Point(0.5, 1.0), Point(0.0, 0.5), Point(1.0, 0.5)) in polygon
        True
        >>> Point(0.5, 1.5) in polygon
        False

        Args:
            point: A point or an iterable of points.
        """
        if isinstance(point, Iterable) and isinstance(tuple(point)[0], Point):
            return all(self.contains(p) for p in point)

        # Lie on the edges or vertices
        point = Point.aspoint(point)
        if self.inVertices(point) or self.inEdges(point):
            return True

        # LineRay casting
        ray = LineRay(start=point, end=Point(0, 0))
        intersections, intersecting_points = 0, PointSequence()
        for edge in self.edges:
            if ray.isIntersecting(edge):
                intersection = ray.intersect(edge)
                if intersection not in intersecting_points:
                    intersections += 1
                    intersecting_points.append(intersection)
        return intersections % 2 == 1

    def containsLine(self, line: LineBase | Iterable[LineBase]) -> bool:
        raise NotImplementedError

    def inEdges(self, item: PointType | Iterable[Point]) -> bool:
        """Check if a point is on the edges of the polygon.

        >>> polygon = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        >>> polygon.inEdges((Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)))
        True
        >>> polygon.inEdges((Point(0.5, 0.0), Point(0.5, 1.0), Point(0.0, 0.5), Point(1.0, 0.5)))
        True

        Args:
            item: A point or an iterable of points.
        """
        if isinstance(item, Iterable) and isinstance(tuple(item)[0], Point):
            return all(self.inEdges(p) for p in item)
        point = Point.aspoint(item)
        return any(point in edge for edge in self.edges)

    def inVertices(self, item: PointType | Iterable[Point]) -> bool:
        """Check if a point is on the vertices of the polygon.

        >>> polygon = Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0))
        >>> polygon.inVertices((Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)))
        True

        Args:
            item: A point or an iterable of points.
        """
        if isinstance(item, Iterable) and isinstance(tuple(item)[0], Point):
            return all(self.inVertices(p) for p in item)
        point = Point.aspoint(item)
        return any(point == vertex for vertex in self.vertices)

    @property
    def maxsize(self) -> float:
        """Return the maximum size of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(2.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).maxsize
        2.0
        """
        lf, tr = self.bbox
        return max(tr.x - lf.x, tr.y - lf.y)

    @property
    def area(self) -> float:
        """Return the area of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).area
        1.0
        """
        v1, v2 = self.vertices, self.vertices[1:] + self.vertices[:1]
        return abs(sum((p1.x - p2.x) * (p1.y + p2.y) for p1, p2 in zip(v1, v2))) / 2

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the polygon.

        >>> assert Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).perimeter == 4.0
        """
        return sum(edge.length for edge in self.edges)

    @property
    def centroid(self) -> Point:
        """Return the centroid of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).centroid
        Point(x=0.5, y=0.5)
        """
        v1, v2 = self.vertices, self.vertices[1:] + self.vertices[:1]
        x = abs(sum((p1.x + p2.x) * (p1.x * p2.y - p2.x * p1.y) for p1, p2 in zip(v1, v2))) / (6 * self.area)
        y = abs(sum((p1.y + p2.y) * (p1.x * p2.y - p2.x * p1.y) for p1, p2 in zip(v1, v2))) / (6 * self.area)
        return Point(x, y)

    @property
    def bbox(self) -> Tuple[Point, Point]:
        """Return the bounding box of the polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).bbox
        (Point(x=0.0, y=0.0), Point(x=1.0, y=1.0))
        """
        x, y = zip(*self.vertices)
        return Point(min(x), min(y)), Point(max(x), max(y))

    @property
    def asShapely(self) -> ShapelyPolygon:
        """Return the polygon as a Shapely polygon.

        >>> Polygon(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)).asShapely
        <POLYGON ...>
        """
        return ShapelyPolygon(((vertex.x, vertex.y) for vertex in self.vertices))

    @property
    def drawArgs(self) -> Tuple[QPolygonF]:
        """Return the polygon as a Qt polygon."""
        return (QPolygonF([QPointF(vertex.x, vertex.y) for vertex in self.vertices]),)
