"""Nodeset Parser Class."""

import xml.etree.ElementTree as ET
from typing import Any, List

from asyncua import ua
from asyncua.common.xmlparser import ExtObj, NodeData, RefStruct, XMLParser
from typing_extensions import deprecated

from voraus_opcua_generator.schema import ArgumentSchema, ClientDescription, MethodSchema, ObjectSchema, VariableSchema


class NodesetParser:
    """Nodeset to Schema parser."""

    def __init__(self, file: str):
        """Initialize NodesetParser."""
        self.file = file
        xml_parser = XMLParser()
        tree = ET.parse(self.file)
        xml_parser.root = tree.getroot()
        self.nodes: List[NodeData] = xml_parser.get_node_datas()

    @deprecated("Nodes have already been loaded upon initialization of NodesetParser.")
    def load_nodes(self) -> None:
        """Load nodes from file."""
        xml_parser = XMLParser()
        tree = ET.parse(self.file)
        xml_parser.root = tree.getroot()
        self.nodes = xml_parser.get_node_datas()

    def parse(self, ids: List[ua.NodeId]) -> ClientDescription:
        """Parse target nodes.

        Args:
            ids (List[ua.NodeId]): Target nodes ids

        Returns:
            ClientDescription: Schema
        """
        # filter for related objects
        description = ClientDescription("SomeName", [])

        target_nodes = [id.to_string() for id in ids]

        # get related nodes
        related_nodes = [node for node in self.nodes if node.nodeid in target_nodes]
        for obj_node in related_nodes:
            if str(obj_node.nodetype) != "UAObject":
                continue

            obj_schema = self.parse_object(obj_node)

            description.objects.append(obj_schema)

        return description

    def parse_object(self, obj_node: NodeData) -> ObjectSchema:
        """Parses NodeData to ObjectSchema.

        Args:
            obj_node (NodeData): Target object data

        Raises:
            ValueError: Is not an object

        Returns:
            ObjectSchema: Parser object schema
        """
        if str(obj_node.nodetype) != "UAObject":
            raise ValueError("Is not a UAObject node")

        obj_schema = ObjectSchema(
            name=str(obj_node.displayname),
            description=str(obj_node.desc),
            node_id=ua.NodeId.from_string(obj_node.nodeid),
            variables=[],
            methods=[],
        )

        for child_node in self.get_children_nodes(obj_node):
            if str(child_node.nodetype) == "UAMethod":
                method_schema = self.parse_method(child_node)
                obj_schema.methods.append(method_schema)

            if str(child_node.nodetype) == "UAVariable":
                variable_schema = self.parse_variable(child_node)
                obj_schema.variables.append(variable_schema)

        return obj_schema

    def parse_method(self, method_node: NodeData) -> MethodSchema:
        """Parses NodeData to MethodSchema.

        Args:
            method_node (NodeData): Target method data

        Raises:
            ValueError: _description_

        Returns:
            MethodSchema: _description_
        """
        if str(method_node.nodetype) != "UAMethod":
            raise ValueError("Is not a UAMethod node")

        method_schema = MethodSchema(
            name=str(method_node.displayname),
            description=str(method_node.desc),
            node_id=ua.NodeId.from_string(method_node.nodeid),
            input=[],
            output=[],
        )

        # read arguments
        for prop_node in self.get_children_nodes(method_node):
            target: List[ArgumentSchema] = []
            if str(prop_node.displayname) == "InputArguments":
                target = method_schema.input
            elif str(prop_node.displayname) == "OutputArguments":
                target = method_schema.output
            else:
                continue

            for arg in prop_node.value:
                target.append(self.parse_argument(arg))

        return method_schema

    @staticmethod
    def parse_variable(variable_node: NodeData) -> VariableSchema:
        """Parses target variable.

        Args:
            variable_node (NodeData): Target variable data

        Raises:
            ValueError: Is not a variable

        Returns:
            VariableSchema: Parsed variable schema
        """
        if str(variable_node.nodetype) != "UAVariable":
            raise ValueError("Is not a UAVariable node")

        variable_schema = VariableSchema(
            name=str(variable_node.displayname),
            description=str(variable_node.desc),
            node_id=ua.NodeId.from_string(variable_node.nodeid),
            value_rank=variable_node.rank,
            type=variable_node.valuetype,
            dimensions=variable_node.dimensions,
        )

        return variable_schema

    @staticmethod
    def parse_argument(ext_obj: ExtObj) -> ArgumentSchema:
        """Parses ExtObj to ArgumentSchema.

        Args:
            ext_obj (ExtObj): Argument data

        Returns:
            ArgumentSchema: Parsed argument schema
        """
        argument = _ParseHelper(ext_obj.body)["Argument"]

        name: str = argument["Name"].value
        desc: str = argument["Description"]["Text"].value
        value_rank: ua.ValueRank = argument["ValueRank"].value
        data_type: ua.VariantType = argument["DataType"]["Identifier"].value

        return ArgumentSchema(
            name=name,
            description=desc,
            type=ua.datatype_to_varianttype(ua.NodeId.from_string(data_type)),
            value_rank=ua.ValueRank(int(value_rank)),
            dimensions=None,
        )

    def get_children_nodes(self, node: NodeData) -> List[NodeData]:
        """List children nodes of a node.

        Args:
            node (NodeData): Target node

        Returns:
            List[NodeData]: Children of node
        """
        refs: List[RefStruct] = node.refs
        children_nodeids = [ref.target for ref in refs if ref.forward]
        return [node for node in self.nodes if node.nodeid in children_nodeids]


class _ParseHelper:
    """Helper to parse xml tags."""

    def __init__(self, value: Any):
        """Initialize helper."""
        self.value: Any = value

    def __getitem__(self, name: str) -> Any:
        """Helper to get XML atributes.

        Args:
            name (str): Attribute name

        Raises:
            KeyError: Is no found

        Returns:
            Any: Value of attribute as helper
        """
        for key, val in self.value:
            if key == name:
                return _ParseHelper(val)

        raise KeyError(f"{str(self.value)} has no key '{name}'")
