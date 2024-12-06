"""Contains an argument class, which contains the input and output arguments of OPC UA methods."""

from asyncua.common.xmlparser import ExtObj

from voraus_opcua_generator.doc_builder.types import UA_PY_TYPES
from voraus_opcua_generator.doc_builder.utils import escape_rst_special_chars, mixed_to_snake_case


class Argument:
    """Handles the arguments of OPC UA method nodes."""

    def __init__(self, content: ExtObj) -> None:
        """Initializes an argument.

        Args:
            content : An argument in form of a string.
        """
        self._content = content
        self._body = dict(self._content.body)
        self._argument = dict(self._body["Argument"])
        self._value_rank = int(self._argument["ValueRank"])
        try:
            self._array_dimensions = int(dict(self._argument["ArrayDimensions"])["UInt32"])
        except KeyError:
            pass
        self._datatype = dict(self._argument["DataType"])
        self._description = dict(self._argument["Description"])

        self.name = self._argument["Name"]
        self.name_snake_case = mixed_to_snake_case(self.name).replace(" ", "")
        self.identifier = self._datatype["Identifier"]
        self.text = self._description["Text"]
        self.ua_text = escape_rst_special_chars(self.text)
        self.ua_type, self._py_type = UA_PY_TYPES[self.identifier]

    @property
    def py_type(self) -> str:
        """Provide a python type, while taking into account whether it is one value or an array of them.

        If the length is fixed, it's represented as a tuple; if not, as a list.

        Returns:
            A string in the form of a python typehint describing the given type.
        """
        if hasattr(self, "_array_dimensions"):
            length = self._array_dimensions
            return f"tuple[{', '.join(length*[self._py_type])}]"
        if self._value_rank > 0:
            return f"list[{self._py_type}]"
        return self._py_type
