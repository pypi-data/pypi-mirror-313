import abc
import datetime
import enum
import uuid
from collections.abc import Callable
from copy import deepcopy
from dataclasses import field
from enum import Enum
from typing import Any, ClassVar, Generic, Literal, Protocol, TypeVar

from pydantic import BaseModel


class DatasetDefinition(BaseModel):
    """Holds all additional values required to reconstruct the dataset"""


class DatasetBandClass(BaseModel):
    value: float
    description: str | None = None
    default_color: str | None = None
    """
    A hex color string, e.g. FF0000, that is used by default to represent this class
    """


class DatasetAttribute(BaseModel):
    name: str
    value: str


class DatasetBand(BaseModel):
    name: str
    description: str | None = None
    unit: str | None = None
    min_value: float | None = None
    max_value: float | None = None
    offset: float | None = None
    scale: float | None = None
    center_wavelength: float | None = None
    """
    Center wavelength of the band, in micrometers.
    """
    full_width_half_max: float | None = None
    """
    Full width of the band at half maximum transmission, in micrometers.
    """
    sensor_ground_sample_distance: float | None = None
    """
    Ground sample distance of the sensor, in meters.

    This is not the pixel size. The actual pixel size depends on geometry,
    wavelength and processing steps.

    See https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#gsd
    """
    common_name: str | None = None
    """
    Common name of the band, e.g. "red", "nir"

    See https://github.com/stac-extensions/eo?tab=readme-ov-file#common-band-names
    """
    classes: list[DatasetBandClass] | None = None
    """
    For categorical bands, mapping of values to semantic classes
    """


DatasetProviderRole = Literal["licensor", "producer", "processor", "host"]


class DatasetProvider(BaseModel):
    name: str
    url: str
    roles: list[DatasetProviderRole]


class TemporalResolution(BaseModel):
    value: float
    """
    The number of units in the interval
    """

    type: Literal["cadence", "revisit_interval", "climatological_interval"]
    """
    How the interval should be interpreted. Depends on the data source. For example,
    "cadence" means that the interval is the time between two consecutive data points
    in a time series. "revisit_interval" means that the interval is the time between
    two consecutive observations of the same location (not necessarily reflected in the
    time series). "climatological_interval" means that the interval is the time over
    which the data is aggregated to create a statistical summary.
    """

    unit: Literal["second", "minute", "hour", "day", "week", "month", "year"]
    """
    The time unit of the interval
    """


class DatasetMetadata(BaseModel):
    # <editor-fold desc="TODO: remove these fields after migration">
    # TODO: can't do dict[str, int] | dict[str, list[int]]?
    # throws mypy error when instantiated
    value_map: dict[str, int] | dict[str, list[int]] = field(default_factory=dict)
    bands: list[str] = field(default_factory=list)
    min_maxes_per_band: dict[str, tuple[float | None, float | None]] | None = None
    # </editor-fold>

    attributes: list[DatasetAttribute] = field(default_factory=list)
    """
    Arbitrary user-supplied attributes of the dataset
    """

    bands_meta: list[DatasetBand] = field(default_factory=list)

    min_zoom: int | None = None
    """
    TODO: maybe move this to DatasetVersion?
    """

    max_zoom: int | None = None
    """
    TODO: maybe move this to DatasetVersion?
    """

    # For some datasets/sources it is beneficial to use an external tileserver instead
    # of ours (e.g. for a TileServerDataset)
    tileserver_url: str | None = None
    """
    TODO: maybe move this to DatasetVersion?
    """
    # Whether the dataset supports custom visualizations. If this is set to True, e.g.
    # a default visualization will be created for the dataset
    supports_custom_viz: bool = True
    """
    TODO: maybe move this to DatasetVersion?
    """

    description: str | None = None

    crs: str | None = None

    thumbnail_url: str | None = None
    """
    If available, publically accessible URL to a thumbnail image
    """

    tags: list[str] = field(default_factory=list)

    license: str | None = None
    """
    License as a short unique key, e.g. "CC-BY-SA-4.0"
    """

    terms_of_use: str | None = None
    """
    More detailed terms of use, e.g. a URL to a page with the full license text
    or just an explanation of the license
    """

    providers: list[DatasetProvider] = field(default_factory=list)
    """
    Source of the dataset, e.g. the organization that produced the data,
    the organization that hosts the data, etc.
    """

    temporal_extent: tuple[datetime.datetime, datetime.datetime] | None = None
    """
    Temporal extent of the dataset.

    This is the start and end time of data contained in this dataset.
    If there is no time axis, this is the source time of the pixels in the dataset.

    If the dataset is a time series, this is the start and end time of the time series.
    """

    ground_sample_distance: float | None = None
    """
    Ground sample distance of the dataset, in meters.

    This is not the pixel size. The actual pixel size depends on geometry,
    wavelength and processing steps.
    """

    temporal_resolution: TemporalResolution | None = None
    """
    Temporal resolution of the dataset, if it is a time series.

    This is provided for information only, check the labels of the time series for
    the actual time resolution. For example, there might be missing data points.
    """

    platform: list[str] | None = None
    """
    Platform(s) used to collect the data, e.g. "Sentinel-2A"
    """

    instrument: list[str] | None = None
    """
    Instrument(s) used to collect the data, e.g. "MSI"
    """

    source_id: str | None = None
    """
    If set, this identifies the dataset in the source system (e.g. Earth Engine)
    """


class DatasetDomain(str, Enum):
    """Defines which type of catalog a dataset belongs to."""

    WORKSPACE = "WORKSPACE"
    CATALOG = "CATALOG"


class DatasetType(enum.Enum):
    RASTER = "raster"
    VECTOR = "vector"


class DatasetStatus(enum.Enum):
    NOT_STARTED = "not_started"
    PROCESSING = "processing"
    PROCESSING_FAILED = "processing_failed"
    READY = "ready"


DefinitionType = TypeVar("DefinitionType", bound=DatasetDefinition)

DatasetCreationCallback = Callable[["Dataset[Any]"], None]


class DatasetLoadCallback(Protocol):
    def __call__(
        self,
        dataset_id: uuid.UUID | None,
        dataset_version_id: uuid.UUID | None,
        name: str | None,
    ) -> "Dataset[Any]": ...


class Dataset(abc.ABC, Generic[DefinitionType]):
    # List of functions to call when a dataset is created. This is useful in the case
    # of the SDK which can auto-register a callback when running in a notebook
    _DATASET_CREATION_CALLBACKS: ClassVar[list[DatasetCreationCallback]] = []
    _DATASET_LOAD_CALLBACK: ClassVar[DatasetLoadCallback | None] = None

    @classmethod
    def register_dataset_creation_callback(
        cls, callback: DatasetCreationCallback
    ) -> None:
        cls._DATASET_CREATION_CALLBACKS.append(callback)

    @classmethod
    def register_dataset_load_callback(cls, callback: DatasetLoadCallback) -> None:
        """
        Register a callback to load by either dataset_id, dataset_version_id or name.
        Only one of the three will be set.
        """
        cls._DATASET_LOAD_CALLBACK = callback

    def __init__(
        self,
        name: str,
        explicit_name: bool,
        attributes: dict[str, str] | None,
        metadata: DatasetMetadata,
        type_: DatasetType,
        status: DatasetStatus,
        definition: DefinitionType,
        dataset_id: uuid.UUID | None,
        dataset_version_id: uuid.UUID | None,
    ):
        self.name = name
        self.metadata = metadata
        if attributes is not None:
            self.metadata.attributes = [
                DatasetAttribute(name=name, value=value)
                for name, value in attributes.items()
            ]
        self.type = type_
        self.status = status
        self._explicit_name = explicit_name
        self.definition = definition
        self.dataset_id = dataset_id
        self.dataset_version_id = dataset_version_id

        if explicit_name:
            # Used for e.g. registering in the Notebook case
            for callback in self._DATASET_CREATION_CALLBACKS:
                callback(self)

    @classmethod
    def load(cls, dataset_id: uuid.UUID) -> "Dataset[DefinitionType]":
        if cls._DATASET_LOAD_CALLBACK is None:
            raise ValueError("No dataset load callback registered")
        return cls._DATASET_LOAD_CALLBACK(
            dataset_id=dataset_id,
            dataset_version_id=None,
            name=None,
        )

    @classmethod
    def load_version(cls, dataset_version_id: uuid.UUID) -> "Dataset[DefinitionType]":
        if cls._DATASET_LOAD_CALLBACK is None:
            raise ValueError("No dataset load callback registered")
        return cls._DATASET_LOAD_CALLBACK(
            dataset_id=None,
            dataset_version_id=dataset_version_id,
            name=None,
        )

    @classmethod
    def load_by_name(cls, name: str) -> "Dataset[DefinitionType]":
        if cls._DATASET_LOAD_CALLBACK is None:
            raise ValueError("No dataset load callback registered")
        return cls._DATASET_LOAD_CALLBACK(
            dataset_id=None,
            dataset_version_id=None,
            name=name,
        )

    @classmethod
    def from_serialized_definition(
        cls,
        dataset_id: uuid.UUID | None,
        dataset_version_id: uuid.UUID | None,
        name: str,
        metadata: DatasetMetadata,
        definition: dict[str, Any],
    ) -> "Dataset[DefinitionType]":
        definition = deepcopy(definition)
        kw_args = definition.pop("kw_args", {})
        attributes = {attr.name: attr.value for attr in metadata.attributes}

        return cls(
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
            name=name,
            metadata=metadata,
            attributes=attributes,
            **definition,
            **kw_args,
        )

    @property
    def data_region(self) -> str | None:
        return None

    def serialize_definition(self) -> dict[str, Any]:
        return self.definition.model_dump(mode="json")

    @abc.abstractmethod
    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get the bounds of the dataset, in EPSG:4326"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_dates(self) -> list[datetime.datetime]:
        raise NotImplementedError


# Used to lookup datasets by class name
_DATASET_CLASS_REGISTRY: dict[str, type[Dataset[Any]]] = {}


class _DatasetRegistry:
    """Factory creating instances of dataset subclasses based on an id and a a config"""

    def __init__(self) -> None:
        self._registry: dict[str, type[Dataset[Any]]] = {}

    def register_class(self, name: str, cls: type[Dataset[Any]]) -> None:
        if name in self._registry:
            raise ValueError(f"Name {name} already registered")
        if cls in self._registry.values():
            raise ValueError(f"Dataset class {cls} already registered")

        """Register a dataset class"""
        self._registry[name] = cls

    def unregister_class(self, name: str) -> None:
        """Unregister a dataset class"""
        if name not in self._registry:
            raise ValueError(f"Name {name} not registered")
        del self._registry[name]

    def get_registry_name(self, cls: type[Dataset[Any]]) -> str:
        for name, dataset_cls in self._registry.items():
            if dataset_cls == cls:
                return name
        raise ValueError(f"Dataset class {cls} is not registered")

    def create(
        self,
        class_name: str,
        dataset_id: uuid.UUID | None,
        dataset_version_id: uuid.UUID | None,
        dataset_name: str,
        metadata: DatasetMetadata,
        definition: dict[str, Any],
    ) -> Dataset[Any]:
        """Create a dataset instance"""
        if class_name not in self._registry:
            raise ValueError(f"Dataset class with name {class_name} not registered")
        cls = self._registry[class_name]
        return cls.from_serialized_definition(
            dataset_id, dataset_version_id, dataset_name, metadata, definition
        )


registry = _DatasetRegistry()
