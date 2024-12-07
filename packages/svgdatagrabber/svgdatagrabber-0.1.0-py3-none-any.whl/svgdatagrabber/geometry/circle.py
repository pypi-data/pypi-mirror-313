from typing import Tuple

from .ellipse import Ellipse
from .point import Point, PointType


class Circle(Ellipse):
    """A class representing a circle."""

    #: The radius of the circle.
    _r: float

    def __init__(self, center: PointType, r: float):
        """Create a circle, either by center and radius or by parameters.

        >>> Circle(center=Point(0.0, 0.0), r=1.0)
        Circle(center=Point(x=0.0, y=0.0), r=1.0)

        Args:
            center: The center of the circle.
            r: The radius of the circle.
        """
        super().__init__(center=center, ra=r, rb=r, theta=0.0)
        self._r = r

    def __repr__(self) -> str:
        """Get the string representation of the circle.

        >>> repr(Circle(center=Point(0.0, 0.0), r=1.0))
        'Circle(center=Point(x=0.0, y=0.0), r=1.0)'
        """
        return f"{self.__class__.__name__}(center={self.center}, r={self.r})"

    @property
    def r(self):
        """Get the radius of the circle.

        >>> Circle(center=Point(0.0, 0.0), r=1.0).r
        1.0
        """
        return self._r

    @r.setter
    def r(self, value):
        """Set the radius of the circle.

        >>> circle = Circle(center=Point(0.0, 0.0), r=1.0)
        >>> circle.r = 2.0
        >>> circle.r
        2.0
        """
        self._r, self.ra, self.rb = value, value, value

    def bbox(self) -> Tuple[Point, Point]:
        """Get the bounding box of the circle.

        >>> Circle(center=Point(0.0, 0.0), r=1.0).bbox()
        (Point(x=-1.0, y=-1.0), Point(x=1.0, y=1.0))

        Returns:
            The bounding box of the circle.
        """
        return (
            Point(x=self.center.x - self.r, y=self.center.y - self.r),
            Point(x=self.center.x + self.r, y=self.center.y + self.r),
        )
