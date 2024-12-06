"""This module defines the voraus-opcua-generator documentation builder."""

import os
from pathlib import Path

from voraus_opcua_generator.doc_builder.node import initialize_paths
from voraus_opcua_generator.doc_builder.obj import render_obj
from voraus_opcua_generator.doc_builder.overview import render_overview
from voraus_opcua_generator.doc_builder.parser import parse_opcua_xml
from voraus_opcua_generator.doc_builder.rst import write_root_rst_file
from voraus_opcua_generator.doc_builder.utils import check_gitignore, check_index_content


def build_docs(xml_file: Path, doc_dir: Path, check_gitignore_file: bool = True) -> None:
    """Build OPC-UA documentation RST file from an OPC-UA server XML.

    Args:
        xml_file: The source OPC-UA server XML file.
        doc_dir: The target documentation directory.
        check_gitignore_file: Check for .gitingore entry.
    """
    nodes = parse_opcua_xml(xml_file)
    root_nodes = [n for n in nodes if n.parent is None]
    initialize_paths(root_nodes)

    rst_file_prefix = xml_file.stem
    rst_dir = doc_dir / rst_file_prefix
    gitignore_file = Path.cwd() / ".gitignore"

    check_index_content(doc_dir, rst_file_prefix)
    if check_gitignore_file:
        check_gitignore(rst_dir, gitignore_file)

    rst_dir.mkdir(exist_ok=True)

    for old_rst_file in rst_dir.glob(f"{rst_file_prefix}*.rst"):
        os.remove(old_rst_file)
    for root_node in root_nodes:
        render_obj(root_node, rst_dir=rst_dir, rst_file_prefix=rst_file_prefix)

    render_overview(nodes, rst_dir)
    write_root_rst_file(xml_file, root_nodes, rst_dir, rst_file_prefix)
