import uuid
from typing import Any

from loguru import logger
from shapely.geometry import shape
from shapely.wkt import dumps as wkt_dumps

from earthscale.aoi import AOI
from earthscale.repositories.utils import (
    timestamp_to_iso,
)
from supabase import Client

_AOI_TABLE = "aois"


def _raw_results_to_aois(results: list[dict[str, Any]]) -> list[AOI]:
    aois = []
    for result in results:
        geometry = shape(result["geometry"])
        try:
            aoi = AOI(
                name=result["name"],
                geometry=geometry,
            )
            aois.append(aoi)
        except Exception as e:
            logger.error(f"Error loading AOI {result['name']}: {e}")
    return aois


class AOINotFoundError(Exception):
    pass


class AOIRepository:
    def __init__(
        self,
        client: Client,
    ):
        self.client = client

    def get(
        self,
        id_: str,
    ) -> AOI:
        query = (
            self.client.table(_AOI_TABLE)
            .select("*")
            .eq("id", id_)
            .order("updated_at", desc=True)
        )
        results = query.limit(1).execute()
        items = self.raw_results_to_items(results.data)
        if len(items) == 0:
            raise AOINotFoundError(f"No item found with id {id_}")
        item = items[0]
        return item

    def get_by_name(
        self,
        name: str,
    ) -> AOI:
        query = (
            self.client.table(_AOI_TABLE)
            .select("*")
            .eq("name", name)
            .order("updated_at", desc=True)
        )
        results = query.limit(1).execute()
        items = self.raw_results_to_items(results.data)
        if len(items) == 0:
            raise AOINotFoundError(f"No item found with name {name}")
        item = items[0]
        return item

    def get_all(
        self,
    ) -> list[AOI]:
        results = (
            self.client.table(_AOI_TABLE)
            .select("*")
            .order("updated_at", desc=True)
            .execute()
        )
        items = self.raw_results_to_items(results.data)
        return items

    def get_recent(
        self,
        most_recent_timestamp: int,
    ) -> list[AOI]:
        iso = timestamp_to_iso(most_recent_timestamp)
        results = (
            self.client.table(_AOI_TABLE)
            .select("*")
            .gt("updated_at", iso)
            .order("updated_at", desc=True)
            .execute()
        )
        items = self.raw_results_to_items(results.data)
        return items

    def add(
        self,
        item: AOI,
    ) -> None:
        existing_items = (
            self.client.table(_AOI_TABLE)
            .select("*")
            .eq("name", item.name)
            .order("updated_at", desc=True)
            .limit(1)
            .execute()
        )
        results = existing_items.data
        created_at_timestamp: int | None = None
        if results and len(results) > 0:
            created_at_timestamp = results[0]["created_at"]

        item_dict = self.item_to_dict(item)
        if created_at_timestamp:
            item_dict["created_at"] = created_at_timestamp
        user = self.client.auth.get_user().user

        if "id" not in item_dict:
            item_dict["id"] = str(uuid.uuid4())

        if "user_id" not in item_dict:
            item_dict["user_id"] = user.id

        self.client.table(_AOI_TABLE).insert(item_dict).execute()

    @staticmethod
    def raw_results_to_items(results: list[dict[str, Any]]) -> list[AOI]:
        return _raw_results_to_aois(results)

    @staticmethod
    def item_to_dict(item: AOI) -> dict[str, Any]:
        geometry = wkt_dumps(item.geometry)
        return {
            "name": item.name,
            "geometry": geometry,
        }
