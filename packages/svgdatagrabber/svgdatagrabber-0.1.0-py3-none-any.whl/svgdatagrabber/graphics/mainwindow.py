from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow

from ..geometry import Circle, Point, Polygon
from .graphicsview import GraphicsView


class SvgDataGrabberMainWindow(QMainWindow):
    """A custom main window for the data grabber application."""

    def __init__(self, parent=None):
        super(SvgDataGrabberMainWindow, self).__init__(parent)
        self.view = GraphicsView(self)
        self.setCentralWidget(self.view)

        self.resize(800, 600)
        self.setWindowTitle("SVG Data Grabber")

        # add test geometries
        self.view.addPrimitive(Polygon(Point(0.0, 0.0), Point(100.0, 0.0), Point(100.0, 100.0), Point(0.0, 100.0)))
        self.view.addPrimitive(Circle(center=Point(50.0, 50.0), r=50.0))
        self.view.redraw(Qt.blue, Qt.red)
