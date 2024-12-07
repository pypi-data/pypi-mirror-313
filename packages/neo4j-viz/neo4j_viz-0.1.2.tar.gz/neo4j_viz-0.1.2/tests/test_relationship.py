from neo4j_viz import CaptionAlignment
from neo4j_viz.relationship import Relationship


def test_rels_with_all_options() -> None:
    rel = Relationship(
        id="1",
        source="2",
        target="3",
        caption="BUYS",
        caption_align=CaptionAlignment.TOP,
        caption_size=12,
        color="#FF0000",
    )

    assert rel.to_dict() == {
        "id": "1",
        "from": "2",
        "to": "3",
        "caption": "BUYS",
        "captionAlign": "top",
        "captionSize": 12,
        "color": "#ff0000",
    }


def test_rels_minimal_rel() -> None:
    rel = Relationship(
        source="1",
        target="2",
    )

    rel_dict = rel.to_dict()

    assert {"id", "from", "to"} == set(rel_dict.keys())
    assert rel_dict["from"] == "1"
    assert rel_dict["to"] == "2"


def test_rels_additional_fields() -> None:
    rel = Relationship(
        source="1",
        target="2",
        componentId=2,
    )

    rel_dict = rel.to_dict()
    assert {"id", "from", "to", "componentId"} == set(rel_dict.keys())
    assert rel.componentId == 2  # type: ignore[attr-defined]
