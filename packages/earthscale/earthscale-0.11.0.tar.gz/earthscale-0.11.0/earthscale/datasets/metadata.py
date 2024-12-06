import random
from collections.abc import Hashable, Mapping
from typing import Any

import numpy as np
import xarray as xr
from loguru import logger
from rasterio import RasterioIOError
from rio_tiler.constants import WEB_MERCATOR_TMS

from earthscale.constants import (
    MAX_NUM_BANDS_FOR_MIN_MAX_ESTIMATION,
    NUM_CHUNKS_FOR_MIN_MAX_ESTIMATION,
)
from earthscale.datasets.raster import RasterDataset
from earthscale.exceptions import (
    convert_rasterio_to_earthscale,
)
from earthscale.repositories.utils import get_min_tile_zoom_for_viz

_TMS = WEB_MERCATOR_TMS
_MAX_TILE_SIZE_MIB = 4096


def _chunks_to_slices(
    chunks: Mapping[Hashable, tuple[int, ...]],
) -> dict[Hashable, list[slice]]:
    slices_per_dim: dict[Hashable, list[slice]] = {dim: [] for dim in chunks}
    for dim, chunk_sizes in chunks.items():
        cum_sizes = np.cumsum(chunk_sizes)
        if len(cum_sizes) == 1:
            slices = [slice(None)]
        else:
            slices = [slice(0, cum_sizes[0])]
            slices.extend(
                [
                    slice(cum_sizes[i], cum_sizes[i + 1])
                    for i in range(len(cum_sizes) - 1)
                ]
            )
        slices_per_dim[dim] = slices
    return slices_per_dim


def _approx_min_max_values(
    dset: xr.Dataset, bands: list[str], n_chunks: int = 10
) -> dict[str, tuple[float, float]]:
    slices_per_dim = _chunks_to_slices(dset.chunks)

    # take random combinations of slices per dimension
    rand_slices_per_dim: dict[Hashable, list[slice]] = {}
    for dim, slices in slices_per_dim.items():
        rand_slices_per_dim[dim] = random.choices(slices, k=n_chunks)
    # turn into {k: slice}
    rand_slices: list[dict[Hashable, slice]] = [
        dict(zip(rand_slices_per_dim, t, strict=False))
        for t in zip(*rand_slices_per_dim.values(), strict=False)
    ]

    for var in dset.data_vars:
        nodata_value = dset[var].rio.nodata
        if nodata_value is not None:
            dset[var] = dset[var].where(dset[var] != nodata_value)

    running_min: dict[str, float] = {band: float("inf") for band in bands}
    running_max: dict[str, float] = {band: float("-inf") for band in bands}
    for chunk_slices in rand_slices:
        chunk_data = dset.isel(**chunk_slices)[bands]  # type: ignore
        try:
            chunk_min = chunk_data.min(skipna=True).compute()
            chunk_max = chunk_data.max(skipna=True).compute()
        except RasterioIOError as e:
            raise convert_rasterio_to_earthscale(e) from e

        for band in bands:
            running_min[band] = min(running_min[band], float(chunk_min[band]))
            running_max[band] = max(running_max[band], float(chunk_max[band]))
    running_min_max: dict[str, tuple[float, float]] = {
        band: (running_min[band], running_max[band]) for band in bands
    }
    return running_min_max


def _true_min_max_values(
    dset: xr.Dataset, bands: list[str]
) -> dict[str, tuple[float, float]]:
    min_values: xr.Dataset = dset[bands].min().compute()
    max_values: xr.Dataset = dset[bands].max().compute()
    min_maxes_per_band: dict[str, tuple[float, float]] = {}
    for band in bands:
        min_maxes_per_band[band] = (float(min_values[band]), float(max_values[band]))
    return min_maxes_per_band


def get_min_max_values(
    dset: xr.Dataset, bands: list[str], n_chunks: int = 10
) -> dict[str, tuple[float | None, float | None]]:
    min_maxes_per_band: dict[str, tuple[float, float]] = {}
    if n_chunks > 0:
        min_maxes_per_band = _approx_min_max_values(dset, bands, n_chunks)
    else:
        min_maxes_per_band = _true_min_max_values(dset, bands)

    # Post-process to ensure that the min and max values are None if they are NaN/inf
    postprocessed_min_maxes_per_band: dict[str, tuple[float | None, float | None]] = {}
    for band in bands:
        min_val, max_val = min_maxes_per_band[band]
        has_inf = np.isinf(min_val) or np.isinf(max_val)
        has_nan = np.isnan(min_val) or np.isnan(max_val)
        if has_inf or has_nan:
            postprocessed_min_maxes_per_band[band] = (None, None)
        else:
            postprocessed_min_maxes_per_band[band] = (min_val, max_val)

    return postprocessed_min_maxes_per_band


def add_raster_viz_metadata(
    dataset: RasterDataset[Any],
) -> None:
    # TODO(remove_to_xarray): We can probably get the bands based on the items and the
    #                         grouping to avoid the `.to_xarray()` call
    dset = dataset.to_xarray()
    available_bands = list(dset.data_vars)
    dataset.metadata.bands = available_bands
    # We don't need min zoom when we've got an external tileserver
    dataset.metadata.min_zoom = get_min_tile_zoom_for_viz(
        dset=dset,
        tms=_TMS,
        max_tile_size_mib=_MAX_TILE_SIZE_MIB,
    )

    # Check if any min/max values are missing from the metadata.
    min_maxes_per_band = dataset.metadata.min_maxes_per_band or {}
    bands_with_no_min_max = [
        band for band in available_bands if band not in min_maxes_per_band
    ]

    if len(bands_with_no_min_max) > MAX_NUM_BANDS_FOR_MIN_MAX_ESTIMATION:
        logger.warning(
            f"This dataset has {len(available_bands)} bands with no min/max values, "
            f"which is more than the max of {MAX_NUM_BANDS_FOR_MIN_MAX_ESTIMATION} "
            "for min/max estimation. Skipping min/max estimation."
        )
        # Add default min/max values to the metadata
        defaults = {band: (0, 1) for band in bands_with_no_min_max}
        dataset.metadata.min_maxes_per_band = min_maxes_per_band | defaults
    elif len(bands_with_no_min_max) > 0:
        logger.debug(f"Estimating min/max values for bands: {bands_with_no_min_max}")
        new_min_maxes = get_min_max_values(
            dset,
            bands_with_no_min_max,
            NUM_CHUNKS_FOR_MIN_MAX_ESTIMATION,
        )
        dataset.metadata.min_maxes_per_band = min_maxes_per_band | new_min_maxes
    return
