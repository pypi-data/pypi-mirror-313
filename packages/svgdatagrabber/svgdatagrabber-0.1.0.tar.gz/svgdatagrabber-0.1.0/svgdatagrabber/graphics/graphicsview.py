from __future__ import annotations

from typing import List, overload

from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter
from qtpy.QtWidgets import QGraphicsScene, QGraphicsView, QOpenGLWidget, QWidget

from ..geometry import GeometryBase
from .annotations import QBrushType, QPenType
from .geometricobject import GeometricObject


class GraphicsView(QGraphicsView):
    """GraphicsView class."""

    #: geometric objects
    geometric_objects: List[GeometricObject]

    @overload
    def __init__(self, parent: QWidget | None = None, *, useOpenGL: bool = False): ...

    @overload
    def __init__(self, scene: QGraphicsScene = None, parent: QWidget | None = None, *, useOpenGL: bool = False): ...

    def __init__(
        self,
        scene: QGraphicsScene | QWidget | None = None,
        parent: QWidget | None = None,
        *,
        useOpenGL: bool = False,
    ):
        """Initialize the class."""
        if isinstance(scene, QWidget):
            scene, parent = None, scene
        super().__init__(parent)
        self.scene = scene or QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.HighQualityAntialiasing)

        # geometric objects
        self.geometric_objects = []

        # use OpenGL
        useOpenGL and self.useOpenGL()

    def addPrimitive(self, primitive: GeometricObject | GeometryBase, fitInView: bool = True, scale: float = 1.0):
        """Add a primitive to the scene."""
        if isinstance(primitive, GeometryBase):
            primitive = GeometricObject(primitive)
        primitive.redraw(self.scene)
        self.geometric_objects.append(primitive)
        fitInView and self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.scale(scale, scale)

    def redraw(self, pen: QPenType = None, brush: QBrushType = None, fitInView: bool = True, scale: float = 1.0):
        """Draw the geometries in the scene and fit the view."""
        for geometric_object in self.geometric_objects:
            geometric_object.redraw(self.scene, pen, brush)
        fitInView and self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.scale(scale, scale)

    def useOpenGL(self):
        """Use OpenGL."""
        self.setViewport(QOpenGLWidget())

    def wheelEvent(self, event):
        """
        Zoom in or out of the view, from https://stackoverflow.com/a/29026916/18728919.
        """
        # Zoom factors
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        zoomFactor = zoomInFactor if event.angleDelta().y() > 0 else zoomOutFactor
        self.scale(zoomFactor, zoomFactor)
        self.centerOn(self.mapToScene(self.viewport().rect().center()))

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
