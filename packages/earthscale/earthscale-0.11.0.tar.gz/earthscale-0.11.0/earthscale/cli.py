import dataclasses
import importlib
import inspect
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import click
import loguru
import requests

from earthscale.auth import authenticate as run_auth
from earthscale.auth import get_supabase_client
from earthscale.constants import BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL
from earthscale.datasets.dataset import Dataset
from earthscale.ingest import (
    ingest_dataset_to_earthscale,
    is_dataset_readable_by_earthscale,
    validate_if_dataset_is_ingestable,
)
from earthscale.repositories.dataset import DatasetRepository

# Disable all logging
loguru.logger.disable("earthscale")


@click.group()
def cli() -> None:
    """Earthscale command line tool."""
    pass


def _find_datasets_for_module(
    module: ModuleType,
) -> list[Dataset[Any]]:
    datasets = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, Dataset):
            datasets.append(obj)
    return datasets


def _ingest_if_no_access_and_possible(
    dataset: Dataset[Any],
    ingest_is_set: bool,
) -> tuple[bool, Dataset[Any], str | None]:
    # Returns a tuple of success and message
    message = None
    if not is_dataset_readable_by_earthscale(dataset):
        if not ingest_is_set:
            message = (
                "Dataset is not readable by Earthscale backend. Not ingesting "
                "as --ingest was not set."
            )
            return False, dataset, message

        message = "Ingested dataset to Earthscale's shared storage."
        validate_if_dataset_is_ingestable(dataset)
        dataset = ingest_dataset_to_earthscale(dataset)
    return True, dataset, message


@dataclasses.dataclass
class _RegistrationResult:
    success: bool
    message: str | None


_PACKAGE_ROOT = """
Root directory of the Python pacakge. This directory will be added to the Python path
and all files will be relative to this directory if given. For example, if the package
path is my_project/my_package and the files are in my_project/my_package/data.py, you
can register the datasets in data.py by running
'earthscale register my_project/my_package/data.py -p my_project/my_package'.
If not provided, the current working directory will be used.
"""


@cli.command(help="Register datasets from a Python module.")
@click.option(
    "--ingest",
    is_flag=True,
    help="Ingest any datasets that are not already in Earthscale's shared storage. "
    "Attention, you might incur egress costs by copying data to the shared "
    "bucket!",
)
@click.option(
    "-p",
    "--package_root",
    help=_PACKAGE_ROOT,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    default=None,
)
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
def register(  # noqa: C901
    ingest: bool,
    files: list[str],
    package_root: str | Path | None,
) -> None:
    if len(files) == 0:
        click.secho(
            "No files provided. Please make sure to add at least one file. "
            "For example: 'earthscale register datasets.py'",
            err=True,
            fg="red",
        )
        exit(1)

    package_root = Path().cwd() if package_root is None else Path(package_root)

    absolute_package_root = Path(package_root).resolve()
    sys.path.append(str(absolute_package_root))

    # Look for all Dataset instances in the module
    datasets = []
    for file in files:
        file_path = Path(file).absolute()
        relative_file_path = file_path.relative_to(absolute_package_root)
        # Convert file to python module
        module = (
            str(relative_file_path)
            .replace("/", ".")
            .replace("\\", ".")
            .replace(".py", "")
        )
        try:
            mod = importlib.import_module(module)
        except ImportError as e:
            if "No module named" in str(e):
                click.secho(
                    f"The module {module} could not be found. This is likely "
                    f"because the package root is incorrect. You can try again by "
                    f"setting the package root with the -p flag. Or use the --help "
                    f"flag for more information.",
                    err=True,
                    fg="red",
                )
            else:
                click.secho(
                    f"An error occurred while trying to import {module}: {e}",
                    err=True,
                    fg="red",
                )
            exit(1)
        datasets.extend(_find_datasets_for_module(mod))

    if len(datasets) == 0:
        click.secho(
            "No datasets found in the provided files. ",
            fg="green",
        )
        exit(0)

    named_datasets = [d for d in datasets if d._explicit_name]
    unnamed_datasets = [d for d in datasets if not d._explicit_name]

    if len(named_datasets) == 0:
        click.secho(
            "No named datasets found in the provided files. "
            "Hint: Have you set the `name` attribute on the Datasets? "
            "Only named datasets will be registered.",
            fg="red",
        )
        exit(0)

    if len(unnamed_datasets) > 0:
        click.secho(
            f"Found {len(unnamed_datasets)} unnamed datasets. "
            "Hint: Have you set the `name` attribute on the Datasets? "
            "Only named datasets will be registered.",
            fg="yellow",
        )
    click.echo("")

    click.echo(
        "Found "
        + click.style(str(len(named_datasets)), fg="green")
        + " named dataset(s) in "
        + click.style(str(len(files)), fg="green")
        + " file(s)."
    )

    client = get_supabase_client()
    dataset_repo = DatasetRepository(client)

    # Dictionary from dataset to status message
    registered_datasets = {}
    with click.progressbar(
        named_datasets,
        label=click.style("Registering datasets", fg="blue"),
        color=True,
    ) as bar:
        for dataset in bar:
            success = True
            message = None
            if dataset_repo.exists(dataset.name):
                message = "Dataset already existed and was overwritten"

            try:
                status, dataset, ingest_message = _ingest_if_no_access_and_possible(
                    dataset,
                    ingest,
                )
                if not status:
                    success = False
                    message = ingest_message
                else:
                    if ingest_message is not None:
                        message = ingest_message
                    dataset_repo.add(dataset)
            except Exception as e:
                success = False
                if (
                    isinstance(e, requests.HTTPError)
                    and e.response.json()["detail"]["message"]
                ):
                    message = e.response.json()["detail"]["message"]
                else:
                    message = str(e)
            registered_datasets[dataset] = _RegistrationResult(success, message)

    click.echo("")
    click.echo("Registration results:")
    for dataset, result in registered_datasets.items():
        if result.success:
            message = (
                "  ✅ "
                + click.style(f" '{dataset.name}'", fg="green", bold=True)
                + click.style(f" ({type(dataset).__name__})", fg="green")
            )

            if result.message is not None:
                message += click.style(f": {result.message}")
            click.echo(message)
        else:
            message = (
                "  ❌ "
                + click.style(f" '{dataset.name}'", fg="red", bold=True)
                + click.style(f" ({type(dataset).__name__})", fg="red")
            )
            if result.message is not None:
                message += f": {result.message}"
            click.echo(message)


def _earthscale_has_access(
    url: str,
    backend_url: str,
    session: requests.Session,
) -> bool:
    query_params = {"path": url}
    response = session.get(
        f"{backend_url}/ingest/has-read-access",
        params=query_params,
    )
    response.raise_for_status()
    return cast(bool, response.json())


def _add_url(url: str, name: str, backend_url: str, session: requests.Session) -> None:
    request_data = {
        "url": url,
        "name": name,
    }
    response = session.post(
        f"{backend_url}/datasets/add",
        json=request_data,
    )
    match response.status_code:
        case 500:
            response_json = response.json()
            error_message = response_json["detail"]["message"]
            click.secho(error_message, fg="red")
        case 200:
            click.secho(
                f"Dataset from url '{url}' added successfully to Earthscale. It will "
                f"be available as '{name}' in the Catalog on "
                f"https://app.earthscale.ai.",
                fg="green",
            )
        case _:
            try:
                response.raise_for_status()
            except Exception as e:
                if (
                    isinstance(e, requests.HTTPError)
                    and e.response.json()["detail"]["message"]
                ):
                    message = e.response.json()["detail"]["message"]
                else:
                    message = str(e)
                click.secho(message, fg="red")


@cli.command(help="Add a dataset to Earthscale using only a name and a URL.")
@click.argument("url")
@click.option(
    "-n",
    "--name",
    required=True,
    help="Name of the dataset as it will appear in Earthscale.",
)
def add(
    url: str,
    name: str,
) -> None:
    backend_url = os.getenv(BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL).rstrip("/")
    client = get_supabase_client()
    dataset_repo = DatasetRepository(client)

    session = requests.Session()
    request_headers = {
        "Authorization": f"Bearer {client.auth.get_session().access_token}"
    }
    session.headers = request_headers  # type: ignore

    if not _earthscale_has_access(url, backend_url, session):
        click.secho(
            f"Earthscale does not have access to '{url}'. Please ensure that the "
            f"dataset publicly accessible, on a shared bucket or shared with "
            f"`backend-services@earthscale.ai`.",
            err=True,
            fg="red",
        )
        return

    if dataset_repo.exists(name):
        click.secho(
            f"Dataset '{name}' already exist. It will be overwritten.", fg="yellow"
        )

    _add_url(url, name, backend_url, session)


@cli.command(help="Authenticate with Earthscale.")
def authenticate() -> None:
    run_auth()
    click.secho("Successfully authenticated with Earthscale.", fg="green")


if __name__ == "__main__":
    cli()
