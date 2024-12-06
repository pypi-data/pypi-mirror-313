import datetime
import os
from collections.abc import Generator
from contextlib import contextmanager
from typing import cast
from urllib.parse import parse_qs, urlparse

import pandas as pd


@contextmanager
def disabled_registration_callbacks() -> Generator[None, None, None]:
    """Context manager that temporarily disables dataset registration callbacks.

    This is useful when you want to prevent automatic registration of datasets,
    for example during dataset loading or copying operations.

    Example:
        ```python
        with disabled_registration_callbacks():
            dataset = Dataset.load(name="my_dataset")
        ```
    """
    from earthscale.datasets.dataset import Dataset

    original_callbacks = Dataset._DATASET_CREATION_CALLBACKS
    Dataset._DATASET_CREATION_CALLBACKS = []
    try:
        yield
    finally:
        Dataset._DATASET_CREATION_CALLBACKS = original_callbacks


def running_in_notebook() -> bool:
    try:
        from IPython import get_ipython  # type: ignore

        if get_ipython() is None:  # type: ignore
            return False
        return True
    except ImportError:
        return False


def create_valid_url(url: str) -> str:
    if is_google_drive_url(url):
        parsed = urlparse(url)
        query = parsed.query
        query_parameters = parse_qs(query)
        query_parameters["supportsAllDrives"] = ["true"]
        query_parameters["alt"] = ["media"]
        query = "&".join(f"{key}={value[0]}" for key, value in query_parameters.items())
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"
    return url


def running_on_cloud_run() -> bool:
    return "K_SERVICE" in os.environ


def in_test_run() -> bool:
    return "PYTEST_VERSION" in os.environ


def is_google_drive_url(url: str) -> bool:
    return "googleapis.com/drive" in url


def is_gcs_url(url: str) -> bool:
    return url.startswith("gs://")


def generate_filter_date_range(
    start: datetime.datetime, end: datetime.datetime
) -> list[datetime.datetime]:
    """
    Generate a list of dates between start and end, with a frequency that depends on the
    length of the date range such that the dates are not too dense or too sparse.
    """
    delta = end - start
    if delta.days > 365:
        dates = (
            pd.date_range(
                start=pd.Timestamp(start) - pd.DateOffset(years=1),
                end=pd.Timestamp(end) + pd.DateOffset(years=1),
                freq="YS",
                inclusive="right",
            )
            .to_pydatetime()
            .tolist()
        )
    elif delta.days >= 365:
        dates = (
            pd.date_range(
                start=pd.Timestamp(start) - pd.DateOffset(months=1),
                end=pd.Timestamp(end) + pd.DateOffset(months=1),
                freq="MS",
                inclusive="right",
            )
            .to_pydatetime()
            .tolist()
        )
    elif delta.days >= 30:
        dates = (
            pd.date_range(
                start=pd.Timestamp(start) - pd.DateOffset(weeks=1),
                end=pd.Timestamp(end) + pd.DateOffset(weeks=1),
                freq="W-MON",
                inclusive="right",
            )
            .to_pydatetime()
            .tolist()
        )
    else:
        dates = (
            pd.date_range(
                start=pd.Timestamp(start) - pd.DateOffset(days=1),
                end=pd.Timestamp(end) + pd.DateOffset(days=1),
                freq="D",
                inclusive="right",
            )
            .to_pydatetime()
            .tolist()
        )
    return cast(list[datetime.datetime], dates)
