# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

# imports for type checking
from __future__ import annotations
from typing import Optional, Any, Union

# own libraries
from compas.geometry import Point, Polyline, Circle
from . import config
from . import axonometry

# extra
from compas_plotters import Plotter
from time import time
from itertools import pairwise


class DrawingData:
    """Get/set class to organize the elements in a drawing.

    Basically a double list of geometry elements and their line styles.
    """

    def __init__(self):
        self._geometry: list[Point | Polyline | Circle] = (
            []
        )  # list of all drawing operations
        self._line_styles: list[str] = []  # styles of operations in same order

        # keep track of geometry xy boundaries
        self._min_x: Optional[float] = 0.0
        self._max_x: Optional[float] = 0.0
        self._min_y: Optional[float] = 0.0
        self._max_y: Optional[float] = 0.0

        self._x_size = 0.0
        self._y_size = 0.0

    def add(
        self,
        geometry: Point | Polyline | Circle | list[Point | Polyline | Circle],
        style: str,
    ) -> None:
        # flatten lists
        if isinstance(geometry, list):
            for elem in geometry:
                self.add(elem, style)
        # explode Polylines (for animation purpose)
        elif len(geometry) > 2 and isinstance(geometry, Polyline):
            geometry = [Polyline(pair) for pair in pairwise(geometry)]
            self.add(geometry, style)
        # add geometry to data
        else:
            self._geometry.append(geometry)
            self._line_styles.append(style)

            self._update_boundaries(geometry)

    def get(self) -> tuple[list[Any | Any | Any], list[str]]:
        return self._geometry, self._line_styles

    def _update_boundaries(
        self, geometry: Point | Polyline | Circle | list[Point | Polyline | Circle]
    ) -> None:
        """Update boundary values of drawing.

        Parse the added geometries to get their constituent Point values.
        Update min and max values for x and y coordinates.

        Args:
            geometry: geometry objects added to the drawing data.
        """
        if isinstance(geometry, Point):
            self._min_x = min(geometry.x, self._min_x)
            self._max_x = max(geometry.x, self._max_x)
            self._min_y = min(geometry.y, self._min_y)
            self._max_y = max(geometry.y, self._max_y)

            if self._min_x and self._min_y and self._max_x and self._max_y:
                self._x_size = abs(self._max_x - self._min_x)
                self._y_size = abs(self._max_y - self._min_y)

        elif isinstance(geometry, Circle):
            radius = geometry.diameter / 2
            center = geometry.center
            for p in [
                Point(center.x + radius, center.y),
                Point(center.x - radius, center.y),
                Point(center.x, center.y + radius),
                Point(center.x, center.y - radius),
            ]:
                self._update_boundaries(p)

        elif hasattr(geometry, "points"):
            for p in geometry:
                self._update_boundaries(p)


class Drawing(DrawingData):
    """Public class of the axonometry library."""

    _plotted = False

    def update(
        self,
        geometry: Point | Polyline | Circle | list[Point | Polyline | Circle],
        style: str,
        origin: (
            axonometry.Trihedron | axonometry.PicturePlane | axonometry.CoordinatePlane
        ),
    ) -> None:
        if config.verbose:
            # _simple_text = compile(r"^([^.]*).*")
            print(
                f"\n[update] {str(geometry).split('(')[0].replace('[', '')} : {style} in {origin.name}"
            )

        # if custom style, it's a dict not a key
        style: str | dict = (
            config.line_styles[style] if isinstance(style, str) else style
        )

        self.add(geometry, style)

    def display(self, save_in: Optional[str] = None) -> None:
        start_time: float = time()
        plotter: Plotter = self._configure_plotter()

        if not self._plotted:
            geometry, styles = self.get()
            # add geometry objects from data
            for line, style in zip(geometry, styles):
                plotter.add(line, **style)
            print("\n[Displayed in %.2fs]" % (time() - start_time))
            # show or save plotted drawing
            if save_in:
                plotter.save(filepath=save_in + ".png", dpi="figure")
                plotter.show()
            else:
                plotter.show()

            self._plotted = True
        else:
            print("[warning] plot can't be generated twice.")

    def animate(self, file: str) -> None:
        _plotter = self._configure_plotter()

        if not self._plotted:
            geometry, styles = self.get()

            @_plotter.on(
                interval=0.5,
                frames=len(geometry),
                record=True,
                recording=file + ".gif",
                dpi="figure",
            )
            def add_objects(frame):
                _plotter.add(geometry[frame], **styles[frame])

            self._plotted = True
        else:
            print("[warning] plot can't be generated twice.")

    def add_axonometry_from_angles(
        self, angles: tuple[int | float, int | float], position=(0, 0)
    ) -> axonometry.Axonometry:
        # TODO: rename position to 'location'
        position = Point(*position)
        return axonometry.Axonometry(self, position=position, angles=angles)

    def _configure_plotter(
        self,
        dpi: int = config.dpi,
        resolution: tuple[int, int] = config.image_resolution,
    ) -> Plotter:
        """Make a Plotter instance with adapted parameters.

        Arg:
            dpi (int):
                The dpi value of the plot,
                defaults to 96 in config.py
                which is the Inkscape standard.

        Returns:
            A :class:`.compas_plotters.Plotter`
            instance scale to the size of the geometries.
        """

        min_x, max_x, min_y, max_y = 0.0, 0.0, 0.0, 0.0
        if self._min_x and self._min_y and self._max_x and self._max_y:
            min_x = self._min_x - 1
            max_x = self._max_x + 1
            min_y = self._min_y - 1
            max_y = self._max_y + 1

        return Plotter(
            view=(
                (min_x, max_x),
                (min_y - 1, max_y),
            ),
            figsize=(
                resolution[0] / dpi,
                resolution[1] / dpi,
            ),  # make precise image size in pixel
            dpi=dpi,
            bgcolor=(1.0, 1.0, 1.0),
            show_axes=False,
            zstack="zorder",
        )
