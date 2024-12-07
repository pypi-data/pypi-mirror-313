from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, List, Sequence, Union, overload

from .geometrybase import GeometryBase
from .point import Point, PointType
from .straightline import Line

SequenceItem = Union[GeometryBase, Point, Line]
SequenceItemType = Union[GeometryBase, PointType, Line]


class GeometrySequence(Sequence[GeometryBase]):
    """A class representing a sequence of geometries."""

    #: Items in the sequence.
    items: List[SequenceItem]

    def __init__(self, *items: SequenceItemType):
        """Create a sequence of items.

        >>> GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))
        GeometrySequence(Point(x=1.0, y=2.0), Point(x=3.0, y=4.0))

        Args:
            items: The items to add to the sequence.
        """
        self.items = list(self.asitem(item) for item in items)
        self.check()

    def __repr__(self) -> str:
        """Return a string representation of the sequence.

        >>> repr(GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0)))
        'GeometrySequence(Point(x=1.0, y=2.0), Point(x=3.0, y=4.0))'
        """
        return f"{self.__class__.__name__}({', '.join(repr(p) for p in self.items)})"

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> SequenceItem: ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence[SequenceItem]: ...

    def __getitem__(self, index: int) -> SequenceItem | Sequence[SequenceItem]:
        """Get a point from the sequence.

        >>> GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))[0]
        Point(x=1.0, y=2.0)
        >>> GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))[1]
        Point(x=3.0, y=4.0)
        >>> GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))[0:1]
        [Point(x=1.0, y=2.0)]

        Args:
            index: The index of the item to get.
        """
        return self.items[index]

    def __setitem__(self, key: int, value: SequenceItemType):
        """Set a point in the sequence.

        >>> ps = GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))
        >>> ps[1] = Point(5.0, 6.0)
        >>> ps
        GeometrySequence(Point(x=1.0, y=2.0), Point(x=5.0, y=6.0))
        """
        self.items[key] = self.asitem(value)

    def __len__(self) -> int:
        """Return the length of the sequence.

        >>> len(GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0)))
        2
        """
        return len(self.items)

    def __iter__(self) -> Iterable[GeometryBase]:
        """Return an iterator over the items.

        >>> list(GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0)))
        [Point(x=1.0, y=2.0), Point(x=3.0, y=4.0)]
        """
        return iter(self.items)

    def __reversed__(self):
        """Return a reversed iterator over the items.

        >>> list(reversed(GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))))
        [Point(x=3.0, y=4.0), Point(x=1.0, y=2.0)]
        """
        return reversed(self.items)

    def __eq__(self, other: "GeometrySequence") -> bool:
        """Check if two polygons are equal.

        >>> ps1 = GeometrySequence(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0))
        >>> ps2 = GeometrySequence(Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0))
        >>> ps1 == ps2
        True
        """
        return all(v1 == v2 for v1, v2 in zip(self.items, other.items))

    def __contains__(self, item: SequenceItem | Iterable[SequenceItem]) -> bool:
        """Check if an item is in the sequence.

        >>> Point(1.0, 2.0) in GeometrySequence(Point(0.0, 0.0), Point(1.0, 2.0))
        True
        >>> (Point(1.0, 2.0), Point(3.0, 4.0)) in GeometrySequence(Point(0.0, 0.0), Point(1.0, 2.0))
        False
        >>> (Point(1.0, 2.0), Point(3.0, 4.0)) in GeometrySequence(Point(0.0, 0.0), Point(1.0, 2.0), Point(3.0, 4.0))
        True
        """
        if isinstance(item, Iterable) and isinstance(tuple(item)[0], Point):
            return all(p in self.items for p in item)
        return self.asitem(item) in self.items

    def check(self):
        """Check if the sequence is valid."""
        pass

    @classmethod
    def asitem(cls, item: SequenceItemType) -> SequenceItem:
        """Prepare an item for adding to the sequence, if necessary.

        >>> GeometrySequence.asitem(Point(1.0, 2.0))
        Point(x=1.0, y=2.0)
        """
        return item

    def append(self, item: SequenceItemType) -> None:
        """Add a point to the sequence.

        >>> ps = GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))
        >>> ps.append(Point(5.0, 6.0))
        >>> ps
        GeometrySequence(Point(x=1.0, y=2.0), Point(x=3.0, y=4.0), Point(x=5.0, y=6.0))
        """
        self.items.append(self.asitem(item))

    def index(self, item: SequenceItemType, start: int = 0, stop: int = None) -> int:
        """Find the index of a point in the sequence.

        >>> ps = GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0))
        >>> ps.index(Point(3.0, 4.0))
        1

        Args:
            item: The item to find.
            start: The start index.
            stop: The end index.

        Returns:
            The index of the item.
        """
        item = self.asitem(item)
        args = (item, start, stop) if stop is not None else (item, start)
        return self.items.index(*args)

    def count(self, item: SequenceItemType) -> int:
        """Count the number of occurrences of a value.

        >>> ps = GeometrySequence(Point(1.0, 2.0), Point(3.0, 4.0), Point(1.0, 2.0))
        >>> ps.count(Point(1.0, 2.0))
        2

        Args:
            item: The item to count.

        Returns:
            The number of occurrences.
        """
        return self.items.count(self.asitem(item))


class PointSequence(GeometrySequence):
    """A sequence of points."""

    @property
    def points(self) -> List[Point]:
        """Return the points in the sequence.

        >>> PointSequence(Point(1.0, 2.0), Point(3.0, 4.0)).points
        [Point(x=1.0, y=2.0), Point(x=3.0, y=4.0)]
        """
        return self.items

    @classmethod
    def asitem(cls, item: PointType) -> Point:
        """Prepare the point for adding to the sequence, if necessary."""
        return Point.aspoint(item)


class LineSequence(GeometrySequence):
    """A sequence of lines."""

    @property
    def lines(self) -> List[Line]:
        """Return the lines in the sequence.

        >>> LineSequence(Line(A=1.0, B=-1.0, C=1.0), Line(A=0.0, B=1.0, C=1.0)).lines
        [Line(A=1.0, B=-1.0, C=1.0), Line(A=0.0, B=1.0, C=1.0)]
        """
        return self.items
