"""Creates an overview list with all nodes and nodeids."""

from pathlib import Path

from voraus_opcua_generator import templates
from voraus_opcua_generator.doc_builder.node import Node


def render_overview(nodes: list[Node], rst_dir: Path) -> None:
    """Renders the RST template for an overview over all the nodes with the nodeids.

    Args:
        nodes : List of the OPC UA nodes.
        rst_dir : Directory for the rst file.
    """
    rendered_overview = templates.OVERVIEW_TEMPLATE.render(nodes=nodes)

    with open(rst_dir / "overview.rst", "w", encoding="utf-8") as file:
        file.write(rendered_overview)
