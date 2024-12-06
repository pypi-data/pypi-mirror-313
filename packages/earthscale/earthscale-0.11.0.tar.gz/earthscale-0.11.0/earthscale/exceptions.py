from rasterio import RasterioIOError


class EarthscaleError(Exception):
    """Base class for exceptions in this module."""

    pass


class RasterFileNotFoundError(EarthscaleError):
    """Raised when a file is not found"""

    pass


class RasterAccessDeniedError(EarthscaleError):
    """Raised when the user does not have access to the dataset,
    or if the dataset is not found"""

    pass


class UnsupportedRasterFormatError(EarthscaleError):
    """Raised when the user tries to open a raster file that is not supported"""

    pass


def convert_rasterio_to_earthscale(
    e: RasterioIOError,
) -> RasterioIOError | EarthscaleError:
    """Handle rasterio IO errors."""
    if "No such file or directory" in e.args[0]:
        return RasterFileNotFoundError(e.args[0])
    if "Access Denied" in e.args[0]:
        return RasterAccessDeniedError(
            f"{e.args[0]} This could be due to insufficient permissions, "
            "the file not existing, or the file not being readable by rasterio. "
            "Please check that the file exists and you have the necessary "
            "access rights."
        )
    return e
