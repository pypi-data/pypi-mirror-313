from __future__ import annotations

from typing import Callable

import numpy as np
from svgpathtools.path import Path
from svgpathtools.svg_to_paths import svg2paths

from .filters import (
    ClosedPathFilter,
    CustomFilter,
    FilterBase,
    HorizontalLineFilter,
    RectangleRangeFilter,
    SegmentNumberFilter,
    VerticalLineFilter,
)
from .geometry import PathSequence
from .geometry.csys import CoordinateSystem


class SvgPathParser:
    """Parse an SVG file and return the paths."""

    #: Path to the svg file
    svgfile: str
    #: Filters
    filters: list[FilterBase]
    #: coordinate system
    csys: CoordinateSystem

    def __init__(
        self,
        svgfile: str,
        xrange: tuple[float, float] = (-np.inf, np.inf),
        yrange: tuple[float, float] = (-np.inf, np.inf),
        min_segments: int = 4,
        drop_horizontal_lines: bool = True,
        drop_vertical_lines: bool = True,
        drop_closed_paths: bool = True,
        custom_filter: Callable[[Path], bool] | FilterBase = None,
        tolerance: float = 1e-6,
    ):
        """Constructor of the SvgPathParser class.

        Args:
            svgfile: Path to the svg file.
            xrange: Range of x values to include.
            yrange: Range of y values to include.
            min_segments: Minimum number of segments in a path.
            drop_horizontal_lines: Whether to drop horizontal lines.
            drop_vertical_lines: Whether to drop closed paths.
            drop_closed_paths: Whether to drop closed paths.
            custom_filter: Custom filter for the paths.
            tolerance: Tolerance for determining if a path is a horizontal or vertical line.
        """
        self.svgfile = svgfile
        self.filters = [
            RectangleRangeFilter(xrange=xrange, yrange=yrange),
            SegmentNumberFilter(min_segments=min_segments),
            HorizontalLineFilter(enabled=drop_horizontal_lines, tolerance=tolerance),
            VerticalLineFilter(enabled=drop_vertical_lines, tolerance=tolerance),
            ClosedPathFilter(enabled=drop_closed_paths),
        ]
        self.addFilter(custom_filter)
        self.csys = CoordinateSystem()

    def addFilter(self, f: Callable[[Path], bool] | FilterBase):
        """Add a custom filter to the parser.

        Args:
            f: Custom filter for the paths.
        """
        if not f:
            return
        self.filters.append(f if isinstance(f, FilterBase) else CustomFilter(f))

    def parse(self) -> PathSequence:
        """Parse the paths from the svg file.

        Returns:
            A list of paths.
        """

        def filtered(pts: list[Path]) -> list[Path]:
            return [pt for pt in pts if all(f.accept(pt) for f in self.filters)]

        paths, atts = svg2paths(self.svgfile)
        paths = PathSequence.fromSvgPathToolsPathSequence(filtered(paths)).transformed(self.csys)
        return paths
