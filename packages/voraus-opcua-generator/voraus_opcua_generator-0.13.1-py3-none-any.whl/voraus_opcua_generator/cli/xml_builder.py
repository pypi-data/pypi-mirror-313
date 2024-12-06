"""This module defines an xml builder from a running OPC-UA server instance."""

from asyncio import run as aiorun
from pathlib import Path
from typing import List

from asyncua import Client, Node
from typer import Argument


def build_xml(xml_file_path: Path, opcua_uri: str = Argument("opc.tcp://127.0.0.1:48401")) -> None:
    """Call the asynchronous xml_builder as typer compatible function.

    Args:
        xml_file_path: The target OPC-UA server XML files path.
        opcua_uri: The source OPC-UA server to export the structure from.
    """
    aiorun(build_xml_async(xml_file_path, opcua_uri))


async def build_xml_async(xml_file_path: Path, opcua_uri: str) -> None:
    """Build an OPC-UA representation as XML file from a running OPC-UA server instance.

    Args:
        xml_file_path: The target OPC-UA server XML files path.
        opcua_uri: The source OPC-UA server to export the structure from.
    """
    async with Client(url=opcua_uri) as client:
        nodes = []

        async def iterate(node: Node) -> None:
            ns_index = node.nodeid.NamespaceIndex
            if ns_index == 1:
                nodes.append(node)

            children: List[Node] = await node.get_children()
            for child in children:
                b_name = await child.read_browse_name()
                if ns_index == 1 and b_name.Name in ("InputArguments", "OutputArguments"):
                    nodes.append(child)
                else:
                    await iterate(child)

        objects_root = await client.nodes.root.get_child(["0:Objects"])

        await iterate(objects_root)
        await client.export_xml(nodes, xml_file_path, export_values=True)
