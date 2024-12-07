from __future__ import annotations

from typing import Union

from svgpathtools.path import Arc, CubicBezier, Line, Path, QuadraticBezier

from .filterbase import FilterBase


class HorizontalLineFilter(FilterBase):
    """Filter for horizontal lines."""

    def accept(self, path: Path) -> bool:
        def segmentIsHorizontal(segment: Union[Line, QuadraticBezier, CubicBezier, Arc]):
            if not isinstance(segment, Line):
                return False
            return abs(segment.start.imag - segment.end.imag) < self.tolerance

        return not self.enabled or not (all(segmentIsHorizontal(segment) for segment in path))


class VerticalLineFilter(FilterBase):
    """Filter for vertical lines."""

    def accept(self, path: Path) -> bool:
        def segmentIsVertical(segment: Union[Line, QuadraticBezier, CubicBezier, Arc]):
            if not isinstance(segment, Line):
                return False
            return abs(segment.start.real - segment.end.real) < self.tolerance

        return not self.enabled or not (all(segmentIsVertical(segment) for segment in path))
