from pyproj import CRS

# Converted from:
#   https://github.com/OSGeo/spatialreference.org/blob/master/scripts/sr-org.json
# We do not have all the SR-ORG definitions here, because their database is massive and
# contains lots of garbage. We only include the ones we need.
_SR_ORG_CRS: dict[int, CRS] = {
    6974: CRS.from_wkt(
        'PROJCS["MODIS Sinusoidal",'
        'GEOGCS["WGS 84",'
        '   DATUM["WGS_1984",'
        '       SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],'
        '       AUTHORITY["EPSG","6326"]],'
        '   PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],'
        '   UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],'
        '   AUTHORITY["EPSG","4326"]],'
        'PROJECTION["Sinusoidal"],'
        'PARAMETER["false_easting",0.0],'
        'PARAMETER["false_northing",0.0],'
        'PARAMETER["central_meridian",0.0],'
        'PARAMETER["semi_major",6371007.181],'
        'PARAMETER["semi_minor",6371007.181],'
        'UNIT["m",1.0],'
        'AUTHORITY["SR-ORG","6974"]]'
    )
}


def crs_from_str(crs_str: str) -> CRS:
    """
    Use this for Earth Engine CRS strings, since they have custom CRS definitions.
    """
    first_colon = crs_str.find(":")
    if first_colon == -1:
        return CRS.from_string(crs_str)
    authority = crs_str[:first_colon].lower()
    if authority == "epsg":
        return CRS.from_string(crs_str)
    if authority == "sr-org":
        code = int(crs_str[first_colon + 1 :])
        return _SR_ORG_CRS[code]
    return CRS.from_string(crs_str)
