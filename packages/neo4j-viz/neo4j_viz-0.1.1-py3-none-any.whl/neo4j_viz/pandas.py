from __future__ import annotations

from pandas import DataFrame

from .node import Node
from .relationship import Relationship
from .visualization_graph import VisualizationGraph


def from_dfs(node_df: DataFrame, rel_df: DataFrame) -> VisualizationGraph:
    nodes = []
    for _, row in node_df.iterrows():
        node = Node(**row.to_dict())
        nodes.append(node)

    relationships = []
    for _, row in rel_df.iterrows():
        rel = Relationship(**row.to_dict())
        relationships.append(rel)

    return VisualizationGraph(nodes=nodes, relationships=relationships)
