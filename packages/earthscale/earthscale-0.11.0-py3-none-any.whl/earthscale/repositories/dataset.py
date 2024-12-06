import os
import uuid
from typing import Any, TypeVar, cast

import requests
from loguru import logger
from postgrest.base_request_builder import BaseFilterRequestBuilder

from earthscale.api import DatasetRegistrationRequest, DatasetRegistrationResponse
from earthscale.constants import (
    BACKEND_URL_ENV_VAR,
    DEFAULT_BACKEND_URL,
)
from earthscale.datasets.dataset import (
    Dataset,
    DatasetDomain,
    DatasetMetadata,
    registry,
)
from earthscale.repositories.utils import (
    timestamp_to_iso,
)
from supabase import Client

_DATASET_VERSIONS_TABLE = "dataset_versions"
_LATEST_DATASETS_TABLE = "datasets_latest"


class DatasetProcessingError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class NoOrganizationError(Exception):
    pass


class DatasetNotFoundError(Exception):
    pass


def get_org_id_for_user(
    client: Client,
    user_id: str,
) -> str:
    # This works because we have a policy that a user can only
    # view their own user info
    result = client.table("users").select("*").eq("id", user_id).execute()
    if result.data is None or len(result.data) == 0:
        raise UserNotFoundError(f"User {user_id} not found")
    org_id: str = result.data[0]["org_id"]
    if org_id is None:
        raise NoOrganizationError(f"User {user_id} has no organization")
    return org_id


DatasetType = TypeVar("DatasetType", bound=Dataset[Any])


class DatasetRepository:
    def __init__(
        self,
        client: Client,
        backend_url: str | None = None,
        domain: DatasetDomain | None = None,
        version: str | None = None,
    ):
        self.domain = domain
        self.version = version
        if backend_url is None:
            backend_url = os.getenv(BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL)

        self._backend_url = backend_url.rstrip("/")

        if self.domain == DatasetDomain.WORKSPACE and version:
            raise ValueError("Cannot version a workspace dataset")

        self.client = client

    def _get_version_raw(self, dataset_version_id: uuid.UUID) -> list[dict[str, Any]]:
        query = (
            self.client.table(_DATASET_VERSIONS_TABLE)
            .select("*")
            .eq("id", dataset_version_id)
            .order("updated_at", desc=True)
        )
        query = self._add_common_filters(query)
        results = query.limit(1).execute()
        if results.data is None or len(results.data) == 0:
            raise DatasetNotFoundError(
                f"No dataset version found with id" f" {dataset_version_id}"
            )
        return cast(list[dict[str, Any]], results.data)

    def get_version(
        self,
        dataset_version_id: uuid.UUID,
    ) -> Dataset[Any]:
        results = self._get_version_raw(dataset_version_id)
        dataset = self._raw_results_to_datasets(results)[0]
        return dataset

    def get_version_and_cache_key(
        self,
        dataset_version_id: uuid.UUID,
    ) -> tuple[Dataset[Any], uuid.UUID | None]:
        results = self._get_version_raw(dataset_version_id)
        dataset = self._raw_results_to_datasets(results)[0]
        cache_key = results[0]["cache_key"]
        return dataset, uuid.UUID(cache_key) if cache_key else None

    def exists(
        self,
        name: str,
    ) -> bool:
        query = (
            self.client.table(_LATEST_DATASETS_TABLE)
            .select("*")
            .eq("name", name)
            .limit(1)
        )
        results = query.limit(1).execute()
        return results.data is not None and len(results.data) > 0

    def get_latest_by_name(
        self,
        name: str,
    ) -> Dataset[Any]:
        query = (
            self.client.table(_LATEST_DATASETS_TABLE)
            .select("*")
            .eq("name", name)
            .order("updated_at", desc=True)
        )
        query = self._add_common_filters(query)
        results = query.limit(1).execute()
        datasets = self._raw_results_to_datasets(results.data)
        if len(datasets) == 0:
            raise DatasetNotFoundError(f"No dataset found with name '{name}'")
        dataset = datasets[0]
        return dataset

    def get_latest(
        self,
        dataset_id: uuid.UUID,
    ) -> Dataset[Any]:
        query = (
            self.client.table(_LATEST_DATASETS_TABLE)
            .select("*")
            .eq("dataset_id", dataset_id)
            .order("updated_at", desc=True)
        )
        query = self._add_common_filters(query)
        results = query.limit(1).execute()
        datasets = self._raw_results_to_datasets(results.data)
        if len(datasets) == 0:
            raise DatasetNotFoundError(f"No dataset found with id {dataset_id}")
        dataset = datasets[0]
        return dataset

    def _add_common_filters(
        self, query: BaseFilterRequestBuilder[Any]
    ) -> BaseFilterRequestBuilder[Any]:
        if self.domain:
            query = query.eq("domain", self.domain)
        if self.version:
            query = query.eq("version", self.version)
        return query

    def get_all(
        self,
    ) -> list[Dataset[Any]]:
        query = (
            self.client.table(_DATASET_VERSIONS_TABLE)
            .select("*")
            .order("updated_at", desc=True)
        )
        query = self._add_common_filters(query)
        results = query.execute()
        datasets = self._raw_results_to_datasets(results.data)
        return datasets

    def get_recent(
        self,
        most_recent_timestamp: int,
    ) -> list[Dataset[Any]]:
        iso = timestamp_to_iso(most_recent_timestamp)
        query = (
            self.client.table(_DATASET_VERSIONS_TABLE)
            .select("*")
            .gt("updated_at", iso)
            .order("updated_at", desc=True)
        )
        query = self._add_common_filters(query)

        results = query.execute()
        datasets = self._raw_results_to_datasets(results.data)
        return datasets

    def add(
        self,
        dataset: DatasetType,
        match_by_name: bool = True,
    ) -> DatasetType:
        """
        Adds a dataset to the repository. If `match_by_name` is True, the dataset is
        matched by name. If a dataset with the same name exists, and is accessible by
        the user, a new version of the dataset is created. If multiple datasets with the
        same name exist, an error is raised. In this case, specify `match_by_name` as
        False and provide a dataset id.

        If `match_by_name` is False and a dataset id is specified, a new version of the
        dataset is created.

        In any other case, a new dataset is created.
        """
        # TODO: remove DatasetDomain in all places (we don't need it anymore)
        data = DatasetRegistrationRequest.from_dataset(
            dataset, self.domain or DatasetDomain.CATALOG, match_by_name
        ).model_dump(mode="json")

        response = requests.post(
            f"{self._backend_url}/datasets/register",
            json=data,
            headers={
                "Authorization": f"Bearer {self.client.auth.get_session().access_token}"
            },
        )
        response.raise_for_status()
        return cast(
            DatasetType,
            self.get_version(
                DatasetRegistrationResponse.model_validate_json(
                    response.content
                ).dataset_version_id
            ),
        )

    @staticmethod
    def _raw_results_to_datasets(results: list[dict[str, Any]]) -> list[Dataset[Any]]:
        datasets = []
        seen_names = set()
        for result in results:
            if result["name"] in seen_names:
                continue
            try:
                dataset = registry.create(
                    result["class_name"],
                    result["dataset_id"],
                    result["id"],
                    result["name"],
                    DatasetMetadata(**result["metadata"]),
                    result["definition"],
                )

                datasets.append(dataset)
                seen_names.add(result["name"])
            except Exception as e:
                logger.error(f"Error loading dataset {result['name']}: {e}")
                raise e
        return datasets
