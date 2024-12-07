"""
This package provides classes and functions to handle geographical locations. There are a number of
pre-set locations of interest to the NZ NSHM made availabe in this package. They can be accessed via
the "location lists." See examples below.

Classes:
 CodedLocation: a location defined by a latitude, longitude pair at a given resolution
 CodedLocationBin: a collection of CodedLocations bined at a given resolution (genrally lower than
 the resolution of the CodedLocations themselves)

Functions:
 get_location_list_names: get the names of the "location lists" which are lists of pre-set locations
 get_location_list: get all locations from one or more location lists as CodedLocations
 commonly used in the analysis of the NZ NSHM.
 get_locations: convert a variety of location identifiers into an iterable of CodedLocations
 location_by_id: get information about a particular location in any of the "location lists"

Example:
    ```py
    >>> all_locations = get_location_list(get_location_list_names())
    >>> nz_cities = get_location_list(["NZ"])
    >>> wellington = location_by_id("WLG")
    >>> locs = get_locations(["WLG", "CHC"])
    ```
"""

from .coded_location import CodedLocation, CodedLocationBin
from .location import get_location_list, get_location_list_names, get_locations, get_name_with_macrons, location_by_id
