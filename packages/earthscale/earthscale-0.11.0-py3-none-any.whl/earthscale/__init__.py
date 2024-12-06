# We're adding a noqa here as dataset needs to be imported before the DatasetRepository
import os
import uuid
from typing import Any

from loguru import logger

# from earthscale.aoi import AOI
from earthscale.auth import get_supabase_client
from earthscale.datasets.dataset import Dataset, DatasetDomain

# from earthscale.repositories.aoi import AOIRepository
from earthscale.repositories.dataset import DatasetRepository
from earthscale.utils import disabled_registration_callbacks, running_in_notebook


def _register_dataset(dataset: Dataset[Any]) -> None:
    from earthscale.ingest import (
        ingest_dataset_to_earthscale,
        is_dataset_readable_by_earthscale,
        validate_if_dataset_is_ingestable,
    )

    supabase_client = get_supabase_client()
    dataset_repo = DatasetRepository(supabase_client, domain=DatasetDomain.WORKSPACE)

    if not is_dataset_readable_by_earthscale(dataset):
        logger.warning(f"Dataset {dataset.name} is not readable by Earthscale backend.")
        should_copy = (
            input("Copy dataset to Earthscale's shared storage? (y/n): ") or "y"
        )
        if should_copy.lower() == "y":
            logger.info("Copying dataset to Earthscale's shared storage...")
            with disabled_registration_callbacks():
                validate_if_dataset_is_ingestable(dataset)
                dataset = ingest_dataset_to_earthscale(dataset)
        else:
            logger.warning(
                f"Not registering dataset {dataset.name} as it is not readable by "
                "Earthscale backend."
            )
            return

    with disabled_registration_callbacks():
        dataset_repo.add(dataset)


def _load_dataset(
    dataset_id: uuid.UUID | None,
    dataset_version_id: uuid.UUID | None,
    name: str | None,
) -> Dataset[Any]:
    num_set = sum(
        [dataset_id is not None, dataset_version_id is not None, name is not None]
    )
    if num_set != 1:
        raise ValueError(
            "Exactly one of dataset_id, dataset_version_id, or name must be provided"
        )

    supabase_client = get_supabase_client()
    with disabled_registration_callbacks():
        dataset_repo = DatasetRepository(supabase_client)
        if dataset_id is not None:
            return dataset_repo.get_latest(dataset_id)
        if dataset_version_id is not None:
            return dataset_repo.get_version(dataset_version_id)
        if name is not None:
            return dataset_repo.get_latest_by_name(name)

        raise ValueError(
            "Exactly one of dataset_id, dataset_version_id, or name must be provided"
        )


# def _load_aoi(name: str) -> AOI:
#     supabase_client = get_supabase_client()
#     aoi_repo = AOIRepository(supabase_client)
#     return aoi_repo.get_by_name(name)


# Enable registration of datasets outside of the notebook context
_ALWAYS_REGISTER = os.getenv("EARTHSCALE_ALWAYS_REGISTER", None) is not None

# In the case of running the SDK in a notebook, we want to register datasets
# automatically
if running_in_notebook() or _ALWAYS_REGISTER:
    Dataset.register_dataset_creation_callback(_register_dataset)

Dataset.register_dataset_load_callback(_load_dataset)
# AOI.register_aoi_load_callback(_load_aoi)

__all__ = [
    "Dataset",
    "DatasetDomain",
]
