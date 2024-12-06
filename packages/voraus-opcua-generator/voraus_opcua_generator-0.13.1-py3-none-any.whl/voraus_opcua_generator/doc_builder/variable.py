"""Contains the variable documentation builder."""

from voraus_opcua_generator import templates
from voraus_opcua_generator.doc_builder.node import Node
from voraus_opcua_generator.doc_builder.utils import escape_rst_special_chars


def render_variable(node: Node) -> str:
    """Render an rst based on the according Template.

    Args:
        node: Current OPC UA node.

    Returns:
        Rendered RST template for the UA variable.
    """
    python_code = templates.VARIABLE_PYTHON_TEMPLATE.render(
        inumber=node.identifier,
        namespace=node.namespace,
        access_level=node.access_level.name,
        value=node.data.value,
    )

    rendered_content = templates.VARIABLE_TEMPLATE.render(
        name=escape_rst_special_chars(node.path_text),
        nodeid=node.data.nodeid,
        access_level=str(node.access_level.name),
        value=node.data.value,
        desc=escape_rst_special_chars(node.data.desc).replace(".", ""),
        parent=node.data.parent,
        path=escape_rst_special_chars(node.path_text),
        valuetype=node.data.valuetype,
        browsename=escape_rst_special_chars(node.data.browsename),
        datatype=node.data.datatype,
        pycode=python_code,
    )
    return rendered_content
