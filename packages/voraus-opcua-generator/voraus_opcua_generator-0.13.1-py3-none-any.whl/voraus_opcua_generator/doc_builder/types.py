"""Contains UA Python type mappings."""

from __future__ import annotations

from warnings import warn

from asyncua import ua

# The OPC UA node ids are used.
# For more information check: https://reference.opcfoundation.org/Core/Part6/v104/docs/5.1.2
UA_PY_TYPES: dict[str, tuple[str, str]] = {
    f"i={ua.VariantType.Boolean.value}": (ua.VariantType.Boolean.name, "bool"),
    f"i={ua.VariantType.SByte.value}": (ua.VariantType.SByte.name, "int"),
    f"i={ua.VariantType.Byte.value}": (ua.VariantType.Byte.name, "int"),
    f"i={ua.VariantType.Int16.value}": (ua.VariantType.Int16.name, "int"),
    f"i={ua.VariantType.UInt16.value}": (ua.VariantType.UInt16.name, "int"),
    f"i={ua.VariantType.Int32.value}": (ua.VariantType.Int32.name, "int"),
    f"i={ua.VariantType.UInt32.value}": (ua.VariantType.UInt32.name, "int"),
    f"i={ua.VariantType.Int64.value}": (ua.VariantType.Int64.name, "int"),
    f"i={ua.VariantType.UInt64.value}": (ua.VariantType.UInt64.name, "int"),
    f"i={ua.VariantType.Float.value}": (ua.VariantType.Float.name, "float"),
    f"i={ua.VariantType.Double.value}": (ua.VariantType.Double.name, "float"),
    f"i={ua.VariantType.String.value}": (ua.VariantType.String.name, "str"),
    f"i={ua.VariantType.DateTime.value}": (ua.VariantType.DateTime.name, "str"),
}

PY_DEFAULT_VALUES: dict[str, str] = {
    "bool": str(False),
    "int": str(0),
    "float": str(0.0),
    "str": '""',
}


def default_value(py_typehint: str) -> str:
    """Provide a string of a near-zero default value for a given python typehint in its string representation.

    Args:
        py_typehint: A Python typehint in string representation

    Return:
        A string of the near-zero default value.

    Raises:
        NotImplementedError: If a (yet) unsupported typehint is encountered.
    """
    if py_typehint.startswith("list["):
        return "[]"
    try:
        return PY_DEFAULT_VALUES[py_typehint]
    except KeyError as exc:
        raise NotImplementedError(f"{py_typehint} has no assigned `default_value()`.") from exc


def py_type(variant_type: str | None) -> str:
    """For a given ua.VariantTypes name provide a python typehint, that represents it.

    Args:
        variant_type: The name of the ua.VariantType

    Return:
        A typehint matching the provided ua.VariantType description.

    Raises:
        NotImplementedError: If a (yet) unsupported VariantType description is encountered.
    """
    if variant_type is None:
        warn("RR-122, affected by invalid py_type output")
        return "set[set[set]]"
    for known_relation in UA_PY_TYPES.values():
        if variant_type == known_relation[0]:
            return known_relation[1]
    if variant_type.startswith("ListOf"):
        return f"list[{py_type(variant_type[6:])}]"
    raise NotImplementedError(f"{variant_type} can not be translated to python by `py_type()`")
