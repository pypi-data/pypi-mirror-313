from __future__ import annotations

from svgpathtools.path import Path

from .filterbase import FilterBase


class ClosedPathFilter(FilterBase):
    """Filter for closed paths."""

    def accept(self, path: Path) -> bool:
        return not self.enabled or not (path.iscontinuous() and path.isclosed())
