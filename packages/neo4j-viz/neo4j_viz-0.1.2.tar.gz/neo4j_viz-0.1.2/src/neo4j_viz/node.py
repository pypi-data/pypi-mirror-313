from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_serializer, field_validator
from pydantic_extra_types.color import Color, ColorType

from .options import CaptionAlignment


class Node(BaseModel, extra="allow"):
    """
    A node in a graph to visualize.
    All options available in the NVL library (see https://neo4j.com/docs/nvl/current/base-library/#_nodes)
    """

    id: Union[str, int] = Field(description="Unique identifier for the node")
    caption: Optional[str] = Field(None, description="The caption of the node")
    caption_align: Optional[CaptionAlignment] = Field(
        None, serialization_alias="captionAlign", description="The alignment of the caption text"
    )
    caption_size: Optional[int] = Field(
        None, serialization_alias="captionSize", description="The size of the caption text"
    )
    size: Optional[Union[int, float]] = Field(None, ge=0, description="The size of the node as radius in pixel")
    color: Optional[ColorType] = Field(None, description="The color of the node")

    @field_serializer("color")
    def serialize_color(self, color: Color) -> str:
        return color.as_hex(format="long")

    @field_serializer("id")
    def serialize_id(self, id: Union[str, int]) -> str:
        return str(id)

    @field_validator("color")
    @classmethod
    def cast_color(cls, color: ColorType) -> Color:
        if not isinstance(color, Color):
            return Color(color)

        return color

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)
