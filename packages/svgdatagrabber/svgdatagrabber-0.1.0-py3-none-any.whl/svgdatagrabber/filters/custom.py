from __future__ import annotations

from typing import Callable

from svgpathtools.path import Path

from .filterbase import FilterBase


class CustomFilter(FilterBase):
    """Custom filter."""

    #: Custom filter function
    filter_function: Callable[[Path], bool]

    def __init__(self, filter_function: Callable[[Path], bool], *, enabled: bool = True, tolerance: float = 1e-6):
        super().__init__(enabled=enabled, tolerance=tolerance)
        self.filter_function = filter_function

    def accept(self, path: Path) -> bool:
        return not self.enabled or self.filter_function(path)
