from neo4j_viz import CaptionAlignment, Node


def test_nodes_with_all_options() -> None:
    node = Node(
        id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
        caption="Person",
        caption_align=CaptionAlignment.TOP,
        caption_size=12,
        color="#FF0000",
        size=10,
    )

    assert node.to_dict() == {
        "id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
        "caption": "Person",
        "captionAlign": "top",
        "captionSize": 12,
        "color": "#ff0000",
        "size": 10,
    }


def test_nodes_minimal_node() -> None:
    node = Node(
        id="1",
    )

    assert node.to_dict() == {
        "id": "1",
    }


def test_node_with_float_size() -> None:
    node = Node(
        id="1",
        size=10.2,
    )

    assert node.to_dict() == {
        "id": "1",
        "size": 10.2,
    }


def test_node_with_additional_fields() -> None:
    node = Node(
        id="1",
        componentId=2,
    )

    assert node.to_dict() == {
        "id": "1",
        "componentId": 2,
    }
