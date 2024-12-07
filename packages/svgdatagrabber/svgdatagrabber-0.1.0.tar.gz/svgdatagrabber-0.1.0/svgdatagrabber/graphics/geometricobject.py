from qtpy.QtWidgets import QGraphicsScene

from ..geometry import GeometryBase
from .annotations import QBrushType, QGraphicsItemType, QPenType


class GeometricObject:
    #: The geometry of the object.
    geometry: GeometryBase
    #: The graphics item of the object.
    item: QGraphicsItemType

    def __init__(self, geometry: GeometryBase, item: QGraphicsItemType = None):
        """Create a geometric object.

        Args:
            geometry: The geometry of the object.
            item: The graphics item of the object.
        """
        self.geometry = geometry
        self.item = item

    def redraw(
        self,
        scene: QGraphicsScene,
        pen: QPenType = None,
        brush: QBrushType = None,
    ):
        """Draw the object in the scene."""
        self.item = self.geometry.draw(scene, pen, brush, self.item)
