import uuid
from typing import Any

from pydantic import BaseModel, model_validator

from earthscale import DatasetDomain
from earthscale.datasets.dataset import (
    Dataset,
    DatasetMetadata,
    DatasetType,
    registry,
)


class DatasetRegistrationRequest(BaseModel):
    @classmethod
    def from_dataset(
        cls, dataset: Dataset[Any], domain: DatasetDomain, match_by_name: bool
    ) -> "DatasetRegistrationRequest":
        return cls(
            match_by_name=match_by_name,
            dataset_id=None if match_by_name else dataset.dataset_id,
            name=dataset.name,
            metadata=dataset.metadata,
            type=dataset.type,
            domain=domain,
            class_name=registry.get_registry_name(type(dataset)),
            dataset_definition=dataset.definition.model_dump(mode="json"),
        )

    match_by_name: bool
    dataset_id: uuid.UUID | None
    name: str
    metadata: DatasetMetadata
    type: DatasetType
    domain: DatasetDomain
    class_name: str
    dataset_definition: dict[str, Any]

    @model_validator(mode="after")
    def match_by_name_should_be_false_if_dataset_id_is_specified(
        self,
    ) -> "DatasetRegistrationRequest":
        if self.dataset_id is not None and self.match_by_name:
            raise ValueError(
                "match_by_name should be False if dataset_id is "
                "specified. Set dataset_id to None to match by name."
            )
        return self


class DatasetRegistrationResponse(BaseModel):
    dataset_id: uuid.UUID
    dataset_version_id: uuid.UUID
