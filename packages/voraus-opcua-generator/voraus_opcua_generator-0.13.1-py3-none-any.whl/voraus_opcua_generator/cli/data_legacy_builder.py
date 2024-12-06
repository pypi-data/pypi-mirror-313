"""A simple (yet legacy) generator for no-cores data class."""

from pathlib import Path

from voraus_opcua_generator.data_generator_legacy.generator import render_data_class
from voraus_opcua_generator.doc_builder.node import initialize_paths
from voraus_opcua_generator.doc_builder.parser import parse_opcua_xml


def build_data_legacy(xml_file: Path, data_path: Path) -> None:
    """Build RemoteRobot's data class from an OPC-UA server XML.

    Args:
        xml_file: The source OPC UA server XML file.
        data_path: The target data files path.
    """
    nodes = parse_opcua_xml(xml_file)
    root_nodes = [n for n in nodes if n.parent is None]
    initialize_paths(root_nodes)

    render_data_class(nodes, data_path)
