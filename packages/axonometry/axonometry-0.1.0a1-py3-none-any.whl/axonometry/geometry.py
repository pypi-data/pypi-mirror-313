# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

# TODO: implement custom geometry, with functions to give them projective features ?
# TODO coherent use of source/target pattern for geometric operations

"""
This package collects geometric functions.
"""
from __future__ import annotations
from compas.geometry import (
    Point,
    Line,
    Polyline,
    Circle,
    Frame,
    Translation,
    Rotation,
    Vector,
)
from compas.geometry import (
    convex_hull_xy,
    midpoint_line_xy,
    matrix_from_frame,
    centroid_points_xy,
    project_point_line_xy,
    distance_point_point_xy,
    intersection_line_line_xy,
)
import itertools
from random import randint

# imports for type checking
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .axonometry import (
        CoordinatePlane,
        Trihedron,
        CoordinatePlaneXY,
        CoordinatePlaneYZ,
        CoordinatePlaneZX,
    )


def project_axonometric_image(
    coordinate_plane: "CoordinatePlaneXY | CoordinatePlaneYZ | CoordinatePlaneZX | None",
    point,
    dist: int = 35,
) -> Polyline:
    """
    project geometry from coordinate plane on axonometry frame
    TODO variables for projection, project collection

    Source: one of the three cooridinate planes
    Target (implicit): the axonometric image is linked to the Trihedron object

    """
    # compute projection line
    intersection_p = point + coordinate_plane.vector * dist  # ! bad naming
    line = Polyline([point, intersection_p])
    # add line to its coordinate plane
    # i.e. add_geometry without matrix
    coordinate_plane.trihedron.project_geometry(line, "projection")
    return line


def compute_matrix_from_axis(polyline: Polyline) -> list[list[float]]:
    """Compute a matrix of a ~CoordinatePlane.

    A matrix is necessary to add geometry to a ~CoordinatePlane.

    Args:
        polyline (`~comaps.geometry.Polyline`): The two lines definining a
        `~CoordinatePlane`.

    Returns:
        list[list[float]]: 4x4 transformation matrix.
    """
    # make frame
    point = polyline[1]
    axis_1 = polyline.lines[0].vector.unitized() * -1
    axis_2 = polyline.lines[1].vector.unitized()
    F: Frame = Frame(point, axis_1, axis_2)
    # get frame matrix
    return matrix_from_frame(F)


def get_intersection_outline(lines: list[Polyline]) -> Polyline:
    """
    :param lines: (Polyline) lines to check for intersection.
    :return: Polyline of outline of given points
    """
    points = get_intersection_points(lines)
    # convex hull from intersections points
    outline = convex_hull_xy(points)
    outline.append(outline[0])  # close the outline segment

    return Polyline(outline)


def resize_plane(plane: Polyline, n: int = 10) -> Polyline:
    """
    resize axis of coordinate plane by n
    """
    c = plane[1]
    v1 = Line(c, plane[0]).vector.unitized() * n
    v2 = Line(c, plane[2]).vector.unitized() * n
    new_plane = Polyline([c + v1, c, c + v2])
    return new_plane


def translate_plane_along_axis(
    plane: Polyline, trihedron: "Trihedron", axis: Polyline, factor=1.5
) -> tuple[Polyline, Polyline]:
    """With a given axis from the :class:`.Trihedron` translate a plane
    (defined as `compas.geometry.Polyline`) along it.

    Once the drawdown operations defined the various :class:`.CoordinatePlane`,
    this function translates these planes away from the :class:`.Trihedron`.

    Args:
        plane:
            :class:`compas.geometry.Polyline` resulting from the various :func:`drawdown`.
        trihedron:
            :class:`.Trihedron` defining the :class:`.Axonometry`
        axis:
            one axis from :class:`.Trihedron`
        factor:
            multiplication of length of axis. Defaults to 1.5.

    Returns:
        New plane (:class:`compas.geometry.Polyline` at 90°) which will
        become a :class:`.CoordinatePlane` and a
        :class:`compas.geometry.Polyline` keeping a visual trace of
        the translation:

        (:class:`compas.geometry.Polyline`, :class:`compas.geometry.Polyline`)
    """
    # Translate by making axis longer
    T = Translation.from_vector(
        trihedron.axis[axis].lines[0][1] * -factor
    )  # minus is for direction
    # keep original and translate new one
    new_plane = plane.transformed(T)
    # translation_trace = Polyline([plane.lines[0][1], new_plane.lines[0][1]])
    translation_trace = Polyline([trihedron.position, new_plane.lines[0][1]])
    # translation trace
    return new_plane, translation_trace


def drawdown(
    trihedron: "Trihedron", point: Point, i: Polyline, j: Polyline
) -> tuple[Polyline, Circle, Polyline, Point]:
    """Construct three :class:`.CoordinatePlane` from :class:`.Trihedron`.

    Warning:
        Certain axonometry angles are not yet supported. A check has to be
        implemented in order to determine the best starting point relative
        to the :class:`.Trihedron` shape. The edge cases of angles 45/45 and 0/90/0
        have to be handled appart.


    Args:
        trihedron (:class:`.Trihedron`):
            Axonometric projection of xy, yz, zx planes.
        point (:class:`compas.geometry.Point`):
            selection from axis of the ``trihedron``.
        i (:class:`compas.geometry.Polyline`):
            next axis, opposite from the previous ``point``.
        j (:class:`compas.geometry.Polyline`):
            third axis of the ``trihedron``.

    Important:
        The function is called three times in a loop around the
        :class:`.Trihedron` axis.

    Returns:
        Traces and result of a single drawdown operation + a point to continue
        with the remaining drawdown operations to be performed:

        (``hinge`` *of rotation*, ``circle`` *projection of drawdown sphere*,
        ``plane`` *resulting coordinate plane axis*, ``next_point`` *for the next
        drawdown*)

    """
    vertical_plane = trihedron.axis[i]
    opposite_axis = trihedron.axis[j]
    # 1 selection point on axis
    p1 = point
    # 2 draw orthogonal projection
    perpendicular = Point(*project_point_line_xy(p1, vertical_plane))
    p2 = Point(*intersection_line_line_xy(Line(p1, perpendicular), opposite_axis))
    hinge = Polyline([p1, p2])
    next_point = p2
    # 3 draw sphere (circle of drawdown)
    center = midpoint_line_xy(hinge.lines[0])
    radius = hinge.lines[0].length / 2
    circle = Circle([center, [0, 0, 1]], radius)
    pt1 = (vertical_plane.lines[0][0][0], vertical_plane.lines[0][0][1])
    pt2 = (vertical_plane.lines[0][1][0], vertical_plane.lines[0][1][1])
    p3 = circle_line_segment_intersection(
        (center[0], center[1]), radius, pt1=pt1, pt2=pt2, full_line=False
    )
    try:
        p3 = Point(*p3[0])
    except Exception as e:
        print(
            """
            Issue with angles...
            Maybe getting too close to an oblique projection.
            Exception: {}
            """.format(
                e
            )
        )
        exit()
    # 4 join intersections for coordinate plane drawdown
    plane = Polyline([p2, p3, p1])

    return hinge, circle, plane, next_point


def get_intersection_points(
    lines: list[Polyline], n: int = 3, tol: float = 0.5
) -> list[Point]:
    """
    Find points of intersection between a set of lines.
    TODO research a generic function which returns the points
    and their number of intersections.

    :param lines (list): Polylines to check intersection
    :param n (int): number of intersections to check. Max. 3.
    :param tol (float): distance tolerance to consider point as intersection.

    :return: Polyline of intersection

    """
    # TODO: make double intersections (condition: not in triple)
    # get triple intersection points
    if n == 3:
        inter_points = []
        for a, b, c in itertools.combinations(lines, 3):
            p_1 = intersection_line_line_xy(a, b)
            p_2 = intersection_line_line_xy(b, c)
            p_3 = intersection_line_line_xy(c, a)
            # first check if intersection exists
            if p_1 and p_2 and p_3:
                # check if points are identical by their distance
                if (
                    distance_point_point_xy(p_1, p_2) < tol
                    and distance_point_point_xy(p_2, p_3) < tol
                    and distance_point_point_xy(p_3, p_1) < tol
                ):
                    inter_points.append(Point(*centroid_points_xy([p_1, p_2, p_3])))

    return inter_points


def all_angles(
    step: int = 1,
    remove_equivalent: bool = False,
    convention: Optional[str] = NotImplemented,
) -> list[tuple[int, int]]:
    """
    For animation or exhaustive generations.
    0 <= a <= 90
    0 <= b <= 90
    (90-b)+(90-a) >= 90
    """

    # make all permutations
    start = 1
    stop = 89
    step = step
    # create a range of numbers from start to stop, with step size
    nums = range(start, stop + 1, step)
    # generate all possible permutations of length 2
    perms = list(itertools.permutations(nums, 2))

    # verify condition for axonometric projection
    res = []
    for a, b in perms:
        if (90 - b) + (90 - a) >= 90:
            if remove_equivalent:
                if (b, a) in res:
                    continue
            res.append((a, b))

    return res


def circle_line_segment_intersection(
    circle_center: tuple[float, float],
    circle_radius: float,
    pt1: tuple[float, float],
    pt2: tuple[float, float],
    full_line: bool = True,
    tangent_tol: float = 1e-9,
) -> list[tuple[float, float]]:
    """Find the points at which a circle intersects a line-segment.
    This can happen at 0, 1, or 2 points.

    :param circle_center: The (x, y) location of the circle center
    :param circle_radius: The radius of the circle
    :param pt1: The (x, y) location of the first point of the segment
    :param pt2: The (x, y) location of the second point of the segment
    :param full_line: True to find intersections along full line -
           not just in the segment.  False will just return intersections
           within the segment.
    :param tangent_tol: Numerical tolerance at which we decide the
           intersections are close enough to consider it a tangent
    :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where
            each element is a point at which the circle intercepts a line
            segment.

    Note: we follow http://mathworld.wolfram.com/Circle-LineIntersection.html
    Source: https://stackoverflow.com/a/59582674
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx**2 + dy**2) ** 0.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius**2 * dr**2 - big_d**2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (
                cx
                + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**0.5)
                / dr**2,
                cy + (-big_d * dx + sign * abs(dy) * discriminant**0.5) / dr**2,
            )
            # This makes sure the order along the segment is correct
            for sign in ((1, -1) if dy < 0 else (-1, 1))
        ]
        if not full_line:
            # If only considering the segment, filter out
            # intersections that do not fall within the segment
            fraction_along_segment = [
                (xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy
                for xi, yi in intersections
            ]
            intersections = [
                pt
                for pt, frac in zip(intersections, fraction_along_segment)
                if 0 <= frac <= 1
            ]
        # If line is tangent to circle, return just one point
        # (as both intersections have same location)
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:
            return [intersections[0]]
        else:
            return intersections


def random_angles(convention: Optional[str] = NotImplemented) -> list[int]:
    """
    compute angle > 90.
    """
    a = randint(1, 88)
    b = randint(1, 89 - a)
    while a == 45 and a == b:
        # BUG: 45/45 not working for construction.
        b = randint(1, 89 - a)
    return sorted([a, b])


def project_point_on_coordinate_plane(
    point: Point, coordinate_plane: "CoordinatePlane", dist: int = 30
) -> Point:
    """Project an object from the axonometric picture plane on a
    given coordinate plane."""
    intersection_p = point + (coordinate_plane.vector * dist) * -1
    trace = Polyline([point, intersection_p])
    coordinate_plane.project_geometry(trace)
    return intersection_p


def project_axo_point_on_all_coordinate_planes(
    axo_point: Point,
    coordinate_plane_point: Point,
    coordinate_plane: "CoordinatePlane",
) -> None:
    # -- 1. Find points on known axis
    axis_point_cw, axis_point_ccw = propagate_coordinate_plane_point_axis(
        coordinate_plane_point, coordinate_plane
    )

    # -- 2. Link new points with original axonometric point
    destination_cw, destination_ccw = coordinate_plane.get_others()

    for axis_point, destination in zip(
        [axis_point_cw, axis_point_ccw], [destination_cw, destination_ccw]
    ):
        axo_point_projection = Line(
            axo_point, (axo_point + destination.vector)
        )  # project axo_point along the coordinate plane vector

        projection_line = Line(
            axis_point,
            axis_point
            + Line(
                *destination.get_axis_by_key(coordinate_plane.remaining_axis)
            ).vector,
        )  # project axis_point along the remaining axis vector
        destination_point = Point(
            *intersection_line_line_xy(axo_point_projection, projection_line)
        )
        # destination.project_point_on_axis(destination_point)  # not working somehow...
        destination.project_geometry(
            [
                Polyline([destination_point, axis_point]),
                Polyline([destination_point, axo_point]),
            ]
        )  # workaround
        new_axis_point = Point(
            *project_point_line_xy(
                destination_point,
                Line(*destination.get_axis_by_key(coordinate_plane.remaining_axis)),
            )
        )  # find second and last axis_point for coordinate plane

        # -- 3. Add third axis point
        destination.project_geometry(Polyline([destination_point, new_axis_point]))

        projection_line = Line(new_axis_point, (new_axis_point + destination.vector))
        trihedron_line = Line(
            *coordinate_plane.trihedron.get_axis(coordinate_plane.remaining_axis)
        )
        trihedron_point = Point(
            *intersection_line_line_xy(trihedron_line, projection_line)
        )

        coordinate_plane.project_geometry(Polyline([trihedron_point, new_axis_point]))


def propagate_coordinate_plane_point_axis(
    coordinate_plane_point: Point,
    coordinate_plane: "CoordinatePlane",
) -> list[Point]:
    """Propagate a point in :class:`.CoordinatePlane` onto the
    known axis of the two other Coordinate Planes.

    Args:
        coordinate_plane_point: the point contained in a :class:`.CoordinatePlane`.
        coordinate_plane: the :class:`.CoordinatePlane` from where the operation starts.

    Returns:
        A dictionnary with axis keys and the resulting points.
        Each is on one of the two different Coordinate Planes.
    """
    result_points = []  # cw - ccw order

    # -- Prepare variables
    axis_ccw, axis_cw = coordinate_plane.keys
    trihedron = coordinate_plane.trihedron
    destination_cw, destination_ccw = coordinate_plane.get_others()
    axis_point_ccw, axis_point_cw = coordinate_plane.project_point_on_axis(
        coordinate_plane_point
    )  # get the axis_points

    # -- Propagate point on known axis in CW and CCW order
    for destination, axis, axis_point in zip(
        [destination_cw, destination_ccw],
        [axis_cw, axis_ccw],
        [axis_point_cw, axis_point_ccw],
    ):
        # -- Project point on coordinate plane axis
        destination.project_geometry(Polyline([coordinate_plane_point, axis_point]))

        # -- Project axis_points on Trihedron axis
        trihedron_axis = trihedron.get_axis(axis)
        trihedron_axis = Line(trihedron_axis[0], trihedron_axis[1])
        projection_line = Line(axis_point, (axis_point + coordinate_plane.vector))
        trihedron_axis_point = Point(
            *intersection_line_line_xy(trihedron_axis, projection_line)
        )
        destination.project_geometry(Polyline([axis_point, trihedron_axis_point]))

        # -- Project Trihedron axis point on destination Coordinate Plane axis
        coordinate_plane_axis = destination.get_axis_by_key(axis)
        coordinate_plane_axis = Line(coordinate_plane_axis[0], coordinate_plane_axis[1])
        projection_line = Line(
            trihedron_axis_point, (trihedron_axis_point + destination.vector)
        )
        coordinate_plane_axis_point = Point(
            *intersection_line_line_xy(coordinate_plane_axis, projection_line)
        )
        destination.project_geometry(
            Polyline([trihedron_axis_point, coordinate_plane_axis_point])
        )

        # -- Add resulting point
        result_points.append(coordinate_plane_axis_point)

    return result_points


def project_point_on_coordinate_plane_axis(
    coordinate_plane: "CoordinatePlane",
    point: Point,
) -> tuple[Point, Point]:
    """Project a coordinate point on each axis.

    Args:
        coordinate_plane (:class:`.CoordinatePlane`):
            the coordinate plane which contains ``point``.
        point (:class:`compas.geometry.Point`):
            a point to project on the axis.

    Returns:
        tuple(:class:`compas.geometry.Point`, :class:`compas.geometry.Point`):

            One point per axis.
    """
    axis_polyline = coordinate_plane.axis_polyline

    l1 = Line(axis_polyline[1], axis_polyline[2])
    l2 = Line(axis_polyline[0], axis_polyline[1])

    p1 = project_point_line_xy(point, l1)
    p2 = project_point_line_xy(point, l2)

    return Point(*p1), Point(*p2)
