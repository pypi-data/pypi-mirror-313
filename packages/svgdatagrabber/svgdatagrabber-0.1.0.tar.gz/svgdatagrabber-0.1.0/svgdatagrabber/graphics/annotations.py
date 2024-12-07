from typing import Union

from qtpy.QtCore import Qt
from qtpy.QtGui import QBrush, QColor, QGradient, QPen
from qtpy.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem

QPenType = Union[QPen, QColor, Qt.GlobalColor, QGradient]
QBrushType = Union[QBrush, QColor, Qt.GlobalColor, QGradient]
QGraphicsItemType = Union[QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsEllipseItem]
