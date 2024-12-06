"""Includes generator methods."""

from typing import List, Optional, Union

from asyncua import ua

from voraus_opcua_generator.formatter import (
    format_arg_name,
    format_arg_type,
    format_class_name,
    format_doc_string,
    format_method_args,
    format_method_call_args,
    format_method_name,
    format_method_return,
    format_node_id,
    format_variable_name,
)
from voraus_opcua_generator.schema import (
    ClientDescription,
    MethodSchema,
    NodeSchema,
    ObjectSchema,
    OverrideOptions,
    VariableSchema,
)
from voraus_opcua_generator.source_builder.source_builder import SourceBuilder


def generate_code(description: ClientDescription, override: Optional[List[OverrideOptions]] = None) -> str:
    """Main function to generate code.

    Args:
        description (ClientDescription):
            Schema to write

        override (Optional[List[OverrideOptions]]):
            Override options

    Returns:
        str:
            _description_
    """
    source_builder = SourceBuilder()

    if override is not None:
        for opt in override:
            node = search_node(description.objects, opt.node_id)
            if node is not None:
                node.name = opt.name

    write_header(source_builder)

    for obj in description.objects:
        source_builder.writeln()
        write_object(source_builder, obj)

    return source_builder.get_value()


def search_node(objects: List[ObjectSchema], node_id: ua.NodeId) -> Optional[NodeSchema]:
    """Search node in a list of objects.

    Args:
        objects (List[ObjectSchema]): List of related nodes
        node_id (ua.NodeId): wanted id

    Returns:
        Optional[NodeSchema]: Found Node
    """
    for obj in objects:
        if obj.node_id == node_id:
            return obj

        members: List[Union[VariableSchema, MethodSchema]] = []
        members.extend(obj.variables)
        members.extend(obj.methods)

        for member in members:
            if member.node_id == node_id:
                return member

    return None


def write_header(source_builder: SourceBuilder) -> None:
    """Write necessary module imports.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
    """
    source_builder.writeln('""" This module is auto-generated """')
    source_builder.writeln()
    source_builder.writeln("from asyncua import ua, Node")
    source_builder.writeln("from voraus_opcua_generator.ua_client.ua_client import UaClient, UaNode")
    source_builder.writeln("from typing import List, Tuple")
    source_builder.writeln()


def write_object(source_builder: SourceBuilder, obj: ObjectSchema) -> None:
    """Writes a object as a new python class.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
        obj (ObjectSchema): Schema of current object
    """
    # write new class
    with source_builder.block(f"class {format_class_name(obj)}:"):
        write_object_docs(source_builder, obj)

        # write __init__
        with source_builder.block("def __init__(self, client: UaClient):"):
            source_builder.writeln("self._client: UaClient = client")
            source_builder.writeln(f"self._node: ua.NodeId = {format_node_id(obj)}")

            # write variables
            if len(obj.variables) > 0:
                source_builder.writeln()
                for variable in obj.variables:
                    write_variable(source_builder, variable)

        # write methods
        if len(obj.methods) > 0:
            source_builder.writeln()
            source_builder.writeln()
            for method in obj.methods:
                write_method(source_builder, method)


def write_object_docs(source_builder: SourceBuilder, obj: ObjectSchema) -> None:
    """Writes a object doc strings.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
        obj (ObjectSchema): Schema of current object
    """
    source_builder.writeln('"""')

    # write method description
    source_builder.write_lines(format_doc_string(obj.description))

    source_builder.writeln('"""')


def write_variable(source_builder: SourceBuilder, variable: VariableSchema) -> None:
    """Writes a variable nodeid as ua.NodeId.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
        variable (VariableSchema): Schema of current variable
    """
    v_name = format_variable_name(variable)
    source_builder.writeln(f"self.{v_name}: UaNode = self._client.get_node({format_node_id(variable)})")


def write_method(source_builder: SourceBuilder, method: MethodSchema) -> None:
    """Writes a method as a new python function of the parent class.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
        method (MethodSchema): Schema of current method
    """
    # format related outputs
    m_name = format_method_name(method)
    m_args = format_method_args(method)
    m_result = format_method_return(method)

    # write function
    with source_builder.block(f"def {m_name}({m_args}) -> {m_result}:"):
        # write docs
        write_method_docs(source_builder, method)

        # write function call
        source_builder.writeln(f"method_id = {format_node_id(method)}")
        source_builder.writeln(f"arguments: List[ua.Variant] = {format_method_call_args(method)}")
        source_builder.writeln("result = self._client.call(self._node, method_id, arguments)")
        source_builder.writeln("return result # type: ignore")


def write_method_docs(source_builder: SourceBuilder, method: MethodSchema) -> None:
    """Writes the method description to the python function docs.

    Args:
        source_builder (SourceBuilder): Target SourceBuilder
        method (MethodSchema): Schema of current method
    """
    source_builder.writeln('"""')

    # write method description
    for line in format_doc_string(method.description):
        source_builder.writeln(line)

    # write input docs
    if method.input:
        source_builder.writeln()
        with source_builder.block("Args:"):
            for arg in method.input:
                with source_builder.block(f"{format_arg_name(arg)} ({format_arg_type(arg)}):"):
                    source_builder.write_lines(format_doc_string(arg.description))

    # write output docs
    if method.output:
        source_builder.writeln()
        with source_builder.block("Returns:"):
            for arg in method.output:
                with source_builder.block(f"{format_arg_name(arg)} ({format_arg_type(arg)}):"):
                    source_builder.write_lines(format_doc_string(arg.description))

    source_builder.writeln('"""')
