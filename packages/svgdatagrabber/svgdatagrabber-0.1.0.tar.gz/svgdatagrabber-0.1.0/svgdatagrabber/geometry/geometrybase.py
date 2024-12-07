from __future__ import annotations

import sys
from abc import ABC
from enum import IntEnum
from typing import Tuple

from qtpy.QtCore import Qt
from qtpy.QtGui import QPen
from qtpy.QtWidgets import QApplication, QGraphicsScene

from ..graphics.annotations import QBrushType, QGraphicsItemType, QPenType


class GeometryDrawAs(IntEnum):
    """Geometry draw as enum."""

    DrawAsLine = 0
    DrawAsPolygon = 1
    DrawAsEllipse = 2


DrawAsLine = GeometryDrawAs.DrawAsLine
DrawAsPolygon = GeometryDrawAs.DrawAsPolygon
DrawAsEllipse = GeometryDrawAs.DrawAsEllipse


class GeometryBase(ABC):
    """A base class for all geometries."""

    #: Tolerance for equality.
    tolerance = 1e-6

    #: type of drawing
    drawAs: GeometryDrawAs

    def __repr__(self) -> str:
        """Return the representation of the geometry."""
        raise NotImplementedError

    def __eq__(self, other: "GeometryBase") -> bool:
        """Check if two geometries are equal."""
        raise NotImplementedError

    def __ne__(self, other: "GeometryBase") -> bool:
        """Check if two geometries are not equal."""
        return not self.__eq__(other)

    @property
    def maxsize(self) -> float:
        """Return the max size of the geometry."""
        raise NotImplementedError

    @property
    def drawArgs(self) -> Tuple[str, tuple]:
        """Return the arguments for drawing the geometry."""
        raise NotImplementedError

    def draw(
        self,
        scene: QGraphicsScene,
        pen: QPenType = None,
        brush: QBrushType = None,
        item: QGraphicsItemType = None,
    ) -> QGraphicsItemType:
        """Draw the geometry on the scene.

        Args:
            scene: The scene to draw on.
            pen: The pen to draw with.
            brush: The brush to draw with.
            item: The old item to draw on, if any.
        """
        args = self.drawArgs
        if self.drawAs == DrawAsLine:
            item and item.setLine(*args) or item or (item := scene.addLine(*args))
        elif self.drawAs == DrawAsPolygon:
            item and item.setPolygon(*args) or item or (item := scene.addPolygon(*args))
        elif self.drawAs == DrawAsEllipse:
            item and item.setRect(*args) or item or (item := scene.addEllipse(*args))
        else:
            raise ValueError(f"Unknown type {self.drawAs}")
        pen = QPen(pen or item.pen())
        pen.setWidthF(min(0.02 * self.maxsize, pen.widthF()))
        item.setPen(pen)
        item.setBrush(brush or item.brush())
        return item

    def plot(self, pen: QPenType = None, brush: QBrushType = None, fit: bool = True):
        """Plot the geometry.

        Args:
            pen: The pen to draw with.
            brush: The brush to draw with.
            fit: Fit the view to the geometry.
        """
        from ..graphics.graphicsview import GraphicsView

        app = QApplication(sys.argv)
        scene = QGraphicsScene()
        view = GraphicsView(scene)
        view.setWindowTitle(repr(self))
        view.resize(800, 600)
        view.show()
        self.draw(scene, pen, brush)
        fit and view.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        sys.exit(app.exec_())
