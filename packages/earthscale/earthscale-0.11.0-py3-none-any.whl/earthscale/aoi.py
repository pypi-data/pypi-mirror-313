from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

from pyproj import CRS
from shapely.geometry import MultiPolygon, Polygon

ROOT = Path(__file__).resolve().parent.parent / "demo"


class AOI:
    name: str
    geometry: Polygon | MultiPolygon
    # TODO: enable different projections
    crs: CRS = CRS.from_epsg(4326)

    _AOI_LOAD_CALLBBACK: ClassVar[Callable[[str], "AOI"] | None] = None

    def __init__(
        self,
        name: str,
        geometry: Polygon | MultiPolygon,
    ):
        self.name = name
        self.geometry = geometry

    @classmethod
    def register_aoi_load_callback(cls, callback: Callable[[str], "AOI"]) -> None:
        cls._AOI_LOAD_CALLBBACK = callback

    @classmethod
    def load(
        cls,
        name: str,
    ) -> "AOI":
        if cls._AOI_LOAD_CALLBBACK is None:
            raise ValueError("No AOI load callback registered")
        return cls._AOI_LOAD_CALLBBACK(name)
