from pydantic import BaseModel

from .node import ComputeNode


class ClusterAllocation(BaseModel):

    nodes: list[ComputeNode] = []
