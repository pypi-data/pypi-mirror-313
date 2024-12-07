from __future__ import annotations

from typing import Any, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field, field_serializer, field_validator
from pydantic_extra_types.color import Color, ColorType

from .options import CaptionAlignment


class Relationship(BaseModel, extra="allow"):
    """
    A relationship in a graph to visualize.
    All options available in the NVL library (see https://neo4j.com/docs/nvl/current/base-library/#_relationships)
    """

    id: Union[str, int] = Field(
        default_factory=lambda: uuid4().hex, description="Unique identifier for the relationship"
    )
    source: Union[str, int] = Field(
        serialization_alias="from", description="Node ID where the relationship points from"
    )
    target: Union[str, int] = Field(serialization_alias="to", description="Node ID where the relationship points to")
    caption: Optional[str] = Field(None, description="The caption of the relationship")
    caption_align: Optional[CaptionAlignment] = Field(
        None, serialization_alias="captionAlign", description="The alignment of the caption text"
    )
    caption_size: Optional[int] = Field(
        None, serialization_alias="captionSize", description="The size of the caption text"
    )
    color: Optional[ColorType] = Field(None, description="The color of the relationship")

    @field_serializer("color")
    def serialize_color(self, color: Color) -> str:
        return color.as_hex(format="long")

    @field_serializer("id")
    def serialize_id(self, id: Union[str, int]) -> str:
        return str(id)

    @field_serializer("source")
    def serialize_source(self, source: Union[str, int]) -> str:
        return str(source)

    @field_serializer("target")
    def serialize_target(self, target: Union[str, int]) -> str:
        return str(target)

    @field_validator("color")
    @classmethod
    def cast_color(cls, color: ColorType) -> Color:
        if not isinstance(color, Color):
            return Color(color)

        return color

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)
