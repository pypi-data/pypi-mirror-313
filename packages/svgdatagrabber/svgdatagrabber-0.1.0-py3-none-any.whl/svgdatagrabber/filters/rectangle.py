from __future__ import annotations

from typing import Union

import numpy as np
from svgpathtools.path import Arc, CubicBezier, Line, Path, QuadraticBezier

from .filterbase import FilterBase


class RectangleRangeFilter(FilterBase):
    """Filter paths based on their range."""

    #: Range of x values to include.
    xrange: tuple[float, float]
    #: Range of y values to include.
    yrange: tuple[float, float]
    #: Include or exclude the range
    include: bool
    #: Sensitive or not
    sensitive: bool

    def __init__(
        self,
        xrange: tuple[float, float] = (-np.inf, np.inf),
        yrange: tuple[float, float] = (-np.inf, np.inf),
        include: bool = True,
        sensitive: bool = False,
        enabled: bool = True,
        tolerance: float = 1e-6,
    ):
        super().__init__(enabled=enabled, tolerance=tolerance)
        self.xrange = tuple(xrange)
        self.yrange = tuple(yrange)
        self.include = include
        self.sensitive = sensitive

    def accept(self, path: Path) -> bool:
        def pointInRange(p: complex):
            return self.xrange[0] <= p.real <= self.xrange[1] and self.yrange[0] <= p.imag <= self.yrange[1]

        def segmentInRange(seg: Union[Line, QuadraticBezier, CubicBezier, Arc]):
            func = all if self.sensitive else any
            return func(pointInRange(p) for p in seg.bpoints())

        def pathInRange(pth: Path):
            func = all if self.sensitive else any
            return func(segmentInRange(seg) for seg in pth)

        def pathOutRange(pth: Path):
            return not pathInRange(pth)

        return not self.enabled or (self.include and pathInRange(path)) or (not self.include and pathOutRange(path))
