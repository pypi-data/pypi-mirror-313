import numpy as np
import pytest

from svgdatagrabber.parser import SvgPathParser


@pytest.mark.parametrize(
    "xrange, yrange, size",
    [
        ((-np.inf, np.inf), (-np.inf, np.inf), 19348),
        ((0, 3000), (5000, 6100), 4608),
        ((3300, 5200), (4800, 6100), 4580),
        ((0, 3000), (3300, 4500), 4488),
        ((3300, 5200), (3300, 4500), 4568),
    ],
)
def test_praai2013(xrange, yrange, size):
    paths = SvgPathParser(
        "praai2013.svg",
        xrange=xrange,
        yrange=yrange,
        min_segments=6,
        drop_horizontal_lines=False,
        drop_vertical_lines=False,
        tolerance=1,
    ).parse()
    assert np.sum([array.size for array in paths.arrays]) == size
