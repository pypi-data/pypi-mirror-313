"""Contains a node class, which represents all OPC UA types like UAObject, UAMethod and UAVariable."""

from __future__ import annotations

import re
from typing import Optional

from asyncua.common.xmlparser import NodeData
from asyncua.ua import AccessLevel

from voraus_opcua_generator.doc_builder.argument import Argument
from voraus_opcua_generator.doc_builder.utils import NODE_ID_REGEX, mixed_to_snake_case

NODE_NAMESPACE_REGEX = re.compile(r"ns=(\d+);")


class Node:
    """Handle nodes and check node type."""

    def __init__(self, data: NodeData) -> None:
        """Adds children, parent and path data to the nodes.

        Args:
            data: Nodedata
        """
        self.data = data
        self.children: list["Node"] = []
        self.parent: Optional["Node"] = None
        self.path: Optional[list["Node"]] = None
        self.identifier: str = re.findall(NODE_ID_REGEX, self.data.nodeid)[0]
        self.displayname_snake_case = mixed_to_snake_case(self.data.displayname)
        self.is_variable: bool = self.data.nodetype == "UAVariable"
        self.is_method: bool = self.data.nodetype == "UAMethod"
        self.is_method_argument: bool = self.data.displayname in ("OutputArguments", "InputArguments")
        self.is_object: bool = self.data.nodetype == "UAObject"

    @property
    def method_ids(self) -> list[str]:
        """Creates a list with the node ids of the child methods.

        Returns:
            A list of the child method node ids.
        """
        return [c.data.nodeid for c in self.children if c.is_method]

    @property
    def methods(self) -> list[Node]:
        """Emit an ordered list of child nodes, which represent methods of this node.

        Order the elements by `.data.nodeid`.

        Returns:
            A list of child method nodes.
        """
        filtered_methods = [c for c in self.children if c.is_method]
        return sorted(filtered_methods, key=lambda child: child.data.nodeid)

    @property
    def variable_ids(self) -> list[str]:
        """Creates a list with the node ids of the child variables.

        Returns:
            A list of the child variable node ids.
        """
        return [c.data.nodeid for c in self.children if c.is_variable]

    @property
    def variables(self) -> list[Node]:
        """Emit an ordered list of Nodes which represent variables of this Node.

        Order the elements by `.data.nodeid`.

        Returns:
            A list of child variable nodes.
        """
        filtered_variables = [c for c in self.children if c.is_variable]
        return sorted(filtered_variables, key=lambda child: child.data.nodeid)

    @property
    def children_ids(self) -> list[str]:
        """Creates a list with the node ids of the children.

        Returns:
            A list of the children node ids.
        """
        return [c.data.nodeid for c in self.children if c.is_object]

    @property
    def objects(self) -> list[Node]:
        """Emit an ordered list of Nodes which represent child objects of this Node.

        Order the elements by `.data.nodeid`.

        Returns:
            A list of child object nodes.
        """
        filtered_variables = [c for c in self.children if c.is_object]
        return sorted(filtered_variables, key=lambda child: child.data.nodeid)

    @property
    def path_text(self) -> str:
        """Creates the path text for the rst File.

        Raises:
            ValueError: Raised if the path is none.

        Returns:
            The path text as an string.
        """
        if self.path is not None:
            return ".".join(p.data.displayname for p in self.path)
        raise ValueError(f"Path has not been set using 'initialize_paths' method. Nodeid: {self.data.nodeid}")

    @property
    def namespace(self) -> Optional[str]:
        """Gets the namespace of an opcua node.

        Returns:
            The namespace of the node.
        """
        if re.match(NODE_NAMESPACE_REGEX, self.data.nodeid):
            # The node id contains a namespace and an id
            return re.findall(NODE_NAMESPACE_REGEX, self.data.nodeid)[0]
        return None

    @property
    def access_level(self) -> AccessLevel:
        """Gets the access level information from the acess level integer.

        Raises:
            ValueError: If the accesslevel is not an int or none.

        Returns:
            The accesslevel
        """
        if self.data.accesslevel is None:
            # Default according UA specs
            return AccessLevel.CurrentRead
        if isinstance(self.data.accesslevel, int):
            return AccessLevel(self.data.accesslevel)
        raise ValueError(f"Accesslevel has value {self.data.accesslevel}")

    def any_method_has_input_arguments(self) -> bool:
        """Whether any of the nodes methods has input arguments.

        Returns:
            True if there are any, False if there are none.
        """
        methods = self.methods
        for method in methods:
            if len(method.get_input_arguments()) > 0:
                return True
        return False

    def any_method_has_output_arguments(self) -> bool:
        """Whether any of the nodes methods has output arguments.

        Returns:
            True if there are any, False if there are none.
        """
        methods = self.methods
        for method in methods:
            if len(method.get_output_arguments()) > 0:
                return True
        return False

    def get_input_arguments(self) -> list[Argument]:
        """Gets the input arguments of the opcua method node.

        Returns:
            The input arguments.
        """
        for child in self.children:
            if child.data.displayname == "InputArguments":
                return child.parse_arguments()
        return []

    def get_output_arguments(self) -> list[Argument]:
        """The output arguments of the opcua method node.

        Returns:
           The output arguments.
        """
        for child in self.children:
            if child.data.displayname == "OutputArguments":
                return child.parse_arguments()
        return []

    def parse_arguments(self) -> list[Argument]:
        """Parses the input or output arguments of an opcua method node.

        Returns:
            The parsed arguments as a list.
        """
        if self.data.value is None:
            return []
        return [Argument(a) for a in self.data.value]


def initialize_paths_recursive(node: Node, parent_path: Optional[list[Node]] = None) -> None:
    """Initialize the recursive paths ot the nodes children starting with the root nodes.

    Args:
        node: Current Node
        parent_path: Path of the nodes parent. Defaults to None.
    """
    path: list[Node] = [] if parent_path is None else parent_path.copy()
    path.append(node)

    node.path = path
    for child in node.children:
        initialize_paths_recursive(child, path)


def initialize_paths(nodes: list[Node]) -> None:
    """Initializes the function 'initialize_paths_recursive' for the supplied root nodes.

    Args:
        nodes: List of the root_nodes
    """
    for node in nodes:
        initialize_paths_recursive(node)
