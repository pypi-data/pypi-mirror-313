from collections.abc import Callable, Iterable
from typing import cast

import networkx as nx
import xarray as xr
from networkx import is_directed_acyclic_graph
from odc.geo.geobox import GeoBox
from shapely import box, intersection_all
from shapely.geometry.base import BaseGeometry

from earthscale.datasets.dataset import DatasetMetadata
from earthscale.types import BBOX, Chunksizes


def get_final_node_name(graph: nx.DiGraph) -> str:
    end_nodes = [node for node in graph.nodes if graph.out_degree(node) == 0]
    assert len(end_nodes) == 1
    return cast(str, end_nodes[0])


class Node:
    def __init__(
        self,
        output_name: str,
        output_metadata: DatasetMetadata | None,
    ):
        self.output_name = output_name
        self.output_metadata = output_metadata


class SourceNode(Node):
    def __init__(
        self,
        function: Callable[
            [BBOX | None, Iterable[str] | None, Chunksizes | None], xr.Dataset
        ],
        output_name: str,
        output_metadata: DatasetMetadata | None,
    ):
        self.function = function
        super().__init__(output_name, output_metadata)


class JoinNode(Node):
    def __init__(
        self,
        match_name: str,
        output_name: str,
        output_metadata: DatasetMetadata | None,
    ):
        self.match_name = match_name
        super().__init__(output_name, output_metadata)


def create_source_graph(
    transformation_name: str,
    output_name: str,
    metadata: DatasetMetadata | None,
    function: Callable[
        [BBOX | None, Iterable[str] | None, Chunksizes | None], xr.Dataset
    ],
) -> nx.DiGraph:
    graph = nx.DiGraph()
    node = SourceNode(
        function=function,
        output_name=output_name,
        output_metadata=metadata,
    )
    graph.add_node(
        transformation_name,
        node=node,
    )
    return graph


def _clip_and_reproject_dset(
    dset: xr.Dataset, bbox: BaseGeometry, target_geobox: GeoBox, match_dset: xr.Dataset
) -> xr.Dataset:
    dset = dset.rio.clip_box(*bbox.bounds)
    dset = dset.odc.reproject(target_geobox)
    # ODC returns latitude and longitude as x and y
    dset = dset.rename(
        {
            "longitude": "x",
            "latitude": "y",
        }
    )
    dset = dset.assign_coords(
        {
            "x": match_dset.x,
            "y": match_dset.y,
        }
    )

    # Spatial ref is present on all datasets
    dset = dset.drop_vars("spatial_ref")
    return dset


def _expand_missing_dims(dset: xr.Dataset) -> xr.Dataset:
    if "x" not in dset.dims:
        x = dset.coords["x"].item()
        if not isinstance(x, float):
            raise ValueError("expected single float value")
        dset = dset.expand_dims({"x": [x]})
    if "y" not in dset.dims:
        y = dset.coords["y"].item()
        if not isinstance(y, float):
            raise ValueError("expected single float value")
        dset = dset.expand_dims({"y": [y]})
    return dset


def get_dset_for_node(
    graph: nx.DiGraph,
    node_name: str,
    bbox: BBOX | None,
    bands: Iterable[str] | None,
    chunksizes: Chunksizes | None,
) -> xr.Dataset:
    node: Node = graph.nodes[node_name]["node"]
    if isinstance(node, SourceNode):
        dset = node.function(bbox, bands, chunksizes)
    elif isinstance(node, JoinNode):
        match_dset = None
        dsets_to_match = {}
        for predecessor in graph.predecessors(node_name):
            dataset_name = graph.nodes[predecessor]["node"].output_name
            dset = get_dset_for_node(graph, predecessor, bbox, bands, chunksizes)
            if dataset_name == node.match_name:
                match_dset = dset
            else:
                dsets_to_match[predecessor] = dset
        assert match_dset is not None

        all_dsets = [match_dset, *list(dsets_to_match.values())]

        # Find overlapping bounding box between datasets
        bounding_box = intersection_all([box(*dset.rio.bounds()) for dset in all_dsets])
        match_dset = match_dset.rio.clip_box(*bounding_box.bounds)
        assert match_dset is not None
        target_geobox = match_dset.odc.geobox

        for node_name, dset in dsets_to_match.items():
            dset_for_node = _clip_and_reproject_dset(
                dset, bounding_box, target_geobox, match_dset
            )
            dsets_to_match[node_name] = dset_for_node
        dset = xr.merge([match_dset, *list(dsets_to_match.values())])
    else:
        raise ValueError(f"Unknown node type: {type(node)}")
    # Ensure only time/x/y dimensions exist
    dset = dset.squeeze()

    allowed_dims = {"time", "x", "y"}
    invalid_dims = set(dset.dims) - allowed_dims
    if invalid_dims:
        raise ValueError(
            f"Dataset contains invalid dimensions: {invalid_dims}. Only time/x/y "
            "dimensions are allowed."
        )

    dset = _expand_missing_dims(dset)

    if "time" in dset.sizes:
        dset = dset.transpose("time", "y", "x")
    else:
        dset = dset.transpose("y", "x")
    return dset


def validate_graph(graph: nx.DiGraph) -> None:
    assert is_directed_acyclic_graph(graph)
    for node in graph.nodes:
        assert isinstance(graph.nodes[node]["node"], Node)
