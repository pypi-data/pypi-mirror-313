"""Contains a parser for OPC UA XML files."""

from pathlib import Path

from asyncua.common.xmlparser import NodeData, XMLParser

from voraus_opcua_generator.doc_builder.node import Node


class HasNoParent(Exception):
    """Exception raised for errors while accessing the parent attribute of nodes that have none.

    Attributes:
        node -- node which has no parent
    """

    def __init__(self, node: Node) -> None:
        """Spawn a HasNoPArent exception for the given node.

        Args:
            node: A root node that (allegedly) has no parent.
        """
        self.node = node
        self.message = f"Node {node.data.nodeid} has no parent"
        super().__init__(self.message)


def get_objects_node_data() -> NodeData:
    """Objects node data according OPC UA specification.

    More information on https://files.opcfoundation.org/schemas/UA/1.02/Opc.Ua.NodeSet2.xml.

    Return :
        The node data of the root node.
    """
    node_data = NodeData()
    node_data.nodetype = "UAObject"
    node_data.nodeid = "i=85"
    node_data.browsename = "Objects"
    node_data.displayname = "Objects"
    node_data.parent = "i=84"
    node_data.desc = "The browse entry point when looking for objects in the server address space."

    return node_data


def parse_opcua_xml(path: Path) -> list[Node]:
    """Parses the XML of an OPC UA Server and adds children to the nodes.

    Args:
        path: Path of the XML file

    Returns:
        : Parsed nodes with children
    """
    parser = XMLParser()
    parser.parse_sync(xmlpath=path)

    node_datas: list[NodeData] = parser.get_node_datas()
    node_datas.append(get_objects_node_data())

    # Create a dictionary with node id and node class, which is able to store children.
    nodes: dict[str, Node] = {d.nodeid: Node(data=d) for d in node_datas}

    # Create children and parent references
    for node in nodes.values():
        parent_nodeid = node.data.parent
        if parent_nodeid in nodes:
            parent = nodes[parent_nodeid]
            parent.children.append(node)
            node.parent = parent

    return list(nodes.values())
