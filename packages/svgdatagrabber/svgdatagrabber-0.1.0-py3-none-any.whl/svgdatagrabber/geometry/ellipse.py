from __future__ import annotations

from typing import Iterable, List, Tuple

import numpy as np

from .closedshape import ClosedShape
from .geometrybase import DrawAsEllipse
from .linebase import LineBase
from .point import Point, PointType


class Ellipse(ClosedShape):
    """A class representing an ellipse."""

    drawAs = DrawAsEllipse

    #: The center of the ellipse.
    center: Point
    #: The radius in the x direction.
    ra: float
    #: The radius in the y direction.
    rb: float
    #: The rotation of the ellipse in degrees.
    theta: float

    def __init__(
        self,
        center: PointType = None,
        ra: float = None,
        rb: float = None,
        theta: float = 0.0,
        A: float = None,
        B: float = None,
        C: float = None,
        D: float = None,
        E: float = None,
        F: float = None,
    ):
        """Create an ellipse, either by center, radius and rotation angle or by parameters.

        >>> Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0, theta=0.0)
        Ellipse(center=Point(x=0.0, y=0.0), ra=1.0, rb=1.0, theta=0.0)
        >>> Ellipse(A=1.0, B=0.0, C=1.0, D=0.0, E=0.0, F=-1.0)
        Ellipse(center=Point(x=0.0, y=0.0), ra=1.0, rb=1.0, theta=0.0)

        Args:
            center: The center of the ellipse.
            ra: The radius in the x direction.
            rb: The radius in the y direction.
            theta: The rotation of the ellipse in radians.
        """
        if center is not None and ra is not None and rb is not None and theta is not None:
            self.center = Point.aspoint(center)
            self.ra = ra
            self.rb = rb
            self.theta = theta
        elif A is not None and B is not None and C is not None and D is not None and E is not None and F is not None:
            self.ra = (
                np.sqrt(
                    2
                    * (A * E**2 + C * D**2 - B * D * E + (B**2 - 4 * A * C) * F)
                    / ((B**2 - 4 * A * C) * (np.sqrt((A - C) ** 2 + B**2) - (A + C)))
                )
                + 0.0
            )
            self.rb = (
                np.sqrt(
                    2
                    * (A * E**2 + C * D**2 - B * D * E + (B**2 - 4 * A * C) * F)
                    / ((B**2 - 4 * A * C) * (-np.sqrt((A - C) ** 2 + B**2) - (A + C)))
                )
                + 0.0
            )
            self.theta = np.arctan2(C - A - np.sqrt((A - C) ** 2 + B**2), B) + 0.0
            x0 = (2 * C * D - B * E) / (B**2 - 4 * A * C) + 0.0
            y0 = (2 * A * E - B * D) / (B**2 - 4 * A * C) + 0.0
            self.center = Point(x0, y0)
        else:
            raise ValueError("Invalid arguments.")

    def __repr__(self):
        """Return a string representation of the ellipse.

        >>> repr(Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0, theta=0.0))
        'Ellipse(center=Point(x=0.0, y=0.0), ra=1.0, rb=1.0, theta=0.0)'
        """
        return f"{self.__class__.__name__}(center={self.center}, ra={self.ra}, rb={self.rb}, theta={self.theta})"

    def __eq__(self, other: "Ellipse") -> bool:
        """Check if two ellipses are equal.

        >>> Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0) == Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0)
        True
        >>> Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0) == Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=2.0)
        False

        Args:
            other: The other ellipse.
        """
        return self.center == other.center and self.ra == other.ra and self.rb == other.rb and self.theta == other.theta

    @property
    def boundaries(self) -> List[LineBase]:
        raise NotImplementedError

    def containsPoint(self, point: PointType | Iterable[Point]) -> bool:
        """Check if a point is inside the ellipse.

        >>> Point(0.5, 0.5) in Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0)
        True
        >>> Point(0.6, 0.8) in Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0)
        True

        Args:
            point: The point.
        """
        if isinstance(point, Iterable) and isinstance(tuple(point)[0], Point):
            return all(self.contains(p) for p in point)
        point = Point.aspoint(point)
        x, y = point.x, point.y
        A, B, C, D, E, F = self.coefficients
        return A * x**2 + B * x * y + C * y**2 + D * x + E * y + F <= 0

    def containsLine(self, line: LineBase | Iterable[LineBase]) -> bool:
        raise NotImplementedError

    @property
    def x0(self) -> float:
        """Return the x coordinate of the left side of the ellipse."""
        return self.center.x

    @property
    def y0(self) -> float:
        """Return the y coordinate of the top of the ellipse."""
        return self.center.y

    @property
    def A(self) -> float:
        """Returns A parameter of the ellipse equation."""
        return self.ra**2 * np.sin(self.theta) ** 2 + self.rb**2 * np.cos(self.theta) ** 2

    @property
    def B(self) -> float:
        """Returns B parameter of the ellipse equation."""
        return 2 * (self.rb**2 - self.ra**2) * np.sin(self.theta) * np.cos(self.theta)

    @property
    def C(self) -> float:
        """Returns C parameter of the ellipse equation."""
        return self.ra**2 * np.cos(self.theta) ** 2 + self.rb**2 * np.sin(self.theta) ** 2

    @property
    def D(self) -> float:
        """Returns D parameter of the ellipse equation."""
        return -2 * self.A * self.x0 - self.B * self.y0

    @property
    def E(self) -> float:
        """Returns E parameter of the ellipse equation."""
        return -self.B * self.x0 - 2 * self.C * self.y0

    @property
    def F(self) -> float:
        """Returns F parameter of the ellipse equation."""
        return self.A * self.x0**2 + self.B * self.x0 * self.y0 + self.C * self.y0**2 - self.ra**2 * self.rb**2

    @property
    def coefficients(self) -> Tuple[float, float, float, float, float, float]:
        """Return the coefficients of the ellipse equation.

        Returns:
            The parameters of the ellipse equation.
        """
        return self.A, self.B, self.C, self.D, self.E, self.F

    @property
    def maxsize(self) -> float:
        """Return the maximum size of the ellipse.

        >>> Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=2.0).maxsize
        4.0
        """
        return max(self.ra, self.rb) * 2

    @property
    def area(self) -> float:
        """Return the area of the ellipse.

        >>> assert Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0).area == np.pi
        """
        return np.pi * self.ra * self.rb

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the ellipse.

        >>> assert Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0).perimeter == 2 * np.pi
        """
        return 2 * np.pi * np.sqrt((self.ra**2 + self.rb**2) / 2)

    @property
    def centroid(self) -> Point:
        """Return the centroid of the ellipse.

        >>> Ellipse(center=Point(0.0, 0.0), ra=1.0, rb=1.0).centroid
        Point(x=0.0, y=0.0)
        """
        return self.center

    @property
    def bbox(self) -> Tuple[Point, Point]:
        """Return the bounding box of the ellipse."""
        raise NotImplementedError

    @property
    def drawArgs(self) -> Tuple[float, float, float, float]:
        return self.x0, self.y0, self.ra, self.rb
