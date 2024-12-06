import re
import warnings
from contextlib import suppress
from typing import Any

import pystac
from loguru import logger

from earthscale.datasets.dataset import (
    DatasetBand,
    DatasetBandClass,
    DatasetMetadata,
    DatasetProvider,
    TemporalResolution,
)


def _parse_ee_wavelength_info(
    center_wavelength: float | None,
    full_width_half_max: float | None,
    gee_wavelength: str | None,
) -> tuple[float | None, float | None]:
    """
    Fills in missing center wavelength and FWHM from GEE wavelength field,
    if available and parseable.

    The GEE wavelength field contains strings, which can be formatted like (at least):

    - `2.360-2.430&mu;m`
    - `740.2nm (S2A) / 739.1nm (S2B)`
    - `925.4100nm, FWHM: 11.2754nm`
    - `10.40 - 12.50 &mu;m`
    - `620-670nm`
    - `858nm`
    - `2130nm/2105 - 2155nm`
    - `0.402 - 0.422&micro;m`
    - `0.846-0.885&micro;m`
    """

    if center_wavelength and full_width_half_max:
        return center_wavelength, full_width_half_max
    if not gee_wavelength or gee_wavelength.strip() == "":
        return center_wavelength, full_width_half_max

    factor_to_microns = _detect_wavelength_unit(gee_wavelength)

    if "/" in gee_wavelength:
        return _parse_wavelengths_with_slashes(
            center_wavelength,
            full_width_half_max,
            gee_wavelength,
            factor_to_microns,
        )

    return _parse_wavelengths_without_slashes(
        center_wavelength, full_width_half_max, gee_wavelength, factor_to_microns
    )


def _detect_wavelength_unit(gee_wavelength: str) -> float:
    is_nanometer = "nm" in gee_wavelength
    is_micrometer = (
        "µm" in gee_wavelength
        or "&mu;m" in gee_wavelength
        or "&micro;m" in gee_wavelength
    )
    if is_nanometer and is_micrometer:
        logger.warning(
            f"Cannot parse wavelength unit from {gee_wavelength}. Assuming microns."
        )
        return 1
    if is_micrometer:
        return 1
    if is_nanometer:
        return 1e-3
    logger.warning(
        f"Cannot parse wavelength unit from {gee_wavelength}. Assuming microns."
    )
    return 1


def _parse_wavelengths_without_slashes(
    center_wavelength: float | None,
    full_width_half_max: float | None,
    gee_wavelength: str,
    unit_conversion_factor: float,
) -> tuple[float | None, float | None]:
    # handle simple range "620-670nm"
    match = re.match(r"(\d+(?:\.\d+)?).*?-\s*(\d+(?:\.\d+)?).*?", gee_wavelength)
    if match:
        groups = match.groups()
        min_wavelength = float(groups[0]) * unit_conversion_factor
        max_wavelength = float(groups[1]) * unit_conversion_factor
        center_wavelength = (min_wavelength + max_wavelength) / 2
        full_width_half_max = max_wavelength - min_wavelength
        return center_wavelength, full_width_half_max
    # handle value with FWHM
    match = re.match(
        r"(\d+(?:\.\d+)?).*?,\s*FWHM:\s*(\d+(?:\.\d+)?).*?", gee_wavelength
    )
    if match:
        groups = match.groups()
        if center_wavelength is None:
            center_wavelength = float(groups[0]) * unit_conversion_factor
        if full_width_half_max is None:
            full_width_half_max = float(groups[1]) * unit_conversion_factor
        return center_wavelength, full_width_half_max
    # handle single value "858nm"
    match = re.match(r"(\d+(?:\.\d+)?).*?", gee_wavelength)
    if match:
        if center_wavelength:
            return center_wavelength, full_width_half_max
        center_wavelength = float(match.groups()[0]) * unit_conversion_factor
        return center_wavelength, full_width_half_max
    logger.warning(f"Cannot parse wavelength and FWHM from: {gee_wavelength}")
    return center_wavelength, full_width_half_max


def _parse_wavelengths_with_slashes(
    center_wavelength: float | None,
    full_width_half_max: float | None,
    gee_wavelength: str,
    factor_to_microns: float,
) -> tuple[float | None, float | None]:
    # handle "2130nm/2105 - 2155nm"
    match = re.match(
        r"(\d+(?:\.\d+)?)\w*/(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?).*?",
        gee_wavelength,
    )
    if match:
        groups = match.groups()
        center_wavelength = float(groups[0]) * factor_to_microns
        min_wavelength = float(groups[1]) * factor_to_microns
        max_wavelength = float(groups[2]) * factor_to_microns
        full_width_half_max = max_wavelength - min_wavelength
        return center_wavelength, full_width_half_max
    # handle "885nm/10nm"
    match = re.match(r"(\d+(?:\.\d+)?)\w*/(\d+(?:\.\d+)?)\w*", gee_wavelength)
    if match:
        groups = match.groups()
        center_wavelength = float(groups[0]) * factor_to_microns
        full_width_half_max = float(groups[1]) * factor_to_microns
        return center_wavelength, full_width_half_max
    # handle  945nm (S2A) / 943.2nm (S2B)
    match = re.match(
        r"(\d+(?:\.\d+)?)\w*\s*\((\w+)\)\s*/\s*(\d+(?:\.\d+)?)\w*\s*\((\w+)\)",
        gee_wavelength,
    )
    if match:
        groups = match.groups()
        center_a = float(groups[0]) * factor_to_microns
        sensor_name_a = groups[1]

        center_b = float(groups[2]) * factor_to_microns
        sensor_name_b = groups[3]

        logger.info(
            "Found multiple wavelengths for sensors {sensor_name_a}={"
            "center_a:.4f}µm and {sensor_name_b}={center_b:.4f}µm. Choosing"
            " first.",
            sensor_name_a=sensor_name_a,
            center_a=center_a,
            sensor_name_b=sensor_name_b,
            center_b=center_b,
        )
        center_wavelength = center_a
        return center_wavelength, full_width_half_max
    logger.warning(f"Cannot parse wavelength and FWHM from: {gee_wavelength}")
    return center_wavelength, full_width_half_max


def _parse_earthengine_temporal_resolution(
    ee_stac: dict[str, Any],
) -> TemporalResolution | None:
    gee_interval = ee_stac.get("gee:interval")
    if not gee_interval:
        return None
    try:
        interval_type = gee_interval["type"]
        if interval_type in ("cadence", "revisit_interval", "climatological_interval"):
            interval_value = float(gee_interval["interval"])
            interval_unit = gee_interval["unit"]
            return TemporalResolution(
                type=interval_type,
                value=interval_value,
                unit=interval_unit,
            )
        else:
            logger.warning(f"Cannot parse temporal resolution from {gee_interval}")
    except (ValueError, KeyError):
        pass
    logger.warning(f"Cannot parse temporal resolution from {gee_interval}")
    return None


def parse_earth_engine_stac_to_earthscale(ee_stac: dict[str, Any]) -> DatasetMetadata:
    with logger.contextualize(ee_id=ee_stac.get("id")):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ps = pystac.Collection.from_dict(ee_stac)
        thumbnail_url = next(
            (link.href for link in ps.links if link.rel == "preview"), None
        )
        temporal_resolution = _parse_earthengine_temporal_resolution(ps.extra_fields)

        bands = []
        ee_bands = ps.summaries.get_list("eo:bands")
        if ee_bands:
            bands = [_parse_earthengine_band(band, ps) for band in ee_bands]

        temporal_extent = None
        intervals = ps.extent.temporal.intervals
        if intervals and len(intervals[0]) == 2:
            start, end = intervals[0]
            temporal_extent = (start, end)

        providers = None
        ee_providers = ps.providers
        if ee_providers:
            providers = [
                DatasetProvider(
                    name=provider.name,
                    roles=provider.roles or [],
                    url=provider.url,
                )
                for provider in ee_providers
            ]
        gsd = None
        try:
            gsd_summary = ps.summaries.get_list("gsd")
            if gsd_summary:
                gsd = float(gsd_summary[0])
        except (KeyError, ValueError):
            pass

        return DatasetMetadata(
            description=ps.description,
            thumbnail_url=thumbnail_url,
            tags=ps.keywords or [],
            license=ps.license,
            terms_of_use=ps.extra_fields.get("gee:terms_of_use"),
            providers=providers,
            source_id=ps.id,
            bands=[b.name for b in bands],
            bands_meta=bands,
            ground_sample_distance=gsd,
            temporal_resolution=temporal_resolution,
            temporal_extent=temporal_extent,
            platform=ps.summaries.get_list("platform"),
            instrument=ps.summaries.get_list("instruments"),
            supports_custom_viz=False,
        )


def _parse_earthengine_band(band: dict[str, Any], ps: pystac.Collection) -> DatasetBand:
    band_name = band["name"]
    center_wavelength = band.get("center_wavelength")
    full_width_half_max = band.get("full_width_half_max")
    center_wavelength, full_width_half_max = _parse_ee_wavelength_info(
        center_wavelength,
        full_width_half_max,
        band.get("gee:wavelength"),
    )
    min_value = None
    max_value = None
    band_range = ps.summaries.get_range(band_name)
    if band_range:
        min_value = float(band_range.minimum)
        max_value = float(band_range.maximum)

    # noinspection PyUnusedLocal
    offset = None
    with suppress(KeyError, ValueError):
        offset = float(band["gee:offset"])
    # noinspection PyUnusedLocal
    scale = None
    with suppress(KeyError, ValueError):
        scale = float(band["gee:scale"])
    # noinspection PyUnusedLocal
    unit = None
    with suppress(KeyError, ValueError):
        unit = band["gee:units"]
    # noinspection PyUnusedLocal
    gsd = None
    with suppress(KeyError, ValueError):
        gsd = float(band["gsd"])
    # noinspection PyUnusedLocal
    classes: list[DatasetBandClass] | None = None
    with suppress(KeyError):
        ee_classes = band["gee:classes"]
        classes = _parse_earthengine_band_classes(ee_classes)

    dataset_band = DatasetBand(
        name=band_name,
        description=band.get("description"),
        common_name=band.get("common_name"),
        min_value=min_value,
        max_value=max_value,
        offset=offset,
        scale=scale,
        unit=unit,
        classes=classes,
        sensor_ground_sample_distance=gsd,
        center_wavelength=center_wavelength,
        full_width_half_max=full_width_half_max,
    )
    return dataset_band


def _parse_earthengine_band_classes(
    ee_classes: list[dict[str, Any]],
) -> list[DatasetBandClass]:
    classes: list[DatasetBandClass] = []
    for class_ in ee_classes:
        try:
            value = float(class_["value"])
        except (KeyError, ValueError):
            logger.warning(f"Cannot parse class value from {class_}")
            continue
        classes.append(
            DatasetBandClass(
                value=value,
                description=class_.get("description"),
                default_color=class_.get("color"),
            )
        )
    return classes
