import random
import unittest

import pytest

from nzshm_common import CodedLocation, LatLon
from nzshm_common.constants import DEFAULT_RESOLUTION
from nzshm_common.grids.region_grid import load_grid
from tests.helpers import does_not_raise

GRID_02 = load_grid('NZ_0_2_NB_1_1')
LOCS = [CodedLocation(loc[0], loc[1], 0.001) for loc in GRID_02[20:50]]  # type: ignore


def test_coded_location_is_hashable():
    c = CodedLocation(-45.2, 175.2, 0.1)
    s = set()
    s.add(c)
    assert c in s


class CodedLocationResampling(unittest.TestCase):
    def test_get_nearest_hazard_for_an_arbitrary_location(self):
        gridloc = random.choice(LOCS)
        print(f'gridloc {gridloc}')

        off_lat = round(gridloc.lat + random.randint(0, 9) * 0.01, 3)
        off_lon = round(gridloc.lon + random.randint(0, 9) * 0.01, 3)
        somewhere_off_grid = CodedLocation(off_lat, off_lon, 0.001)

        nearest_grid = somewhere_off_grid.downsample(0.2)

        print(f'somewhere_off_grid {somewhere_off_grid}')
        print(f'nearest_grid {nearest_grid}')

        self.assertEqual(gridloc, nearest_grid.resample(0.001))
        self.assertEqual(gridloc, nearest_grid.downsample(0.001))
        self.assertEqual(gridloc.code, nearest_grid.downsample(0.001).code)

        self.assertEqual(gridloc, CodedLocation(nearest_grid.lat, nearest_grid.lon, 0.001))
        self.assertTrue(CodedLocation(nearest_grid.lat, nearest_grid.lon, 0.001) in LOCS)


oh_point_five_expected = [
    (-45.27, 171.1, '-45.5~171.0'),
    (-45.23, 171.1, '-45.0~171.0'),
    (-45.27, 171.4, '-45.5~171.5'),
    (-45.27, 171.8, '-45.5~172.0'),
    (-41.3, 174.783, '-41.5~175.0'),  # WLG
]


def test_as_tuple():
    c = CodedLocation(-45.2, 175.2, 0.1)

    assert isinstance(c.as_tuple, LatLon)
    assert c.as_tuple.latitude == -45.2
    assert c.as_tuple.longitude == 175.2
    assert c.as_tuple[0] == -45.2
    assert c.as_tuple[1] == 175.2


@pytest.mark.parametrize("lat,lon,expected", oh_point_five_expected)
def test_coded_location_equality(lat, lon, expected):
    c0 = CodedLocation(lat, lon, 0.5)
    c1 = CodedLocation(lat, lon, 0.5)
    assert c0 == c1


def test_coded_location_from_tuple():
    coded_loc = CodedLocation.from_tuple(LatLon(latitude=-45.27, longitude=171.14))
    assert isinstance(coded_loc, CodedLocation), "Return type should be CodedLocation"
    assert coded_loc.resolution == DEFAULT_RESOLUTION, "Should have default resolution"
    assert coded_loc.lat == -45.27, "Latitude should match"
    assert coded_loc.lon == 171.14, "Longitude should match"

    # A naked (latitude, longitude) tuple with the same values should work also.
    coded_loc_lores = CodedLocation.from_tuple((-45.27, 171.14), resolution=0.1)
    assert coded_loc_lores.resolution == 0.1, "Should have lowered resolution"
    assert coded_loc_lores.lat == -45.3, "Should have rounded latitude"
    assert coded_loc_lores.lon == 171.1, "Should have rounded longitude"


@pytest.mark.parametrize(
    "lat,lon,is_before,is_code_before,description",
    [
        (-45.1, +171.3, 1, 1, "0.1 North 0.1 West"),
        (-45.1, +171.4, 1, 1, "0.1 North"),
        (-45.1, +171.5, 1, 1, "0.1 North 0.1 East"),
        (-45.2, +171.3, 1, 1, "0.1 West"),
        (-45.2, +171.4, 0, 0, "Reference (in Southern/Eastern Hemispheres)"),
        (-45.2, +171.5, 0, 0, "0.1 East"),
        (-45.3, +171.3, 0, 0, "0.1 South 0.1 West"),
        (-45.3, +171.4, 0, 0, "0.1 South"),
        (-45.3, +171.5, 0, 0, "0.1 South 0.1 East"),
        (+45.2, -171.4, 1, 0, "Northern / Western Hemispheres (code sort inverts lat)"),
        (+45.2, +171.4, 1, 0, "Northern / Eastern Hemispheres (code sort inverts lat)"),
        (-45.2, -171.4, 1, 1, "Southern / Western Hemispheres"),
    ],
)
def test_coded_location_ordering(lat, lon, is_before, is_code_before, description):
    """
    Characterising differences in sorting arithmetically by latitude then
    longitude, versus alphanumeric .code sorting.

    Alpha sorting works for New Zealand because we have a negative latitude,
    but would sort in the opposite direction for the northern hemisphere.

    For arithmetic comparisons we expect:

    - North before Sorth, or
    - West before East when on the same latitude
    """
    reference_point = CodedLocation(-45.24, 171.4, 0.1)
    is_before = bool(is_before)
    is_code_before = bool(is_code_before)

    target = CodedLocation(lat, lon, 0.1)
    assert (target < reference_point) == is_before, f"Comparison expected: {is_before}"
    assert (target.code < reference_point.code) == is_code_before, f"Code comparison expected: {is_code_before}"


@pytest.mark.parametrize("lat,lon,expected", oh_point_five_expected)
def test_downsample_default_oh_point_five_no_downsampling_required(lat, lon, expected):
    print(f"lat {lat} lon {lon} -> {expected}")
    assert CodedLocation(lat, lon, 0.5).code == expected


@pytest.mark.parametrize("lat,lon,expected", oh_point_five_expected)
def test_downsample_default_oh_point_five(lat, lon, expected):
    print(f"lat {lat} lon {lon} -> {expected}")
    c = CodedLocation(lat, lon, 0.5)
    assert c.downsample(0.5).code == expected


@pytest.mark.parametrize(
    "lat,lon,expected",
    [
        (-45.27, 171.1, '-45.0~171.0'),
        (-45.23, 171.1, '-45.0~171.0'),
        (-45.77, 171.4, '-46.0~171.0'),
        (-45.27, 171.8, '-45.0~172.0'),
        (-41.3, 174.78, '-41.0~175.0'),  # WLG
    ],
)
def test_downsample_one_point_oh(lat, lon, expected):
    c = CodedLocation(lat, lon, 1.0)
    assert c.downsample(1.0).code == expected


@pytest.mark.parametrize(
    "lat,lon,expected",
    [
        (-45.27, 171.1, '-45.3~171.1'),
        (-45.239, 171.13, '-45.2~171.1'),
        (-45.27, 171.4, '-45.3~171.4'),
        (-45.27, 171.8, '-45.3~171.8'),
        (-41.333, 174.78, '-41.3~174.8'),  # WLG
    ],
)
def test_downsample_oh_point_one(lat, lon, expected):
    c = CodedLocation(lat, lon, 0.1)
    assert c.downsample(0.1).code == expected


@pytest.mark.parametrize(
    "lat,lon,expected",
    [
        (-45.27, 171.111, '-45.25~171.10'),
        (-45.239, 171.73, '-45.25~171.75'),
        (45.126, 171.4, '45.15~171.40'),
        (-45.27, 171.03, '-45.25~171.05'),
        (-41.333, 174.78, '-41.35~174.80'),  # WLG
    ],
)
def test_downsample_oh_point_oh_five(lat, lon, expected):
    c = CodedLocation(lat, lon, 0.05)
    assert c.downsample(0.05).code == expected


@pytest.mark.parametrize(
    "resolution, expectation",
    [
        (-0.1, pytest.raises(AssertionError)),
        (0.0, pytest.raises(AssertionError)),
        (0.05, does_not_raise()),
        (0.1, does_not_raise()),
        (150, does_not_raise()),
        (180, pytest.raises(AssertionError)),
    ],
)
def test_resolution_bounds(resolution, expectation):
    """Ensure invalid resolutions throw an assertion error before calculating."""
    with expectation:
        CodedLocation(-41.333, 174.78, resolution)
