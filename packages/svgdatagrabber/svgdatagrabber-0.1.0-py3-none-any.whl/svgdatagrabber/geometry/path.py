from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterable, List, Union

import numpy as np
from svgpathtools import Arc as SvgPathToolsArc
from svgpathtools import CubicBezier as SvgPathToolsCubicBezier
from svgpathtools import Line as SvgPathToolsLine
from svgpathtools import Path as SvgPathToolsPath
from svgpathtools import QuadraticBezier as SvgPathToolsQuadraticBezier
from typing_extensions import Self

from .arc import Arc
from .bezier import Bezier, CubicBezier, QuadraticBezier
from .csys import CoordinateSystem
from .linebase import LineBase, StraightLineBase
from .sequence import GeometrySequence, LineSequence
from .straightline import LineSegment

SvgPathToolsSegmentType = Union[SvgPathToolsLine, SvgPathToolsArc, SvgPathToolsQuadraticBezier, SvgPathToolsCubicBezier]

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from pandas import DataFrame


class Path(StraightLineBase, LineSequence):
    items: List[LineSegment | Arc | QuadraticBezier | CubicBezier]

    #: Whether to only export the start and end points of the path.
    start_end_only: bool

    def __init__(self, *segments: LineBase, start_end_only: bool = True):
        LineSequence.__init__(self, *segments)
        self.start_end_only = start_end_only

    def __repr__(self):
        return LineSequence.__repr__(self)

    def __eq__(self, other: "Path") -> bool:
        return LineSequence.__eq__(self, other)

    @property
    def segments(self) -> List[LineSegment | Arc | QuadraticBezier | CubicBezier]:
        return self.items

    @classmethod
    def fromSvgPathToolsPath(cls, path: "SvgPathToolsPath", start_end_only: bool = True):
        segments = []
        for segment in path:
            if isinstance(segment, SvgPathToolsLine):
                segments.append(LineSegment.fromSvgPathToolsLine(segment))
            elif isinstance(segment, SvgPathToolsArc):
                segments.append(Arc.fromSvgPathToolsArc(segment))
            elif isinstance(segment, SvgPathToolsQuadraticBezier):
                segments.append(QuadraticBezier.fromSvgPathToolsQuadraticBezier(segment))
            elif isinstance(segment, SvgPathToolsCubicBezier):
                segments.append(CubicBezier.fromSvgPathToolsCubicBezier(segment))
        return cls(*segments, start_end_only=start_end_only)

    @property
    def array(self) -> np.ndarray:
        if self.start_end_only:
            return np.array([[p.x, p.y] for segment in self.segments for p in [segment.start, segment.end]])
        else:
            return np.array([[p.x, p.y] for segment in self.segments for p in segment])

    def transformed(self, csys: CoordinateSystem):
        for segment in self.items:
            segment.start = csys.transform(segment.start)
            segment.end = csys.transform(segment.end)
            if isinstance(segment, Bezier):
                segment.controls = [csys.transform(control) for control in segment.controls]


class PathSequence(GeometrySequence):
    items: List[Path]

    def __init__(self, *paths: Path):
        GeometrySequence.__init__(self, *paths)

    def __getitem__(self, item) -> Self | Path:
        items = self.items[item]
        return self.__class__(*items) if isinstance(items, list) else items

    @property
    def paths(self) -> List[Path]:
        return self.items

    @classmethod
    def fromSvgPathToolsPathSequence(cls, paths: Iterable["SvgPathToolsPath"]):
        return cls(*[Path.fromSvgPathToolsPath(path) for path in paths])

    @property
    def arrays(self) -> List[np.ndarray]:
        return [path.array for path in self.paths]

    def transformed(self, csys: CoordinateSystem):
        """Transform the paths.

        Args:
            csys: Coordinate system to transform the paths to.

        Returns:
            The transformed paths.
        """
        for path in self.items:
            path.transformed(csys)
        return self

    def plot(self, ax: "Axes" = None, fig_kwargs: dict = None, **kwargs) -> "Axes":
        """Plot the paths.

        Args:
            ax: Axes to plot on.
            fig_kwargs: Keyword arguments to pass to plt.figure().
            kwargs: Keyword arguments to pass to plt.plot().
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(**(fig_kwargs or {}))
        arrays = self.arrays
        for idx, point in enumerate(arrays):
            kwargs["label"] = f"Line-{idx}"
            ax.plot(point[:, 0], point[:, 1], **kwargs)
        ax.legend(ncol=math.floor(math.sqrt(len(arrays))))
        ax.grid()
        return ax

    def df(self, x: str = "x", y: str = "y") -> "DataFrame":
        """Get the paths as a pandas DataFrame."""
        import pandas as pd

        df = pd.DataFrame(columns=[x, y, "path"])
        for idx, line in enumerate(self.arrays):
            df = pd.concat([df, pd.DataFrame({x: line[:, 0], y: line[:, 1], "path": idx})], ignore_index=True)
        return df

    def to_csv(self, path: str, x: str = "x", y: str = "y"):
        """Save the paths as a csv file."""
        self.df(x, y).to_csv(path, index=False)
