"""Simple polygon builder methods."""

import math
from typing import TYPE_CHECKING, Iterable, List

import shapely.wkt
from shapely.geometry import Point, Polygon

if TYPE_CHECKING:  # pragma: no cover
    from nzshm_common import CodedLocation


def create_hexagon(edge: float, x: float, y: float):
    """
    Create a hexagon centered on (x, y)
    :param edge: length of the hexagon's edge
    :param x: x-coordinate of the hexagon's center
    :param y: y-coordinate of the hexagon's center
    :return: The polygon containing the hexagon's coordinates
    """
    c = [
        [x + math.cos(math.radians(angle)) * edge, y + math.sin(math.radians(angle)) * edge]
        for angle in range(0, 360, 60)
    ]
    return Polygon(c)


def create_square_tile(dim: float, x: float, y: float):
    """
    Create a tile of size dim*dim, centered on (x, y)
    :param dim: length of the tiles edges
    :param x: x-coordinate of the tile's center
    :param y: y-coordinate of the tile's center
    :return: The polygon
    """
    offset = dim / 2
    c = [
        (x + offset, y + offset),
        (x + offset, y - offset),
        (x - offset, y - offset),
        (x - offset, y + offset),
        (x + offset, y + offset),
    ]
    return Polygon(c)


BA_POLYGON_WKT = (
    "POLYGON ((177.2 -37.715, 176.2 -38.72, 175.375 -39.27, "
    "174.25 -40, 173.1 -39.183, 171.7 -34.76, 173.54 -33.22, 177.2 -37.715))"
)


def backarc_polygon() -> Polygon:
    """
    Retrieve the backarc polygon from json and return shapely Polygon object
    """

    return shapely.wkt.loads(BA_POLYGON_WKT)


# TODO: consider if this function and any of the geometry operation functions belong in thier own repo. This
# would remove dependencies from what is supposed to be a pure python library and allow us to consolodate
# all geometry operations into one lib (including those in solvis and eq-fault-geom)
def within_polygon(locations: Iterable['CodedLocation'], polygon: Polygon) -> List[bool]:
    """
    Check if points are within a given polygon.
    Uses shapley.geometry.Polygon.contains() which will be false for points on the polygon boundary.

    Args:
        locations: the points to check
        polygon: the polygon

    Returns:
        A list of boolian values True if the point is within the polygon and False if not
    """

    points = [Point(loc.lon, loc.lat) for loc in locations]
    return [polygon.contains(point) for point in points]
