class QtException(Exception):
    """Base class for all Qt exceptions."""

    pass


class NotDrawableGeometryError(QtException):
    """An exception raised when a geometry cannot be drawn on a Qt scene."""

    pass


class NoCorrespondingQtObjectError(QtException):
    """An exception raised when a geometry has no corresponding Qt object."""

    pass
