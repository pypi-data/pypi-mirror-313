"""Contains functions to handle rst files."""

from pathlib import Path

from voraus_opcua_generator import templates
from voraus_opcua_generator.doc_builder.node import Node


def headline_from_path(path: Path) -> str:
    """Creates a camel case and space separated headline from file path.

    Args:
        path: The file path.

    Returns:
        The formatted headline.
    """
    headline = path.stem
    headline = headline.replace("_", " ").replace("-", " ")
    headline = headline.title()
    return headline


def write_root_rst_file(xml_file: Path, root_nodes: list[Node], rst_dir: Path, rst_file_prefix: str) -> None:
    """Write the root rst file.

    Args:
        xml_file : XML file of the OPC UA server.
        root_nodes : OPC UA root nodes.
        rst_dir : Directory of the rst file.
        rst_file_prefix : Prefix of the rst file.
    """
    rst_headline = headline_from_path(xml_file)
    rst_headline_decorator = "=" * len(rst_headline)
    rst_file_name = xml_file.with_suffix(".rst").name
    rst_content = templates.ROOT_TEMPLATE.render(
        head=rst_headline, dec=rst_headline_decorator, root_nodes=root_nodes, rst_file_prefix=rst_file_prefix
    )
    rst_file = rst_dir / rst_file_name

    with open(rst_file, "w", encoding="utf-8") as file:
        file.write(rst_content)
