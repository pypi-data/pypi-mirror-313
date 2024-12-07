from collections.abc import Iterable
from typing import Any, Union

from pydantic_extra_types.color import ColorType

ColorsType = Union[dict[Any, ColorType], Iterable[ColorType]]

# Comes from https://neo4j.design/40a8cff71/p/5639c0-color/t/page-5639c0-79109681-33
neo4j_colors = [
    "#FFDF81",
    "#C990C0",
    "#F79767",
    "#56C7E4",
    "#F16767",
    "#D8C7AE",
    "#8DCC93",
    "#ECB4C9",
    "#4D8DDA",
    "#FFC354",
    "#DA7294",
    "#579380",
]
