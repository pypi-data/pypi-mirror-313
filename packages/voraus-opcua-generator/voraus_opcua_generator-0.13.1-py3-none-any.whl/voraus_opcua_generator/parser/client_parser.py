"""Client Parser Class."""

from typing import List

from asyncua import ua
from asyncua.sync import Client, SyncNode

from voraus_opcua_generator.schema import ArgumentSchema, ClientDescription, MethodSchema, ObjectSchema, VariableSchema

_inputArgsName = ua.QualifiedName(NamespaceIndex=0, Name="InputArguments")
_ouputArgsName = ua.QualifiedName(NamespaceIndex=0, Name="OutputArguments")


class ClientParser:
    """Client to Schema parser."""

    def __init__(self, url: str):
        """Initialize ClientParser."""
        self.client = Client(url)

    def parse(self, ids: List[ua.NodeId]) -> ClientDescription:
        """Parse target nodes.

        Args:
            ids (List[ua.NodeId]): Target node ids

        Returns:
            ClientDescription: Schema
        """
        # filter for related objects
        description = ClientDescription("SomeName", [])

        self.client.connect()

        for node_id in ids:
            node = self.client.get_node(node_id)

            if node is None:
                print(f"target nodeid {node_id} not found")
                continue

            if node.read_node_class() != ua.NodeClass.Object:
                print(f"target nodeid {node.nodeid.to_string()} is not an object")
                continue

            obj_schema = self.parse_object(node)
            description.objects.append(obj_schema)

        self.client.disconnect()

        return description

    def parse_object(self, obj_node: SyncNode) -> ObjectSchema:
        """Parse objects node.

        Args:
            obj_node (SyncNode): Target object node

        Returns:
            ObjectSchema: Parsed object schema
        """
        obj_schema = ObjectSchema(
            name=obj_node.read_display_name().Text,
            description=obj_node.read_description().Text,
            node_id=obj_node.nodeid,
            variables=[],
            methods=[],
        )

        children: List[SyncNode] = obj_node.get_children()

        for child_node in children:
            if child_node.read_node_class() == ua.NodeClass.Method:
                method_schema = self.parse_method(child_node)
                obj_schema.methods.append(method_schema)

            if child_node.read_node_class() == ua.NodeClass.Variable:
                variable_schema = self.parse_variable(child_node)
                obj_schema.variables.append(variable_schema)

        return obj_schema

    def parse_method(self, method_node: SyncNode) -> MethodSchema:
        """Parse method node.

        Args:
            method_node (SyncNode): Target methode node

        Returns:
            MethodSchema: Parse methode schema
        """
        method_schema = MethodSchema(
            name=method_node.read_display_name().Text,
            description=method_node.read_description().Text,
            node_id=method_node.nodeid,
            input=[],
            output=[],
        )

        children: List[SyncNode] = method_node.get_children()

        for child in children:
            browse_name = child.read_browse_name()

            if browse_name == _inputArgsName:
                target = method_schema.input
            elif browse_name == _ouputArgsName:
                target = method_schema.output
            else:
                continue

            args = child.read_value()

            for arg in args:
                target.append(self.parse_argument(arg))

        return method_schema

    @staticmethod
    def parse_variable(variable_node: SyncNode) -> VariableSchema:
        """Parse variable node.

        Args:
            variable_node (SyncNode): Target variable node

        Returns:
            VariableSchema: Parse variable schema
        """
        variable_schema = VariableSchema(
            name=variable_node.read_display_name().Text,
            description=variable_node.read_description().Text,
            node_id=variable_node.nodeid,
            value_rank=variable_node.read_value_rank(),
            type=variable_node.read_data_type(),
            dimensions=variable_node.read_array_dimensions(),
        )

        return variable_schema

    @staticmethod
    def parse_argument(arg: ua.Argument) -> ArgumentSchema:
        """Parses ExtObj to ArgumentSchema.

        Args:
            arg (ua.Argument): Argument variant

        Returns:
            ArgumentSchema: Parsed argument schema
        """
        return ArgumentSchema(
            name=arg.Name,
            description=arg.Description.Text,
            type=ua.datatype_to_varianttype(arg.DataType),
            value_rank=arg.ValueRank,
            dimensions=arg.ArrayDimensions,
        )
