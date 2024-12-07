from typing import Iterable

import pytest

from nzshm_common.grids import RegionGrid, get_location_grid, get_location_grid_names, load_grid
from nzshm_common.location import CodedLocation


def test_load_wlg_0_005():
    assert len(load_grid('WLG_0_05_nb_1_1')) == 62


def test_load_wlg_0_001():
    assert len(load_grid('WLG_0_01_nb_1_1')) == 764


def test_load_nz_0_1():
    assert len(load_grid('NZ_0_1_NB_1_1')) == 3741


def test_load_lat_lon_order_spacing():
    """Coordinate order must be lat, lon."""
    grid = load_grid('NZ_0_1_NB_1_0')
    assert grid[0] == (-46.1, 166.4)
    assert grid[1] == (-46.0, 166.4)

    grid = load_grid('NZ_0_1_NB_1_1')
    assert grid[0] == (-46.1, 166.4)
    assert grid[1] == (-46.0, 166.4)

    grid = load_grid('NZ_0_2_NB_1_1')
    assert grid[0] == (-46.4, 166.6)
    assert grid[1] == (-46.2, 166.6)

    grid = load_grid('WLG_0_05_nb_1_1')
    assert grid[0] == (-41.4, 174.65)
    assert grid[1] == (-41.35, 174.65)
    assert grid[2] == (-41.3, 174.65)

    grid = load_grid('WLG_0_01_nb_1_1')
    assert grid[0] == (-41.36, 174.69)
    assert grid[1] == (-41.35, 174.69)
    assert grid[2] == (-41.34, 174.69)


def test_get_location_grid_default():
    """Test get_location_grid with standard default resolution."""
    # LatLons for comparison
    baseline_grid = load_grid("WLG_0_05_nb_1_1")

    grid_list = get_location_grid("WLG_0_05_nb_1_1")

    assert isinstance(grid_list, Iterable), "Should be Iterable"
    assert isinstance(grid_list[0], CodedLocation), "Should contain CodedLocation values"
    assert grid_list[0].resolution == RegionGrid.WLG_0_05_nb_1_1.resolution, "Should have grid default resolution"

    assert len(grid_list) == len(baseline_grid), "Should have a CodedLocation for each grid coordinate"
    assert grid_list[0].as_tuple == baseline_grid[0], "Preserving grid ordering"
    assert grid_list[1].as_tuple == baseline_grid[1], "Preserving grid ordering"
    assert grid_list[2].as_tuple == baseline_grid[2], "Preserving grid ordering"


def test_get_location_grid_downsampling():
    """Test behaviours of get_location_grid when setting a lower resolution."""
    # Load at default resolution for comparison
    grid_list = get_location_grid("WLG_0_05_nb_1_1")

    expected_message = "The requested resolution is lower than the grid resolution and will result in fewer points."

    with pytest.warns(UserWarning) as warnings:
        grid_downsampled = get_location_grid("WLG_0_05_nb_1_1", resolution=0.1)

    assert isinstance(grid_downsampled, Iterable), "Should be Iterable"
    assert isinstance(grid_downsampled[0], CodedLocation), "Should contain CodedLocation values"
    assert len(grid_list) > len(grid_downsampled), "Should have fewer downsampled coordinates"

    assert grid_list[0].as_tuple == (-41.4, 174.65), "Baseline value 0"
    # -- Skipped duplicated grid point --
    assert grid_list[2].as_tuple == (-41.3, 174.65), "Baseline value 2"
    # -- Skipped duplicated grid point --
    assert grid_list[4].as_tuple == (-41.35, 174.7), "Baseline value 4"

    assert grid_downsampled[0].as_tuple == (-41.4, 174.6), "Downsampled value 0"
    assert grid_downsampled[1].as_tuple == (-41.3, 174.6), "Downsampled value 1"
    assert grid_downsampled[2].as_tuple == (-41.4, 174.7), "Downsampled value 2"

    resample = grid_downsampled[0].resample(0.001)
    assert grid_downsampled[0] != resample, "Same locations at different resolutions are not considered equal"
    assert (
        grid_downsampled[0].as_tuple == resample.as_tuple
    ), "CodedLocations at different resolutions can be compared as LatLon values"

    assert len(warnings) == 1, "Should only be warned about downsampling"
    assert str(warnings[0].message) == expected_message, "Should have matched expected message"
    assert warnings[0].filename == __file__, "Should have been attributed to this caller"


def test_get_location_grid_names():
    name_list = get_location_grid_names()
    assert isinstance(name_list, Iterable), "Should be Iterable type"
    assert "NZ_0_1_NB_1_0" in name_list, "Should include NZ_... grids"
    assert "WLG_0_01_nb_1_1" in name_list, "Should include WLG_... grids"
    assert "SRWG214" not in name_list, "Should not include location list names"
