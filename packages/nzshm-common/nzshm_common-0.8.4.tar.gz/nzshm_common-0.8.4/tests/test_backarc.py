import unittest

try:
    import shapely  # noqa
    from shapely.geometry import Point

    from nzshm_common.geometry.geometry import backarc_polygon

    HAVE_SHAPELY = True
except ImportError:
    HAVE_SHAPELY = False

LOCATIONS_W_BACKARC = [
    ("AKL", 174.77, -36.87, 1),
    ("BHE", 173.95, -41.51, 0),
    ("CHC", 172.63, -43.53, 0),
    ("DUD", 170.5, -45.87, 0),
    ("GIS", 178.0, -38.65, 0),
    ("GMN", 171.21, -42.45, 0),
    ("HAW", 174.28, -39.59, 1),
    ("HLZ", 175.28, -37.78, 1),
    ("IVC", 168.36, -46.43, 0),
    ("KBZ", 173.68, -42.4, 0),
    ("KKE", 173.97, -35.22, 1),
    ("LVN", 175.28, -40.63, 0),
    ("MON", 170.1, -43.73, 0),
    ("MRO", 175.66, -40.96, 0),
    ("NPE", 176.92, -39.48, 0),
    ("NPL", 174.08, -39.07, 1),
    ("NSN", 173.28, -41.27, 0),
    ("PMR", 175.62, -40.35, 0),
    ("TEU", 167.72, -45.41, 0),
    ("TIU", 171.26, -44.4, 0),
    ("TKZ", 175.87, -38.23, 1),
    ("TMZ", 175.53, -37.13, 1),
    ("TRG", 176.17, -37.69, 1),
    ("TUO", 176.08, -38.68, 1),
    ("ROT", 176.25, -38.14, 1),
    ("WHK", 177.0, -37.98, 0),
    ("WHO", 170.17, -43.35, 0),
    ("WLG", 174.78, -41.3, 0),
    ("WSZ", 171.58, -41.75, 0),
    ("ZWG", 175.05, -39.93, 0),
    ("ZTR", 175.93, -39.0, 0),
    ("ZOT", 171.54, -42.78, 0),
    ("ZHT", 169.06, -43.88, 0),
    ("ZHS", 172.78, -42.54, 0),
    ("ZQN", 168.69, -45.02, 0),
]

LOCATIONS_W_BACKARC_BY_ID = {
    loc[0]: {"id": loc[0], "latitude": loc[2], "longitude": loc[1], "backarc": loc[3]} for loc in LOCATIONS_W_BACKARC
}


@unittest.skipUnless(HAVE_SHAPELY, "Test requires optional shapely module.")
def test_backarc_polygon():

    for location in LOCATIONS_W_BACKARC_BY_ID.values():
        print(backarc_polygon().contains(Point(location['longitude'], location['latitude'])), location['backarc'])
        assert backarc_polygon().contains(Point(location['longitude'], location['latitude'])) == location['backarc']
