import math
from datetime import datetime, timezone

import geopandas as gpd
import numpy as np
import xarray as xr
from dateutil import parser
from morecantile import Tile, TileMatrixSet  # type: ignore
from shapely.geometry import box

_MAX_ZOOM = 14


def iso_to_timestamp(iso: str) -> int:
    return int(parser.parse(iso).timestamp())


def timestamp_to_iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def _compute_decompressed_tile_size_mib(
    x: int,
    y: int,
    z: int,
    data: xr.Dataset,
    tms: TileMatrixSet,
) -> int:
    num_data_vars = len(data.data_vars)

    # Assume 32-bit floats for now
    bytes_per_pixel = 4 * num_data_vars

    # Get max chunk sizes
    max_chunk_sizes = {}
    for k, chunk_sizes in data.chunks.items():
        max_chunk_sizes[k] = max(chunk_sizes)

    total_chunk_size_pixels = np.prod(list(max_chunk_sizes.values()))

    # Get tile size in pixels for the given zoom level and resolution
    tms_tile_bounds = tms.xy_bounds(Tile(x=x, y=y, z=z))
    # Convert from TMS CRS to dataset CRS
    bbox = box(
        tms_tile_bounds.left,
        tms_tile_bounds.bottom,
        tms_tile_bounds.right,
        tms_tile_bounds.top,
    )
    tile_bounds = (
        gpd.GeoDataFrame(geometry=[bbox], crs=tms.crs).to_crs(data.rio.crs).total_bounds
    )

    dset_resolution = data.rio.resolution()
    tile_width_pixels = int((tile_bounds[2] - tile_bounds[0]) / dset_resolution[0])
    tile_height_pixels = int((tile_bounds[3] - tile_bounds[1]) / -dset_resolution[1])

    if tile_width_pixels == 0 or tile_height_pixels == 0:
        return 0

    # Get max number of chunks intersecting with the tile
    max_x_chunks_read = math.ceil(tile_width_pixels / max_chunk_sizes["x"]) + 1
    max_y_chunks_read = math.ceil(tile_height_pixels / max_chunk_sizes["y"]) + 1
    max_chunks_read = max_x_chunks_read * max_y_chunks_read

    total_read_size_bytes = total_chunk_size_pixels * bytes_per_pixel * max_chunks_read
    total_read_size_mib = math.ceil(total_read_size_bytes / 1024 / 1024)

    return total_read_size_mib


def _get_sample_tile_for_zoom(
    dset: xr.Dataset,
    z: int,
    tms: TileMatrixSet,
) -> Tile:
    bounds = dset.rio.bounds()

    # Making sure that the bounds are within WGS84 CRS (-180, -90, 180, 90)
    if dset.rio.crs.is_geographic:
        bounds = (
            max(bounds[0], -180),
            max(bounds[1], -90),
            min(bounds[2], 180),
            min(bounds[3], 90),
        )

    # Convert from dset CRS to TMS CRS
    centroid = (
        gpd.GeoDataFrame(geometry=[box(*bounds)], crs=dset.rio.crs)
        .to_crs("EPSG:3857")
        .centroid.to_crs(tms.geographic_crs)
        .values[0]
    )
    tile = tms.tile(lng=centroid.x, lat=centroid.y, zoom=z)
    return tile


def get_min_tile_zoom_for_viz(
    dset: xr.Dataset,
    tms: TileMatrixSet,
    max_tile_size_mib: int,
) -> int:
    # For now, just take up to 3 bands (RGB)
    # This is independent of the visualization parameters
    all_bands = list(dset.data_vars.keys())
    viz_bands = all_bands[:3]
    viz_dset = dset[viz_bands]

    current_min_tile_zoom = _MAX_ZOOM

    while current_min_tile_zoom > 0:
        tile = _get_sample_tile_for_zoom(
            dset=viz_dset,
            z=current_min_tile_zoom,
            tms=tms,
        )

        tile_size_mb = _compute_decompressed_tile_size_mib(
            x=tile.x,
            y=tile.y,
            z=tile.z,
            data=viz_dset,
            tms=tms,
        )

        if tile_size_mb > max_tile_size_mib:
            break

        current_min_tile_zoom -= 1

    return current_min_tile_zoom + 1
