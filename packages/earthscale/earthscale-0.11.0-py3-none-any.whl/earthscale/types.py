from typing import TypedDict

BBOX = tuple[float, float, float, float]


class Chunksizes(TypedDict):
    x: int
    y: int
    time: int
