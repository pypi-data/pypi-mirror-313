# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This package collects miscellaneous functionality mostly for animation & file
handling puropses. This was used before but needs a complete rewriting.
"""
from typing import List, Any, Union

from compas_plotters import Plotter
from vpype_cli import execute
from vpype import read_multilayer_svg
from PIL import Image
import datetime
import lxml.etree


# -- Metadata -----------------------------------------------------------------


def cartouche():
    """
    drawing DNA
    """
    pass


# -- Animation ----------------------------------------------------------------


def flatten(list_of_lists: List[Any]) -> List[Any]:
    """
    `source <https://stackabuse.com/python-how-to-flatten-list-of-lists/>`__
    """
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


def animate(plotter: Plotter, objects: List[Any], file: str) -> None:
    """
    make gif with each added object as a frame
    """

    @plotter.on(interval=0.1, frames=len(objects), record=True, recording=file)
    def add_objects(frame) -> None:
        plotter.add(objects[frame], size=10)


def save_snapshot(plotter: Plotter, path: str = "./output/tmp/") -> None:
    """
    :param plotter:
    :param path: (str) path at which to make a temporary directory for frames.

    `source <https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-timestamp-in-python/>`__
    """
    # TODO make directory
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000
    # save to file
    # plotter.zoom_extents()
    plotter.save("{}{}.png".format(path, int(unix_timestamp)), bbox_inches="tight")


def get_time_stamp() -> int:
    """
    source: https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-timestamp-in-python/
    """
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000
    return int(unix_timestamp)


# -- File Handling ------------------------------------------------------------


def _clean_svg(files: Union[str, List[str]]) -> None:
    """
    Save files with vpype in order to simplify SVG elements.
    """
    files = files if isinstance(files, list) else [files]

    for svg_file in files:
        drawing = read_multilayer_svg(svg_file, 0.4)
        drawing = execute("write {}".format(svg_file), drawing)

    return None


def clean_matplot_svg(files: Union[str, List[str]]) -> None:
    """
    Clean SVG from matplotlib frame polygon by first occurrence.
    """
    files = files if isinstance(files, list) else [files]

    # simplify svg files
    _clean_svg(files)

    for file in files:
        with open(file, "r") as f:
            tree = lxml.etree.parse(f)
            root = tree.getroot()

            for element in root.iter("*"):
                if "polygon" in element.tag:
                    # first occurrence
                    element.getparent().remove(element)
                    break

        with open(file, "w") as ff:
            ff.write(lxml.etree.tostring(tree, encoding="unicode"))


def a1_svg(
    files: Union[str, List[str]], papersize: str = "a1", align: str = "center"
) -> None:
    """
    Optimize svg for plotting with vpype
    """

    files = files if isinstance(files, list) else [files]

    for svg_file in files:
        drawing = read_multilayer_svg(svg_file, 0.4)
        # layout on a1 but don't optimize to keep construction order
        drawing = execute(
            "layout --fit-to-margins 5cm --valign {} {} write {}\
                            ".format(
                align, papersize, svg_file
            ),
            drawing,
        )
    # See this for series :
    # https://vpype.readthedocs.io/en/latest/cookbook.html#laying-out-multiple-svgs-on-a-grid

    return None


def resize_png(file: str, factor: int = 2) -> None:
    image = Image.open(file)
    x, y = image.size
    image.thumbnail((x // factor, y // factor))
    image.save(file)


def svg_to_gcode(files: list[str], profile: str = "05") -> None:
    # vpype forfile "*.svg" \
    #     read "%_path%" \
    #     gwrite -p 05 "%_path.parent / _path.stem%.gcode" \
    # end
    pass
