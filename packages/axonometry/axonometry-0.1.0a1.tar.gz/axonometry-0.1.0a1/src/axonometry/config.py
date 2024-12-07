# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This file defines basic parameters (like a verbose flag) and performs various parameterization for the image size and line styles.

Image Size
----------

The image size is determined by the width and height in pixels.
It is expressed as a tuple of integer values in :attr:`image_resolution`.
As the size of the image is determined diretcly in pixels, the dpi (dots per inch) value is not necessary to be determined. Therefor set to 1.

Line Styles
-----------

Knowing that the image size is constant, one can determine the size of geometries in point units.

The line weights are determined by the standard 72 ppi (points per inch)
of the Plotter object. We need to convert mm into points, knowing that
1 mm is 1/25.4 inch and that 1 inch is 72 points:

>>> mm = (1 / 25.4) * 72
>>> 1 * mm
>>> 2.8346456692913384

The configuration follows then the line weights implement the DIN A norm, i.e. a
:math:`\sqrt{2} ≈ 1.4` relationship of sizes. As such the lineweights
in mm are:

+------+------+------+------+------+------+------+------+------+------+
| 0.10 | 0.13 | 0.18 | 0.25 | 0.35 | 0.50 | 0.70 | 1.00 | 1.40 | 2.00 |
+------+------+------+------+------+------+------+------+------+------+

sources:
    + `Stackoverflow answer 47639545 <https://stackoverflow.com/a/47639545>`__.
    + `Why A4? The Mathematical Beauty of Paper Size <https://web.archive.org/web/20230814124712/https://scilogs.spektrum.de/hlf/why-a4-the-mathematical-beauty-of-paper-size/>`__.

"""
from typing import Union, Dict, Tuple

# -- Size Parameters ----------------------------------------------------------
image_resolution: tuple[int, int] = (1280, 720)
dpi: int = 1  # useless: pixel size of the image is set and size units are in points
# convert mm into points. written with dpi as potential parameter.
mm: float = ((1 / 25.4) * 72) / (dpi / 72)

InnerValueType = Union[bool, float, str, Tuple[int, Tuple[int, ...]]]

line_styles: Dict[str, Dict[str, InnerValueType]] = {
    "default": {"draw_points": False, "linewidth": 0.35 * mm},
    "trihedron": {"draw_points": False, "linewidth": 0.13 * mm},
    "coordinate_plane": {"draw_points": False, "linewidth": 0.13 * mm},
    "picture_plane": {"draw_points": False, "linewidth": 0.35 * mm},
    "hinge": {
        "draw_points": False,
        "linewidth": 0.1 * mm,
        "linestyle": (+0, (10, 5, +1, 5, +1, 5)),
    },
    "drawdown_sphere": {"linewidth": 0.1 * mm, "fill": False, "linestyle": "dashed"},
    "drawdown_plane": {
        "draw_points": False,
        "linewidth": 0.1 * mm,
        "linestyle": (+0, (10, 10)),
    },
    "translation": {
        "draw_points": False,
        "linewidth": 0.1 * mm,
        "linestyle": (+0, (+1, 10)),
    },
    "outline": {"draw_points": False, "linewidth": 0.70 * mm},
    "projection": {"linewidth": 0.18 * mm, "draw_points": False, "linestyle": "dashed"},
}

# -- Prints in `Drawing.update()`
verbose: bool = True


# -- Cnventional Axonometric Angles
angle_conventions: dict[str, tuple[int | float, int | float]] = {
    "isometric": (30, 30),
    "dimetric_simple_1": (7, 41.5),
    "dimetric": (41.5, 41.5),
    "trimetric_1a": (15, 30),
    "trimetric_1b": (30, 15),
    "trimetric_2a": (15, 45),
    "trimetric_2b": (45, 15),
    "trimetric_3a": (30, 45),
    "trimetric_3b": (45, 30),
    "other_1a": (15, 60),
    "other_1b": (60, 15),
    "other_2": (15, 15),
}
