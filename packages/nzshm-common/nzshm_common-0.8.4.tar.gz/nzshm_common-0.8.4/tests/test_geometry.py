import math
import unittest

from nzshm_common import CodedLocation
from nzshm_common.grids import RegionGrid, load_grid

try:
    import shapely  # noqa

    from nzshm_common.geometry.geometry import (  # these require shapely
        create_hexagon,
        create_square_tile,
        within_polygon,
    )

    HAVE_SHAPELY = True
except ImportError:
    HAVE_SHAPELY = False


class TestSquareTile(unittest.TestCase):
    @unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")
    def test_adjacent_tiles_pt1(self):
        """Get some 0.1 degree locations, check we can build tiles."""

        RESOLUTION = 0.1  # degrees
        grid = RegionGrid['NZ_0_1_NB_1_1']

        cells = []
        for pt in grid.load()[30:33]:
            cells.append(create_square_tile(RESOLUTION, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))
        print('cell exterior', list(cells[0].exterior.coords))
        self.assertAlmostEqual(cells[0].distance(cells[1]), 0.0)


# TODO: need a different grid layout...
def create_hexgrid(bbox, side):
    """
    returns an array of Points describing hexagons centers that are inside the given bounding_box
    :param bbox: The containing bounding box. The bbox coordinate should be in Webmercator.
    :param side: The size of the hexagons'
    :return: The hexagon grid
    """
    pass


class TestHex(unittest.TestCase):

    unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")

    def test_create_hexagon(self):
        RESOLUTION = 1  # degrees
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        hex = create_hexagon(edge, x=-45, y=175)
        print(hex)
        self.assertAlmostEqual(-45, hex.centroid.bounds[0])  # latitude
        self.assertAlmostEqual(175, hex.centroid.bounds[1])  # longiutude

    unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")

    def test_adjacent_hexagons_pt2(self):
        """Get some 0.2 degree locations, check we can buld adjacent hexagons."""

        RESOLUTION = 0.2  # degrees
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        print(f'edge length {edge}')
        grid = load_grid('NZ_0_2_NB_1_1')

        cells = []
        for pt in grid[30:33]:
            cells.append(create_hexagon(edge, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))

        self.assertEqual(cells[0].distance(cells[1]), 0.0)

    unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")

    def test_adjacent_hexagons_pt1(self):
        """Get some 0.1 degree locations, check we can buld adjacent hexagons."""

        RESOLUTION = 0.1  # degrees
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        print(f'edge length {edge}')
        grid = load_grid('NZ_0_1_NB_1_1')

        cells = []
        for pt in grid[30:33]:
            cells.append(create_hexagon(edge, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))

        self.assertAlmostEqual(cells[0].distance(cells[1]), 0.0)


@unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")
def test_within_polygon():
    coords = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
    polygon = shapely.geometry.Polygon(coords)
    locations = [
        CodedLocation(0, 0, 0.001),
        CodedLocation(2, 2, 0.001),
        CodedLocation(0.5, 2, 0.001),
        CodedLocation(0.5, 0.5, 0.001),
    ]
    within_expected = [False, False, False, True]

    within = within_polygon(locations, polygon)

    assert len(within) == len(within_expected)
    assert within == within_expected
