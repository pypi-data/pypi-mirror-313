from __future__ import annotations

from abc import ABC
from typing import Iterable, List, Tuple

from .geometrybase import GeometryBase
from .linebase import LineBase
from .point import Point


class ClosedShape(GeometryBase, ABC):
    """Base class for closed shapes."""

    def __eq__(self, other: "ClosedShape") -> bool:
        raise NotImplementedError

    def __contains__(self, item: GeometryBase | Iterable["GeometryBase"]) -> bool:
        """Check if a point or shape is inside the shape."""
        return self.contains(item)

    def contains(self, item: GeometryBase | Iterable["GeometryBase"]) -> bool:
        """Check if a point or shape is inside the shape."""
        if isinstance(item, Point):
            return self.containsPoint(item)
        elif isinstance(item, LineBase):
            return self.containsLine(item)
        elif isinstance(item, ClosedShape):
            return all(self.containsLine(line) for line in item.boundaries)
        elif isinstance(item, Iterable):
            return all(self.contains(subitem) for subitem in item)
        else:
            raise TypeError(f"Unsupported type: {type(item)}")

    @property
    def boundaries(self) -> List[LineBase]:
        """Return the boundaries of the shape. To decide whether the shape is inside another shape."""
        raise NotImplementedError

    def containsPoint(self, point: Point | Iterable[Point]) -> bool:
        """Check if a point is inside the shape."""
        raise NotImplementedError

    def containsLine(self, line: LineBase | Iterable[LineBase]) -> bool:
        """Check if a line is inside the shape."""
        raise NotImplementedError

    @property
    def area(self) -> float:
        """Return the area of the shape."""
        raise NotImplementedError

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        raise NotImplementedError

    @property
    def centroid(self) -> Point:
        """Return the centroid of the shape."""
        raise NotImplementedError

    @property
    def bbox(self) -> Tuple[Point, Point]:
        """Return the bounding box of the shape."""
        raise NotImplementedError
