from pathlib import Path

import pytest

from nzshm_common.location.coded_location import CodedLocation
from nzshm_common.location.location import LOCATION_LISTS, get_locations

LOCATIONS_FILEPATH = Path(__file__).parent / 'fixtures' / 'location_file.csv'


def test_id():
    expected = [
        CodedLocation(lat=-41.3, lon=174.78, resolution=0.001),
        CodedLocation(lat=-36.87, lon=174.77, resolution=0.001),
    ]
    assert get_locations(["WLG", "AKL"]) == expected


def test_list():
    assert len(get_locations(["NZ", "SRWG214"])) == (
        len(LOCATION_LISTS["NZ"]["locations"]) + len(LOCATION_LISTS["SRWG214"]["locations"])
    )


def test_csv():
    expected = [
        CodedLocation(-41.2, 100.2, 0.001),
        CodedLocation(-30.5, 99, 0.001),
    ]
    assert get_locations([LOCATIONS_FILEPATH]) == expected


def test_mix():
    assert len(get_locations(["NZ", LOCATIONS_FILEPATH])) == 2 + len(LOCATION_LISTS["NZ"]["locations"])


def test_code():
    """Test for lat~lon code format."""
    expected = [
        CodedLocation(-41.2, 100.2, 0.001),
        CodedLocation(-30.5, 99, 0.001),
    ]
    assert (
        get_locations(["-41.200~100.200", "-30.500~99.000"]) == expected
    ), "Should work with codes at default resolution"
    assert (
        get_locations(["-41.2~100.2", "-30.5~99"]) == expected
    ), "Should work when code resolution doesn't exactly match, as long as values are correct"


def test_missing_location_name():
    with pytest.raises(KeyError, match="location missing_name is not a valid location identifier"):
        get_locations(["missing_name"])
