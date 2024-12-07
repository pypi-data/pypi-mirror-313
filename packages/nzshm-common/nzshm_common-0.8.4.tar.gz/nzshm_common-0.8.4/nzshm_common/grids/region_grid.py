import warnings
from collections import namedtuple
from enum import Enum
from functools import partial
from typing import Iterable, List, Optional

from nzshm_common.grids.nz_0_1_nb_1_v0 import NZ01nb1v0
from nzshm_common.grids.nz_0_1_nb_1_v1 import NZ01nb1v1
from nzshm_common.grids.nz_0_2_nb_1_1 import NZ_0_2_nb_1_1
from nzshm_common.grids.wlg_0_01_nb_1_1 import WLG_0_01_nb_1_1
from nzshm_common.grids.wlg_0_05_nb_1_1 import WLG_0_05_nb_1_1
from nzshm_common.location.coded_location import CodedLocation
from nzshm_common.location.types import LatLon

RegionGridEntry = namedtuple("RegionGridEntry", "region_name resolution neighbours grid version")


class RegionGrid(Enum):
    """
    An enumerated collection of region grids defined in this module.
    """

    NZ_0_1_NB_1_0 = RegionGridEntry(region_name="NZ", resolution=0.1, neighbours=1, grid=NZ01nb1v0(), version=0)
    NZ_0_1_NB_1_1 = RegionGridEntry(region_name="NZ", resolution=0.1, neighbours=1, grid=NZ01nb1v1(), version=1)
    NZ_0_2_NB_1_1 = RegionGridEntry(region_name="NZ", resolution=0.2, neighbours=1, grid=NZ_0_2_nb_1_1(), version=1)

    WLG_0_01_nb_1_1 = RegionGridEntry(
        region_name="WLG",
        resolution=0.01,
        neighbours=1,
        grid=WLG_0_01_nb_1_1(),
        version=1,
    )
    WLG_0_05_nb_1_1 = RegionGridEntry(
        region_name="WLG",
        resolution=0.05,
        neighbours=1,
        grid=WLG_0_05_nb_1_1(),
        version=1,
    )

    def __init__(self, region_name, resolution, neighbours, grid, version):
        self.region_name = region_name
        self.resolution = resolution
        self.neighbours = neighbours
        self.grid = grid

    def load(self):
        return self.grid.load()


def load_grid(grid_name: str) -> List[LatLon]:
    """
    Load values from a region grid as `LatLon` pairs.

    Examples:
        >>> from nzshm_common import grids
        >>> grids.load_grid("NZ_0_1_NB_1_0")
        [
            LatLon(latitude=-46.1, longitude=166.4),
            LatLon(latitude=-46.0, longitude=166.4),
            LatLon(latitude=-45.9, longitude=166.4),
            ...
        ]
    """
    return RegionGrid[grid_name].load()


def get_location_grid(location_grid_name: str, resolution: Optional[float] = None) -> Iterable[CodedLocation]:
    """
    Get all coded locations within a grid.

    Note:
        When downsampling to a lower resolution, duplicate location values will be removed.

    Parameters:
        location_grid_name: A valid member key from RegionGrid (e.g. "NZ_0_1_NB_1_1")
        resolution: The resolution of the CodedLocation values generated.
            Defaults to the native RegionGrid resolution value.

    Returns:
        A list of coded locations with the specified resolution.

    Examples:
        >>> from nzshm_common import grids
        >>> grids.get_location_grid("NZ_0_1_NB_1_0")
        [
            CodedLocation(lat=-46.1, lon=166.4, resolution=0.1),
            CodedLocation(lat=-46.0, lon=166.4, resolution=0.1)
            ...
        ]
    """
    if not resolution:
        resolution = RegionGrid[location_grid_name].resolution
    elif resolution > RegionGrid[location_grid_name].resolution:
        warn_msg = "The requested resolution is lower than the grid resolution and will result in fewer points."
        warnings.warn(warn_msg, stacklevel=2)

    grid_values = load_grid(location_grid_name)
    coded_at_resolution = partial(CodedLocation.from_tuple, resolution=resolution)
    # Remove duplicate coordinates from collection, preserving order.
    location_list = []
    for loc in map(coded_at_resolution, grid_values):
        if loc not in location_list:
            location_list.append(loc)

    return location_list


def get_location_grid_names() -> Iterable[str]:
    """
    Return a collection of of valid region grids.

    Returns:
        member names from the RegionGrid Enum class.

    Examples:
        >>> from nzshm_common import grids
        >>> grids.get_location_grid_names()
        dict_keys([
            'NZ_0_1_NB_1_0',
            'NZ_0_1_NB_1_1',
            'NZ_0_2_NB_1_1',
            'WLG_0_01_nb_1_1',
            'WLG_0_05_nb_1_1'
        ])
    """

    return RegionGrid.__members__.keys()
