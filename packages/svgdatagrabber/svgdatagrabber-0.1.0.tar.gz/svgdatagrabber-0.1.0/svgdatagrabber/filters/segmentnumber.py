from __future__ import annotations

from svgpathtools.path import Path

from .filterbase import FilterBase


class SegmentNumberFilter(FilterBase):
    """Filter paths based on the number of segments."""

    #: Minimum number of segments in a path.
    min_segments: int

    def __init__(self, min_segments: int = 4, *, enabled: bool = True, tolerance: float = 1e-6):
        super().__init__(enabled=enabled, tolerance=tolerance)
        self.min_segments = min_segments

    def accept(self, path: Path) -> bool:
        return not self.enabled or len(path) >= self.min_segments
