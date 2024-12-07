import sys

import pytest
from pydantic_extra_types.color import Color

from neo4j_viz import Node, VisualizationGraph
from neo4j_viz.colors import neo4j_colors


@pytest.mark.parametrize("override", [True, False])
def test_color_nodes_dict(override: bool) -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", color="#FF0000"),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", {"Person": "#000000", "Product": "#00FF00"}, override=override)

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    if override:
        assert VG.nodes[2].color == Color("#00ff00")
    else:
        assert VG.nodes[2].color == Color("#ff0000")


@pytest.mark.parametrize("override", [True, False])
def test_color_nodes_iter_basic(override: bool) -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", color="#FF0000"),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", ["#000000", "#00FF00"], override=override)

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    if override:
        assert VG.nodes[2].color == Color("#00ff00")
    else:
        assert VG.nodes[2].color == Color("#ff0000")


def test_color_nodes_iter_exhausted() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    with pytest.warns(
        UserWarning,
        match=(
            "Ran out of colors for property 'caption'. 3 colors were needed, but only 2 were given, " "so reused colors"
        ),
    ):
        VG.color_nodes("caption", ["#000000", "#00FF00"])

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    assert VG.nodes[2].color == Color("#00ff00")
    assert VG.nodes[3].color == Color("#000000")


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="requires python 3.11 or lower")
def test_color_nodes_palette() -> None:
    from palettable.wesanderson import Moonrise1_5  # type: ignore[import-untyped]

    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", Moonrise1_5.colors)

    assert VG.nodes[0].color == Color((114, 202, 221))
    assert VG.nodes[1].color == Color((240, 165, 176))
    assert VG.nodes[2].color == Color((240, 165, 176))
    assert VG.nodes[3].color == Color((140, 133, 54))


def test_color_nodes_default() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption")

    assert VG.nodes[0].color == Color(neo4j_colors[0])
    assert VG.nodes[1].color == Color(neo4j_colors[1])
    assert VG.nodes[2].color == Color(neo4j_colors[1])
    assert VG.nodes[3].color == Color(neo4j_colors[2])
