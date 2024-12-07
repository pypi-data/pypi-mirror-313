from abc import ABC

from .geometrybase import DrawAsLine, GeometryBase


class LineBase(GeometryBase, ABC):
    """A base class for line-like geometries."""

    drawAs = DrawAsLine

    pass


class StraightLineBase(LineBase, ABC):
    """A base class for straight line-like geometries."""

    pass


class CurveLineBase(LineBase, ABC):
    """A base class for curve line-like geometries."""

    pass
