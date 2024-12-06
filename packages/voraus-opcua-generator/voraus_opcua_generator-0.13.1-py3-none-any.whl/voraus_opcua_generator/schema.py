"""A definition of related data schemas."""

from dataclasses import dataclass
from typing import List, Optional

from asyncua import ua


@dataclass
class NodeSchema:
    """Basic schema of a node."""

    name: str
    description: str
    node_id: ua.NodeId


@dataclass
class VariableSchema(NodeSchema):
    """Variable Schema."""

    type: ua.VariantType
    value_rank: ua.ValueRank
    dimensions: Optional[List[ua.Int32]] = None


@dataclass
class ArgumentSchema:
    """Argument Schema."""

    name: str
    description: str
    type: ua.VariantType
    value_rank: ua.ValueRank
    dimensions: Optional[List[ua.Int32]] = None


@dataclass
class MethodSchema(NodeSchema):
    """Method Schema."""

    input: List[ArgumentSchema]
    output: List[ArgumentSchema]


@dataclass
class ObjectSchema(NodeSchema):
    """Object Schema."""

    variables: List[VariableSchema]
    methods: List[MethodSchema]


@dataclass
class ClientDescription:
    """Root description object."""

    name: str
    objects: List[ObjectSchema]


@dataclass
class OverrideOptions:
    """Override options."""

    node_id: ua.NodeId
    name: str
