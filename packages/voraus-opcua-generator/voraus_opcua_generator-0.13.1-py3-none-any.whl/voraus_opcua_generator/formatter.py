"""A collection fo format function, that is used by client generator."""

from re import sub
from typing import List

from asyncua import ua

from voraus_opcua_generator.schema import ArgumentSchema, MethodSchema, NodeSchema, ObjectSchema, VariableSchema


def format_node_id(node: NodeSchema) -> str:
    """Formats identifier of a node to a code string.

    Args:
        node (NodeSchema): Schema of current node

    Returns:
        str: Identifier as python code
    """
    return f'ua.NodeId.from_string("{node.node_id.to_string()}")'


def format_class_name(obj: ObjectSchema) -> str:
    """Formats object name to python class name.

    Args:
        obj (ObjectSchema): Schema of current object

    Returns:
        str: Object name as python class name
    """
    return obj.name.replace(" ", "")


def format_variable_name(variable: VariableSchema) -> str:
    """Formats variable name to python variable name.

    Args:
        variable (VariableSchema): Schema of current variable

    Returns:
        str: Variable name as python variable name
    """
    return snake_case(variable.name)


def format_method_name(method: MethodSchema) -> str:
    """Formats method name to python function name.

    Args:
        method (MethodSchema): Schema of current method

    Returns:
        str: Method name as python function name
    """
    return snake_case(method.name)


def format_method_args(method: MethodSchema) -> str:
    """Formats method input arguments to python function args.

    Args:
        method (MethodSchema): Schema of current method

    Returns:
        str: Methond input arguments as python function args
    """
    args = []

    if method.input:
        for arg in method.input:
            args.append(f"{format_arg_name(arg)}: {format_arg_type(arg)}")

    if len(args) <= 0:
        return "self"

    return f"self, {', '.join(args)}"


def format_method_return(method: MethodSchema) -> str:
    """Formats method output arguments to python function result typing.

    Args:
        method (MethodSchema): Schema of current method

    Returns:
        str: Method output as python function result typing
    """
    outputs = []

    if method.output:
        for arg in method.output:
            outputs.append(format_arg_type(arg))

    if len(outputs) <= 0:
        return "None"

    return f"Tuple[{', '.join(outputs)}]"


def format_method_call_args(method: MethodSchema) -> str:
    """Formats method input arguments to ua call arguments.

    Args:
        method (MethodSchema): Schema of current method

    Returns:
        str: Method input as ua.Variant array
    """
    variants = []

    if method.input:
        for arg in method.input:
            variants.append(format_arg_variant(arg))

    return f'[{", ".join(variants)}]'


def format_arg_name(arg: ArgumentSchema) -> str:
    """Formats argument name to a function arg name.

    Args:
        arg (ArgumentSchema): Schema of current argument

    Returns:
        str: Argument name as function arg name
    """
    return snake_case(arg.name)


def format_arg_type(arg: ArgumentSchema) -> str:
    """Formats argument type to ua.Type.

    Args:
        arg (ArgumentSchema): Schema of current argument

    Returns:
        str: Argument type as ua.Type
    """
    if arg.value_rank == ua.ValueRank.Scalar:
        return f"ua.{arg.type.name}"

    return f"List[ua.{arg.type.name}]"


def format_arg_variant(arg: ArgumentSchema) -> str:
    """Formats argument as ua.Variant.

    Args:
        arg (ArgumentSchema): Schema of current argument

    Returns:
        str: Argument as ua.Variant
    """
    return f"ua.Variant({format_arg_name(arg)}, ua.VariantType.{arg.type.name})"


def snake_case(text: str) -> str:
    """Transforms a string to a snake case.

    Args:
        text (str): Input string

    Returns:
        str: Transformed snake_case string
    """
    return "_".join(sub("([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", text.replace("-", " "))).split()).lower()


def format_doc_string(doc: str) -> List[str]:
    """Splits a string to multiple lines with a max length of 100.

    Args:
        doc (str): A long string

    Returns:
        List[str]: List of formated strings
    """
    lines: List[str] = []

    for line in doc.split("\n"):
        words = iter(line.split())
        current = next(words)
        for word in words:
            if len(current) + 1 + len(word) > 100:
                lines.append(current)
                current = word
            else:
                current += " " + word
        lines.append(current)

    return lines
