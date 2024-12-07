"""
The Graphics User Interface (GUI) for the SVG Data Grabber, run with ``python -m svgdatagrabber.graphics`` or
``svgdatagrabber-graphics``.
"""


def main():
    import sys

    from qtpy.QtWidgets import QApplication

    from svgdatagrabber.graphics.mainwindow import SvgDataGrabberMainWindow

    app = QApplication(sys.argv)
    window = SvgDataGrabberMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
