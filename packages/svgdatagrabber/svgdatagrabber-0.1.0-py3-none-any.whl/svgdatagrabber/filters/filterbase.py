from __future__ import annotations

from abc import ABC

from svgpathtools.path import Path


class FilterBase(ABC):
    """Base class for filters."""

    #: Enabled or not
    enabled: bool = True
    #: Tolerance for determining if a path is a horizontal or vertical line
    tolerance: float = 1e-6

    def __init__(self, *, enabled: bool = True, tolerance: float = 1e-6):
        self.enabled = enabled
        self.tolerance = tolerance

    def accept(self, path: Path) -> bool:
        """Accept or reject a path.

        Args:
            path: Path to check.

        Returns:
            True if the path is accepted, False otherwise.
        """
        raise NotImplementedError

    def __call__(self, path: Path) -> bool:
        return self.accept(path)

    def enable(self):
        """Enable the filter."""
        self.enabled = True

    def disable(self):
        """Disable the filter."""
        self.enabled = False
