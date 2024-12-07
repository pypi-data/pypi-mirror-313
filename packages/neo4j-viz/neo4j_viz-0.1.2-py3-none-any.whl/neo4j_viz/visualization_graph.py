from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Any, Optional

from IPython.display import HTML
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color, ColorType

from .colors import ColorsType, neo4j_colors
from .node import Node
from .nvl import NVL
from .relationship import Relationship


class VisualizationGraph(BaseModel):
    """
    A graph to visualize.
    """

    nodes: list[Node] = Field(description="The nodes in the graph")
    relationships: list[Relationship] = Field(description="The relationships in the graph")

    def render(self, options: Optional[dict[str, Any]] = None, width: str = "100%", height: str = "300px") -> HTML:
        return NVL().render(self.nodes, self.relationships, options=options, width=width, height=height)

    def color_nodes(self, property: str, colors: Optional[ColorsType] = None, override: bool = False) -> None:
        """
        Color the nodes in the graph based on a property.

        Parameters
        ----------
        property:
            The property of the nodes to use for coloring.
        colors:
            The colors to use for the nodes. If a dictionary is given, it should map from property to color.
            If an iterable is given, the colors are used in order.
            The default colors are the Neo4j graph colors.
        override:
            Whether to override existing colors of the nodes, if they have any.
        """
        if colors is None:
            colors = neo4j_colors

        if isinstance(colors, dict):
            self._color_nodes_dict(property, colors, override)
        else:
            self._color_nodes_iter(property, colors, override)

    def _color_nodes_dict(self, property: str, colors: dict[str, ColorType], override: bool) -> None:
        for node in self.nodes:
            color = colors.get(getattr(node, property))

            if color is None:
                continue

            if node.color is not None and not override:
                continue

            if not isinstance(color, Color):
                node.color = Color(color)
            else:
                node.color = color

    def _color_nodes_iter(self, property: str, colors: Iterable[ColorType], override: bool) -> None:
        exhausted_colors = False
        prop_to_color = {}
        colors_iter = iter(colors)
        for node in self.nodes:
            prop = getattr(node, property)

            if prop not in prop_to_color:
                next_color = next(colors_iter, None)
                if next_color is None:
                    exhausted_colors = True
                    colors_iter = iter(colors)
                    next_color = next(colors_iter)
                prop_to_color[prop] = next_color

            color = prop_to_color[prop]

            if node.color is not None and not override:
                continue

            if not isinstance(color, Color):
                node.color = Color(color)
            else:
                node.color = color

        if exhausted_colors:
            warnings.warn(
                f"Ran out of colors for property '{property}'. {len(prop_to_color)} colors were needed, but only "
                f"{len(set(prop_to_color.values()))} were given, so reused colors"
            )
