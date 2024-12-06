"""Contains utilities for the OPC UA python client builder."""

from __future__ import annotations

import builtins
from keyword import iskeyword
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from voraus_opcua_generator.doc_builder.argument import Argument
    from voraus_opcua_generator.doc_builder.node import Node


def escape_keywords(input_word: str) -> str:
    """Escape input by appending an underscore in case it matches one of pythons keywords or builtins.

    Args:
        input_word: The string to escape.

    Returns:
        The escaped string, like "yield_".
    """
    if iskeyword(input_word) or input_word in dir(builtins):
        return f"{input_word}_"
    return input_word


def input_typehint(arguments: list[Argument], optional: bool = True) -> str:
    """Format a list of arguments as input typehint.

    Escape arguments called like python keywords.

    Args:
        arguments: A list of arguments to format.
        optional: Whether all arguments should be marked as optional.
                  This is useful upon generation of callback functions,
                  which do not necessarily consume all available arguments.

    Returns:
        The typehint as string
    """
    if len(arguments) == 0:
        return ""
    res = []
    for argument in arguments:
        res.append(f", {escape_keywords(argument.name_snake_case)}: {argument.py_type}{' | None' if optional else ''}")
    return "".join(res)


def to_module(node_list: list[Node]) -> str:
    """Format a list of nodes as a module string.

    Args:
        node_list: A hierarchically ordered list to be represented in dot notation.

    Returns:
        The module path
    """
    return ".".join([node.displayname_snake_case for node in node_list])
