import pytest

from nzshm_common.location.location import (
    DEFAULT_RESOLUTION,
    LOCATION_LISTS,
    get_location_list,
    get_location_list_names,
    get_locations,
)


def test_single_source():
    location_list = get_location_list(["NZ"])
    assert len(location_list) == len(LOCATION_LISTS["NZ"]["locations"]), "Should match count for NZ locations"

    location_list_codes = [loc.code for loc in location_list]
    assert get_locations(["AKL"])[0].code in location_list_codes, "Should find Auckland"
    assert get_locations(["DUD"])[0].code in location_list_codes, "Should find Dunedin"


def test_multiple_sources():
    location_list = get_location_list(["NZ", "SRWG214"])
    merged_locations = set(LOCATION_LISTS["NZ"]["locations"] + LOCATION_LISTS["SRWG214"]["locations"])
    assert len(location_list) == len(merged_locations), "List length equalling merge of two lists"


def test_source_overlaps():
    """
    Ensure that locations that appear in multiple lists are not duplicated.
    """
    nznz_list = get_location_list(["NZ", "NZ"])
    assert len(nznz_list) == len(LOCATION_LISTS["NZ"]["locations"]), "Should match count for single NZ location list"

    masterton = get_locations(["MRO"])[0]
    # Turning off sort_locations to make the test marginally faster for larger collections.
    nz_list = get_location_list(["NZ"], sort_locations=False)
    all_list = get_location_list(["ALL"], sort_locations=False)
    nz_all_list = get_location_list(["NZ", "ALL"], sort_locations=False)

    assert nz_list.count(masterton) == 1, "Should find Masterton in New Zealand once"
    assert all_list.count(masterton) == 1, "Should find Masterton in All once"
    assert nz_all_list.count(masterton) == 1, "Should find Masterton in combined list once"


def test_missing_source():
    with pytest.raises(KeyError):
        get_location_list(["unknown"])

    with pytest.raises(KeyError):
        get_location_list(["NZ", "unknown"])

    location_list = get_location_list([])
    assert len(location_list) == 0, "Should be an empty list"


def test_resolution_override():
    custom_resolution = 0.1
    assert DEFAULT_RESOLUTION != custom_resolution, "Tested resolutions should be different"

    location_list = get_location_list(["NZ"], resolution=custom_resolution)
    assert len(location_list) == len(LOCATION_LISTS["NZ"]["locations"]), "Should match count for NZ locations"

    location_list_codes = [loc.code for loc in location_list]
    assert (
        get_locations(["AKL"])[0].code not in location_list_codes
    ), "Should not find Auckland code at default resolution"
    assert (
        get_locations(["AKL"], resolution=custom_resolution)[0].code in location_list_codes
    ), "Should find Auckland code at custom resolution"


def test_names():
    name_list = get_location_list_names()
    assert "NZ" in name_list, "Should contain NZ location list"
    assert "SRWG214" in name_list, "Should contain SRWG214 location list"
    assert "NZ_0_1_NB_1_0" not in name_list, "Should not include grid names"
