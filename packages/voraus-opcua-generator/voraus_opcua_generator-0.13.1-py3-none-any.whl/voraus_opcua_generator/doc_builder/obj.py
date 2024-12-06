"""Contains the OPC UAObject representation."""

import logging
from pathlib import Path

from voraus_opcua_generator import templates
from voraus_opcua_generator.doc_builder.method import render_method
from voraus_opcua_generator.doc_builder.node import Node
from voraus_opcua_generator.doc_builder.utils import escape_rst_special_chars
from voraus_opcua_generator.doc_builder.variable import render_variable

_logger = logging.getLogger(__name__)


def render_obj(node: Node, rst_dir: Path, rst_file_prefix: str) -> None:
    """Renders the RST template for a node with the node specific parameters.

    Args:
        node : Node of the OPC UA.
        rst_dir : Directionary of the rst file.
        rst_file_prefix : Prefix of the rst file.
    """
    parent = f"{node.data.parent}" if node.parent is None else f":ref:`{node.data.parent}`"
    py_code = templates.NODE_PYTHON_TEMPLATE.render(inumber=node.identifier, namespace=node.namespace)

    children_template_content, method_template_content, variable_template_content = get_templates(node, rst_file_prefix)

    rendered_content = templates.NODE_TEMPLATE.render(
        name=escape_rst_special_chars(node.path_text),
        nodeid=node.data.nodeid,
        desc=escape_rst_special_chars(node.data.desc).replace(".", ""),
        parent=parent,
        browsename=escape_rst_special_chars(node.data.browsename),
        path=escape_rst_special_chars(node.path_text),
        method=method_template_content,
        variable=variable_template_content,
        children=children_template_content,
        pycode=py_code,
        rst_file_prefix=rst_file_prefix,
        children_ids=node.children_ids,
        variable_ids=node.variable_ids,
        method_ids=node.method_ids,
    )

    for child in node.children:
        if child.is_object:
            render_obj(child, rst_dir=rst_dir, rst_file_prefix=rst_file_prefix)

    rst_file_name = rst_dir / f"{rst_file_prefix}.{node.path_text}.rst"
    with open(rst_file_name, "w", encoding="utf-8") as file:
        file.write(rendered_content)
        _logger.info(rst_file_name.absolute())


def get_templates(node: Node, rst_file_prefix: str) -> tuple[str, str, str]:
    """Gets the rendered children, method and variable templates to render the node.

    Args:
        node : Current OPC_UA node
        rst_file_prefix : Prefix of the imported xml file.

    Returns:
        The rendered templates children_temp, method_temp, variable_temp
    """
    children_template = ""
    method_template = ""
    variable_template = ""

    for child in node.children:
        if child.is_method:
            method_template += f"\n{render_method(child)}\n\n"
        if child.is_variable:
            variable_template += f"\n{render_variable(child)}\n\n"
        if child.is_object:
            children_template += f"   {rst_file_prefix}.{child.path_text}\n"

    return children_template, method_template, variable_template
