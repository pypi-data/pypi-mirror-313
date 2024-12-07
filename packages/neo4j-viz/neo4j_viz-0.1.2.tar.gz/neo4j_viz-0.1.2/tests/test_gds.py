import os
import sys

import pandas as pd
import pytest
from graphdatascience import Graph, GraphDataScience
from pytest_mock import MockerFixture

from neo4j_viz import Node
from neo4j_viz.gds import from_gds

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")

NEO4J_AUTH = ("neo4j", "password")
if os.environ.get("NEO4J_USER"):
    NEO4J_AUTH = (
        os.environ.get("NEO4J_USER", "DUMMY"),
        os.environ.get("NEO4J_PASSWORD", "neo4j"),
    )


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="requires python 3.12 or lower")
@pytest.mark.requires_neo4j_and_gds
def test_from_gds_integration() -> None:
    nodes = pd.DataFrame(
        {
            "nodeId": [0, 1, 2],
            "labels": ["A", "C", ["A", "B"]],
            "score": [1337, 42, 3.14],
            "component": [1, 4, 2],
        }
    )
    rels = pd.DataFrame(
        {
            "sourceNodeId": [0, 1, 2],
            "targetNodeId": [1, 2, 0],
            "relationshipType": ["REL", "REL2", "REL"],
        }
    )

    gds = GraphDataScience(NEO4J_URI, auth=NEO4J_AUTH)

    with gds.graph.construct("flo", nodes, rels) as G:
        VG = from_gds(gds, G, size_property="score", additional_node_properties=["component"])

        assert len(VG.nodes) == 3
        assert sorted(VG.nodes, key=lambda x: x.id) == [
            Node(id=0, labels=["A"], size=float(1337), component=float(1)),
            Node(id=1, labels=["C"], size=float(42), component=float(4)),
            Node(id=2, labels=["A", "B"], size=float(3.14), component=float(2)),
        ]

        assert len(VG.relationships) == 3
        vg_rels = sorted([(e.source, e.target, e.relationshipType) for e in VG.relationships], key=lambda x: x[0])  # type: ignore[attr-defined]
        assert vg_rels == [
            (0, 1, "REL"),
            (1, 2, "REL2"),
            (2, 0, "REL"),
        ]


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="requires python 3.12 or lower")
def test_from_gds_mocked(mocker: MockerFixture) -> None:
    nodes = {
        "A": pd.DataFrame(
            {
                "nodeId": [0, 2],
                "score": [1337, 3.14],
                "component": [1, 2],
            }
        ),
        "B": pd.DataFrame(
            {
                "nodeId": [2],
                "score": [3.14],
                "component": [2],
            }
        ),
        "C": pd.DataFrame(
            {
                "nodeId": [1],
                "score": [42],
                "component": [4],
            }
        ),
    }
    rels = pd.DataFrame(
        {
            "sourceNodeId": [0, 1, 2],
            "targetNodeId": [1, 2, 0],
            "relationshipType": ["REL", "REL2", "REL"],
        }
    )

    mocker.patch(
        "graphdatascience.Graph.__init__",
        lambda x: None,
    )
    mocker.patch(
        "graphdatascience.Graph.name",
        lambda x: "DUMMY",
    )
    node_properties = ["score", "component"]
    mocker.patch(
        "graphdatascience.Graph.node_properties",
        lambda x: pd.Series({lbl: node_properties for lbl in nodes.keys()}),
    )
    mocker.patch("graphdatascience.Graph.node_labels", lambda x: list(nodes.keys()))
    mocker.patch("graphdatascience.GraphDataScience.__init__", lambda x: None)
    mocker.patch("neo4j_viz.gds._node_dfs", return_value=nodes)
    mocker.patch("neo4j_viz.gds._rel_df", return_value=rels)

    gds = GraphDataScience()  # type: ignore[call-arg]
    G = Graph()  # type: ignore[call-arg]

    VG = from_gds(gds, G, size_property="score", additional_node_properties=["component"])

    assert len(VG.nodes) == 3
    assert sorted(VG.nodes, key=lambda x: x.id) == [
        Node(id=0, labels=["A"], size=float(1337), component=float(1)),
        Node(id=1, labels=["C"], size=float(42), component=float(4)),
        Node(id=2, labels=["A", "B"], size=float(3.14), component=float(2)),
    ]

    assert len(VG.relationships) == 3
    vg_rels = sorted([(e.source, e.target, e.relationshipType) for e in VG.relationships], key=lambda x: x[0])  # type: ignore[attr-defined]
    assert vg_rels == [
        (0, 1, "REL"),
        (1, 2, "REL2"),
        (2, 0, "REL"),
    ]
