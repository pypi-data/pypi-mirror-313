"""A generator for an OPC UA client package."""

from pathlib import Path

from voraus_opcua_generator.client_generator_python.package_base import create_package_base, render_obj
from voraus_opcua_generator.doc_builder.node import Node, initialize_paths
from voraus_opcua_generator.doc_builder.parser import parse_opcua_xml
from voraus_opcua_generator.templates import (
    OVERVIEW_INIT_HEADER_PYTHON_TEMPLATE,
    OVERVIEW_PY_TEMPLATE,
    UTIL_INIT_HEADER_PYTHON_TEMPLATE,
    UTIL_PY_TEMPLATE,
)


def build_client_package(xml_file: Path, target_package_path: Path) -> None:
    """Build a typed python client interface from an OPC UA server XML.

    Args:
        xml_file: The source OPC UA server XML file.
        target_package_path: The target path to place the generated package at.
    """
    nodes = parse_opcua_xml(xml_file)
    root_nodes = [n for n in nodes if n.parent is None]
    initialize_paths(root_nodes)

    for root_node in root_nodes:
        create_package_base(target_package_path, root_node, True)
        render_obj(root_node, target_package_path)

    _build_overview_subpackage(target_package_path / "overview", nodes=nodes)
    _build_util_subpackage(target_package_path / "util")


def _build_overview_subpackage(target_package_path: Path, nodes: list[Node]) -> None:
    """Build an overview of all nodes in a dictionary like structure.

    Do so with node IDs as keys and the nodes in-tree-position as values.
    """
    target_package_path.mkdir()
    rendered_init = OVERVIEW_INIT_HEADER_PYTHON_TEMPLATE.render()
    rendered_overview = OVERVIEW_PY_TEMPLATE.render(nodes=nodes)

    with open(target_package_path / "__init__.py", "w", encoding="utf-8") as file:
        file.write(rendered_init)
    with open(target_package_path / "_overview.py", "w", encoding="utf-8") as file:
        file.write(rendered_overview)


def _build_util_subpackage(target_package_path: Path) -> None:
    """Build an OPC UA util subpackage which contains some interfaces to be used in the templates.

    Args:
        target_package_path: The target path to place the generated package at.
    """
    target_package_path.mkdir()
    rendered_init = UTIL_INIT_HEADER_PYTHON_TEMPLATE.render()
    rendered_util = UTIL_PY_TEMPLATE.render()

    with open(target_package_path / "__init__.py", "w", encoding="utf-8") as file:
        file.write(rendered_init)
    with open(target_package_path / "_util.py", "w", encoding="utf-8") as file:
        file.write(rendered_util)
