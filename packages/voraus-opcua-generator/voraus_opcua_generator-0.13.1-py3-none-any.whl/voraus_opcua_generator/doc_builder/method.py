"""Contains the Method documentation builder."""

import inspect

from voraus_opcua_generator import templates
from voraus_opcua_generator.doc_builder.node import Node
from voraus_opcua_generator.doc_builder.utils import escape_rst_special_chars


def render_method(node: Node) -> str:
    """Render an rst section according to the template.

    Args:
        node: Node of the OPC UA.

    Raises:
        ValueError: If the node is not an input- or output argument.

    Returns:
        Rendered RST template for the UAMethod.
    """
    if node.parent is not None:
        parent_identifier = node.parent.identifier
    else:
        parent_identifier = "Method has no parent."
    pycode = templates.METHOD_PYTHON_TEMPLATE.render(
        parent_identifier=parent_identifier,
        method_id=node.identifier,
        namespace=node.namespace,
        arguments=node.get_input_arguments(),
        function_name=node.displayname_snake_case,
        input_args=node.get_input_arguments(),
        output_args=node.get_output_arguments(),
    )

    rendered_content = templates.METHOD_TEMPLATE.render(
        name=escape_rst_special_chars(node.path_text),
        nodeid=node.data.nodeid,
        desc=inspect.cleandoc(escape_rst_special_chars(node.data.desc)),
        parent=node.data.parent,
        path=escape_rst_special_chars(node.path_text),
        browsename=escape_rst_special_chars(node.data.browsename),
        datatype=node.data.datatype,
        input_args=node.get_input_arguments(),
        output_args=node.get_output_arguments(),
        pycode=pycode,
    )

    return rendered_content
