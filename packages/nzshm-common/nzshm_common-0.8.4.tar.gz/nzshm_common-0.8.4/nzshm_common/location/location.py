"""
This module contains constants and functions for referring to location or list of locations by an identifier.
"""

import csv
import importlib.resources as resources
import json
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from nzshm_common.constants import DEFAULT_RESOLUTION
from nzshm_common.grids.region_grid import load_grid
from nzshm_common.location.coded_location import CodedLocation
from nzshm_common.location.types import LatLon

# Omitting country for now, focus on NZ
# https://service.unece.org/trade/locode/nz.htm

resource_dir = resources.files('nzshm_common.location.resources')

with resources.as_file(resource_dir / 'locations.json') as path:
    with path.open() as file:
        LOCATIONS = json.load(file)

with resources.as_file(resource_dir / 'nz_ids.json') as path:
    with path.open() as file:
        NZ_IDS = json.load(file)

LOCATIONS_BY_ID: Dict[str, Any] = {location["id"]: location for location in LOCATIONS}


LOCATION_LISTS = {
    "HB": {
        "id": "HB",
        "name": "Hawk's Bay high res grid with vs30",
        "locations": [loc["id"] for loc in LOCATIONS if "hb_" in loc["id"]],
    },
    "NZ": {"id": "NZ", "name": "Default NZ locations", "locations": NZ_IDS},
    "NZ2": {
        "id": "NZ2",
        "name": "Main Cities NZ",
        "locations": ["WLG", "CHC", "DUD", "NPL", "AKL", "ROT", "HLZ"],
    },
    "SRWG214": {
        "id": "SRWG214",
        "name": "Seismic Risk Working Group NZ code locations",
        # "locations": list(map(lambda idn: f"srg_{idn}", range(214))),
        "locations": [loc["id"] for loc in LOCATIONS if "srg_" in loc["id"]],
    },
    "ALL": {
        "id": "ALL",
        "name": "All locations",
        "locations": list(map(lambda loc: loc["id"], LOCATIONS)),
    },
}


def _get_macron_word_mapping() -> Dict[str, str]:
    """using the maori_names.csv file as received from LINZ rather than storing the mapping allows
    us to update without rebuilding the resource"""

    char_map_lower = {
        'ā': 'a',
        'ē': 'e',
        'ī': 'i',
        'ō': 'o',
        'ū': 'u',
    }
    char_map = {}
    for k, v in char_map_lower.items():
        char_map[k] = v
        char_map[k.upper()] = v.upper()
    translation_table = str.maketrans(char_map)

    word_mapping = dict()
    with resources.as_file(resource_dir / 'maori_names.csv') as path:
        with path.open(encoding='utf-8') as file:
            reader = csv.reader(file)
            _ = next(reader)
            for row in reader:
                name = row[1]  # second column of LINZ file contains names
                for word in name.split():  # treat each whole word seperatly
                    if any([char in char_map for char in word]):  # add to mapping if any characters have macron
                        word_nomacron = word.translate(translation_table)
                        word_mapping[word_nomacron] = word
    return word_mapping


WORD_MAPPING = _get_macron_word_mapping()


def get_name_with_macrons(name_input: str) -> str:
    """
    Corrects the spelling of Māori palce names by adding macrons. Place name spellings from
    LINZ "Place names of New Zealand".
    See https://www.linz.govt.nz/products-services/place-names/place-names-new-zealand
    and https://gazetteer.linz.govt.nz/maori_names.csv

    If the input name is not on the LINZ list, the function will return the input.

    Args:
        input_name: the name to correct with macrons

    Returns:
        the place name with the correct Māori spelling
    """

    words_in = name_input.split()
    return " ".join([_map_word(word) for word in words_in])


def _map_word(word_input):
    if word_output := WORD_MAPPING.get(word_input):
        return word_output
    return word_input


def _lat_lon(_id) -> Optional[LatLon]:
    loc = location_by_id(_id)
    if loc:
        return LatLon(loc['latitude'], loc['longitude'])
    return None


def _load_csv(locations_filepath, resolution):
    locs = []
    with locations_filepath.open('r') as locations_file:
        reader = csv.reader(locations_file)
        Location = namedtuple("Location", next(reader), rename=True)
        for row in reader:
            location = Location(*row)
            locs.append(CodedLocation(lat=float(location.lat), lon=float(location.lon), resolution=resolution))
    return locs


def location_by_id(location_code: str) -> Optional[Dict[str, Any]]:
    """
    Get the information for a location identified by an id.

    Parameters:
        location_code: the code (e.g. "WLG") for the location

    Returns:
        coded location of location_code

    Examples:
        >>> location_by_id("WLG")
        {'id': 'WLG', 'name': 'Wellington', 'latitude': -41.3, 'longitude': 174.78}
    """
    return LOCATIONS_BY_ID.get(location_code)


def get_locations(locations: Iterable[str], resolution: float = DEFAULT_RESOLUTION) -> List[CodedLocation]:
    """
    Get the coded locations from a list of identifiers.

    Identifiers can be any combination of:
        - a location string (latitude~longitude)
        - location list (key in nzhsm_common.location.location.LOCATION_LISTS)
        - location code (e.g. "WLG")
        - grid name in nzshm_common.grids.region_grid.RegionGrid
        - csv file with at least a column headed "lat" and a column headed "lon" (any other columns will be ignored)

    Parameters:
        locations: a list of location identifiers
        resolution: the resolution used by CodedLocation

    Returns:
        coded_locations: a list of coded locations
    """
    coded_locations: List[CodedLocation] = []
    for loc_id in locations:
        location_id = str(loc_id)
        if Path(location_id).exists():
            coded_locations += _load_csv(Path(location_id), resolution)
        elif '~' in location_id:
            lat, lon = location_id.split('~')
            coded_locations.append(CodedLocation(float(lat), float(lon), resolution))
        elif location_by_id(location_id):
            coded_locations.append(CodedLocation(*_lat_lon(location_id), resolution))  # type: ignore
        elif LOCATION_LISTS.get(location_id):
            location_ids = LOCATION_LISTS[location_id]["locations"]
            coded_locations += [CodedLocation(*_lat_lon(_id), resolution) for _id in location_ids]  # type: ignore
        else:
            try:
                coded_locations += [CodedLocation(*loc, resolution) for loc in load_grid(location_id)]  # type: ignore
            except KeyError:
                msg = "location {} is not a valid location identifier".format(location_id)
                raise KeyError(msg)

    return coded_locations


def get_location_list_names() -> List[str]:
    """
    Return a list of valid location lists.

    Examples:
        >>> from nzshm_common import location
        >>> location.get_location_list_names()
        ['HB', 'NZ', 'NZ2', 'SRWG214', 'ALL']
    """
    return list(LOCATION_LISTS.keys())


def get_location_list(
    location_list_names: List[str], resolution: float = DEFAULT_RESOLUTION, sort_locations: bool = True
) -> Iterable[CodedLocation]:
    """
    Get all coded locations within one or more lists.

    The sorting method used for CodedLocation values is described in
    [`CodedLocation.__lt__`](coded_location.md#nzshm_common.location.coded_location.CodedLocation.__lt__)

    Parameters:
        location_list_names: a list of valid LOCATION_LIST keys
        resolution: the resolution used by CodedLocation
        sort_locations: (optional) whether to sort the CodedLocation values

    Returns:
        a list of coded locations

    Examples:
        >>> from nzshm_common import location
        >>> location.get_location_list(["NZ", "SRWG214"])
        [
            CodedLocation(lat=-35.109, lon=173.262, resolution=0.001),
            CodedLocation(lat=-35.22, lon=173.97, resolution=0.001),
            ...
        ]
    """
    # Merge location lists, ensuring unique keys.
    location_keyset = set([loc for name in location_list_names for loc in LOCATION_LISTS[name]["locations"]])
    coded_locations = [
        CodedLocation(
            lat=LOCATIONS_BY_ID[loc]["latitude"],
            lon=LOCATIONS_BY_ID[loc]["longitude"],
            resolution=resolution,
        )
        for loc in location_keyset
    ]
    if sort_locations:
        return sorted(coded_locations)
    else:
        return coded_locations


if __name__ == "__main__":
    """Print all locations."""
    print("custom_site_id,lon,lat")
    for loc in LOCATIONS:
        print(f"{loc['id']},{loc['longitude']},{loc['latitude']}")
