"""Tool to create package stubs."""

from pathlib import Path

from voraus_opcua_generator.doc_builder.node import Node
from voraus_opcua_generator.templates import (
    INIT_HEADER_PYTHON_TEMPLATE,
    INIT_PACKAGE_PYTHON_TEMPLATE,
    MODULE_INTERNAL_TEMPLATE,
)


def create_internal_module(target_path: Path, node: Node) -> None:
    """Create a module for a given object to contain the matching python class.

    Args:
        target_path: Where to create the module.
        node: The node to represent in the module.
    """
    internal_filename = f"_{node.displayname_snake_case}.py"
    rendered_module = MODULE_INTERNAL_TEMPLATE.render(node=node)

    with open(target_path / internal_filename, "w", encoding="utf-8") as file:
        file.write(rendered_module)


def create_package_base(target_path: Path, node: Node, root: bool = False) -> None:
    """Create an empty package at a given location, provided the target paths parent directory exists.

    Args:
        target_path: Where to generate the package_base
        node: For which OPC UA node to generate it
        root: Whether the provided node is a root node
    """
    target_path.mkdir()
    if root:
        rendered_init = INIT_PACKAGE_PYTHON_TEMPLATE.render()
        (target_path / "py.typed").touch(exist_ok=True)
    else:
        rendered_init = INIT_HEADER_PYTHON_TEMPLATE.render(node=node)

    with open(target_path / "__init__.py", "w", encoding="utf-8") as file:
        file.write(rendered_init)


def render_obj(node: Node, target_path: Path) -> None:
    """Renders the python representation for a node with the node specific parameters.

    And does so for all it's children in a recursive manner.

    Args:
        node: Node of the OPC UA.
        target_path: Where to generate the nodes representation.
    """
    cur_path: Path = target_path / node.displayname_snake_case
    create_package_base(cur_path, node)
    create_internal_module(cur_path, node)

    # create children
    for child in node.children:
        if child.is_object:
            render_obj(child, cur_path)
