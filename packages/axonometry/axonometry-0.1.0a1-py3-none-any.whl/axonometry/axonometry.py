# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

# imports for type checking
from __future__ import annotations
from typing import Optional, Union, TYPE_CHECKING
from compas.geometry import (
    Geometry,
    Point,
    Vector,
    Polyline,
    Rotation,
)

# regular imports
from math import radians
from .geometry import (
    drawdown,
    resize_plane,
    compute_matrix_from_axis,
    translate_plane_along_axis,
    project_point_on_coordinate_plane_axis,
)

if TYPE_CHECKING:
    from .drawing import Drawing


class PicturePlane:
    """
    Observer classes in order to transmit added geometry
    (i.e. drawing elements) to a Drawing class object and
    subsequently a Plotter instance.
    """

    _geometry: list[Geometry]  # TODO: typing Protocol implementation
    _projections: list[Polyline]
    # TODO: typing Protocol implementation & rename to 'traces'

    def __init__(self, drawing: "Drawing"):
        self._drawing = drawing
        self._geometry = []
        self._projections = []
        self._matrix: Optional[list[list[float]]] = None
        self.name = ""
        # TODO: make geometry collection which makes it
        # easier to retrieve certain objects and their
        # style.

    def add_geometry(
        self,
        geometry: Geometry | list[Polyline],
        style: str = "default",
        no_matrix: bool = False,
    ) -> Geometry:
        """Base function to add geometries."""
        if self._matrix and not no_matrix:
            geometry = geometry.transformed(self._matrix)
        self._geometry.append(geometry)
        self._notify(geometry, style)  # send geometry to Drawing

        return geometry

    def project_geometry(
        self, geometry: Geometry, style: str = "projection"
    ) -> Geometry:
        self._projections.append(geometry)
        self._notify(geometry, style)  # send geometry to Drawing

        return geometry

    def get_geometry(self) -> list[Geometry]:
        """Get the geometry previously added.

        Returns:
            A list of the geometries.
        """
        return (
            self._geometry
        )  # TODO: exclude own geometry, i.e. get only added geometry

    def _notify(self, geometry: Geometry, style: str) -> None:
        """Notify :class:`.Drawing`.

        Pass ``self`` along the notification to include
        the location where the geometry was added in
        the output message.

        Args:
            geometry: what was added.
            style: choice of line style.
        """

        self._drawing.update(geometry, style, origin=self)


class Axonometry:
    """Class to manage the different components of an Axonometry construction.

    An Axonometry is composed of the three components: 1x :class:`PicturePlane`,
    1x :class:`Trihedron` and 3x :class:`CoordinatePlane`. These objects are
    initiated together with the Axonometry instance.

    The Axonometry object itself works more like a data structure than
    a drawing surface. The geometry added to the Axonometry object by
    :func:`add_geometry` lands on the :class:`PicturePlane` instance.

    .. note:: the :class:`.Drawing` object is part of the Axonometry instantiated and
        passed on to the PicturePlane instances of :class:`PicturePlane`,
        :class:`Trihedron` and :class:`CoordinatePlane`.

    """

    def __init__(
        self,
        drawing: "Drawing",
        position: "Point",
        angles: Optional[tuple[float, float]] = None,
    ) -> None:
        """
        Args:
            drawing (:class:`.Drawing`):
                a Drawing instance to be passed on to the :class:`.PicturePlane`
                initiations of the :class:`PicturePlane`, :class:`Trihedron`
                and :class:`CoordinatePlane`
            angles (tuple(float, float)):
                axonometric angle pair. Defaults to None.
        """

        self.trihedron = Trihedron(drawing, position, angles)

    def add_geometry(
        self,
        geometry: Geometry | list[Geometry],
        style="trihedron",
    ) -> None:
        """Add geometries to the :class:`PicturePlane` components.

        Args:
            geometry: _description_
            style: _description_. Defaults to "picture_plane".
        """
        self.trihedron.add_geometry(geometry, style)

    def get_coordinate_plane(
        self, key: str
    ) -> Union[CoordinatePlaneXY, CoordinatePlaneYZ, CoordinatePlaneZX, None]:
        """Access a coordinate plane by its keys.

        Args:
            key (str(xy | yz | zx)):
                one of the three :class:`CoordinatePlane`

        Returns:
            :class:`CoordinatePlaneXY` |
            :class:`CoordinatePlaneYZ` |
            :class:`CoordinatePlaneZX`
        """
        return self.trihedron.coordinate_planes.get(key)

    def get_all_coordinate_planes(
        self,
    ) -> list[Union[CoordinatePlaneXY, CoordinatePlaneYZ, CoordinatePlaneZX]]:
        """Get a list of all three Coordinate Planes."""
        return list(self.trihedron.coordinate_planes.values())

    def get_projection_lines(self) -> list[Polyline]:
        """Get the lines from the coordinate plane projections.

        Returns:
            List of all projection lines from all three coordinate planes.
        """
        lines: list[Polyline] = []
        for plane in self.get_all_coordinate_planes():
            for line in plane._projections:
                lines.append(line)

        for line in self.trihedron._projections:
            lines.append(line)

        return lines


class Trihedron(PicturePlane):
    """Trihedron component class."""

    def __init__(
        self,
        drawing: "Drawing",
        position: "Point",
        angles: Optional[tuple[float, float]] = None,
    ) -> None:
        """
        Args:
            drawing: see above.
            angles: _description_. Defaults to None.
            position: _description_. Defaults to Point(0, 0).
        """
        super().__init__(drawing)
        self.name = "Trihedron"
        self.position = position
        if angles:
            print(self.name, "location:", self.position, "angles:", angles)
            self.axis: dict[str, Polyline] = self._trihedron_from_angles(
                self.position, angles
            )
        # elif lines:
        #     self.axis: Polyline = self._trihedron_from_lines(lines)
        self.add_geometry(self.get_all_axis(), "trihedron")  # PicturePlane function
        self.coordinate_planes: dict[
            str, CoordinatePlaneXY | CoordinatePlaneYZ | CoordinatePlaneZX
        ] = {}
        self._make_coordinate_planes()

    def _trihedron_from_angles(
        self, position: Point, angles: tuple[float, float]
    ) -> dict[str, Polyline]:
        p0 = position
        p1: Point = p0 + Point(10, 0)
        p2: Point = p0 + Point(-10, 0)
        p3: Point = p0 + Point(0, 10)
        a, b = angles
        alpha, beta = -radians(a), radians(b)
        # Make axis
        axis_x, axis_y, axis_z = (
            Polyline([p0, p1]),
            Polyline([p0, p2]),
            Polyline([p0, p3]),
        )
        # Rotate axis (following alpha/beta) into axonometric angles
        rotation = Rotation.from_axis_and_angle([0, 0, 1], alpha)
        axis_x.transform(rotation)
        rotation = Rotation.from_axis_and_angle([0, 0, 1], beta)
        axis_y.transform(rotation)

        return {"x": axis_x, "y": axis_y, "z": axis_z}

    # def _trihedron_from_lines(self, lines: Polyline) -> Optional[Polyline]:
    #     raise NotImplementedError

    def _make_coordinate_planes(self, start_axis: str = "x") -> None:
        """Construct the three :class:`CoordinatePlane` from :class:`Trihedron`.

        Args:
            start_axis: _description_. Defaults to "x".

        Returns:
            _description_
        """
        drawdown_planes: list[Polyline] = []
        point: Point = self.get_axis(start_axis).point(0.95)
        # progress from X -> Y -> Z
        for orthogonal, end_line, keys in zip(
            ["z", "x", "y"], ["y", "z", "x"], ["xy", "yz", "zx"]
        ):
            # -- Construct drawdown plane
            hinge, center, drawdown_plane, point = drawdown(
                self, point, orthogonal, end_line
            )
            drawdown_planes.append(drawdown_plane)
            # draw drawdown operations
            self.add_geometry(hinge, "hinge")
            self.add_geometry(center, "drawdown_sphere")
            self.add_geometry(drawdown_plane, "drawdown_plane")

            # -- Translate drawdown plane
            new_plane: Polyline
            trace: Polyline
            new_plane, trace = translate_plane_along_axis(
                drawdown_plane, self, orthogonal
            )
            # resize translated plane
            new_plane = resize_plane(new_plane, 10)
            # draw translation
            self.add_geometry(trace, "translation")

            # -- Instantiate coordinate plane objects
            if keys == "xy":
                self.coordinate_planes["xy"] = CoordinatePlaneXY(
                    self._drawing,
                    new_plane,
                    trace,
                    self,
                )

            elif keys == "yz":
                self.coordinate_planes["yz"] = CoordinatePlaneYZ(
                    self._drawing,
                    new_plane,
                    trace,
                    self,
                )

            elif keys == "zx":
                self.coordinate_planes["zx"] = CoordinatePlaneZX(
                    self._drawing,
                    new_plane,
                    trace,
                    self,
                )

    def get_axis(self, key: str) -> Polyline:
        return self.axis.get(key)

    def get_all_axis(self) -> list[Polyline]:
        return list(self.axis.values())

    def get_coordinate_plane(
        self, key: str
    ) -> Union[CoordinatePlaneXY, CoordinatePlaneYZ, CoordinatePlaneZX, None]:
        return self.coordinate_planes.get(key)


class CoordinatePlane(PicturePlane):
    """Base class for Coordinate Planes.

    .. important:: When adding geometries to a Coordinate Plane,
        a matrix transformation is required. Only :class:`CoordinatePlane`
        objects have matrix attributes. The ``no_matrix`` can disable
        when calling the function from :func:`add_geometry`.

    """

    def __init__(
        self, drawing: "Drawing", axis: Polyline, trace: Polyline, trihedron: Trihedron
    ) -> None:
        """
        Args:
            drawing: see above.
            axis: _description_
            trace: _description_
            trihedron: _description_
        """
        super().__init__(drawing)
        self.axis_polyline = axis
        self.vector: Vector = Vector.from_start_end(*trace).unitized() * -1
        self.trihedron = trihedron
        self.projection_lines: list[Polyline] = []
        self._matrix: list[list[float]] = compute_matrix_from_axis(self.axis_polyline)
        self.name = ""
        self.remaining_axis = ""

    def project_point_on_axis(self, point: Point) -> tuple[Point, Point]:
        return project_point_on_coordinate_plane_axis(self, point)

    def get_axis_by_key(self, key: str) -> Polyline:
        """Get 'x | y | z' axis :class:`compas.geometry.Polyline`

        Args:
            key (str): axis to select.

        Returns:
            The :class:`compas.geometry.Polyline` object of the axis.
        """
        return self.axis_lines.get(key)

    def get_others(self):
        return (
            self.trihedron.get_coordinate_plane(self.others[0]),
            self.trihedron.get_coordinate_plane(self.others[1]),
        )


class CoordinatePlaneXY(CoordinatePlane):
    """Coordinate Plane component class for XY"""

    def __init__(
        self, drawing: "Drawing", axis: Polyline, trace: Polyline, trihedron: Trihedron
    ) -> None:
        super().__init__(drawing, axis, trace, trihedron)
        self.name = "XY Coordinate Plane"
        self.keys = ("x", "y")
        self.remaining_axis = "z"
        self.others = ["yz", "zx"]
        # order axis
        self.x = Polyline([self.axis_polyline[1], self.axis_polyline[2]])
        self.y = Polyline([self.axis_polyline[0], self.axis_polyline[1]])
        self.add_geometry([self.x, self.y], "coordinate_plane", no_matrix=True)
        self.axis_lines = {"x": self.x, "y": self.y}


class CoordinatePlaneYZ(CoordinatePlane):
    """Coordinate Plane component class for YZ"""

    def __init__(
        self, drawing: "Drawing", axis: Polyline, trace: Polyline, trihedron: Trihedron
    ) -> None:
        super().__init__(drawing, axis, trace, trihedron)
        self.name = "YZ Coordinate Plane"
        self.keys = ("y", "z")
        self.remaining_axis = "x"
        self.others = ["zx", "xy"]
        # order axis
        self.y: Polyline = Polyline([self.axis_polyline[1], self.axis_polyline[2]])
        self.z: Polyline = Polyline([self.axis_polyline[0], self.axis_polyline[1]])
        self.add_geometry([self.y, self.z], "coordinate_plane", no_matrix=True)
        self.axis_lines: dict[str, Polyline] = {"y": self.y, "z": self.z}


class CoordinatePlaneZX(CoordinatePlane):
    """Coordinate Plane component class for ZX"""

    def __init__(
        self, drawing: "Drawing", axis: Polyline, trace: Polyline, trihedron: Trihedron
    ) -> None:
        super().__init__(drawing, axis, trace, trihedron)
        self.name = "ZX Coordinate Plane"
        self.keys = ("z", "x")
        self.remaining_axis = "y"
        self.others = ["xy", "yz"]
        # order axis
        self.z: Polyline = Polyline([self.axis_polyline[1], self.axis_polyline[2]])
        self.x: Polyline = Polyline([self.axis_polyline[0], self.axis_polyline[1]])
        self.add_geometry([self.z, self.x], "coordinate_plane", no_matrix=True)
        self.axis_lines: dict[str, Polyline] = {"z": self.z, "x": self.x}
