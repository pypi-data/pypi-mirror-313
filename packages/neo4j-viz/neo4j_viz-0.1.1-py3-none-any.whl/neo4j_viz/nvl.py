import json
import sys
import uuid
from importlib.resources import files

from .node import Node
from .relationship import Relationship

if sys.version_info >= (3, 11):
    from importlib.resources.abc import Traversable
else:
    from importlib.abc import Traversable

from typing import Any, Optional

from IPython.display import HTML


class NVL:
    def __init__(self) -> None:
        js_path: Traversable = files("neo4j_viz.resources.nvl_entrypoint") / "base.js"

        with js_path.open("r", encoding="utf-8") as file:
            self.library_code = file.read()

    def render(
        self,
        nodes: list[Node],
        relationships: list[Relationship],
        options: Optional[dict[str, Any]] = None,
        width: str = "100%",
        height: str = "300px",
    ) -> HTML:
        nodes_json = json.dumps([node.to_dict() for node in nodes])
        rels_json = json.dumps([rel.to_dict() for rel in relationships])
        container_id = str(uuid.uuid4())
        js_code = f"""
        var myNvl = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            {nodes_json},
            {rels_json},
            {options if options is not None else {}}
        );
        """
        full_code = self.library_code + js_code
        html_output = f"""
        <div id="{container_id}" style="width: {width}; height: {height};"></div>
        <script>
            {full_code}
        </script>
        """
        return HTML(html_output)  # type: ignore[no-untyped-call]
