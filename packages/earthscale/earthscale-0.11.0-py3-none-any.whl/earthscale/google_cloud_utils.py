from typing import cast
from urllib.parse import urlparse

from google.cloud import storage
from loguru import logger


def get_region_from_gcs_url(url: str) -> str | None:
    """Will return the region from a GCS URL"""
    parsed_url = urlparse(url)
    bucket_name = parsed_url.netloc
    client = storage.Client()
    try:
        bucket = client.get_bucket(bucket_name)
        return cast(str, bucket.location.lower())
    except Exception as e:
        logger.error(f"Error getting region from GCS URL: {e}")
        return None
