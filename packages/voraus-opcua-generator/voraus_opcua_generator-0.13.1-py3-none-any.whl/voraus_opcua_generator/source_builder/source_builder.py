"""This module contains the SourceBuilder class."""

from contextlib import contextmanager
from io import StringIO
from typing import Generator

from voraus_opcua_generator.source_builder.indent_manager import IndentManager


class SourceBuilder:
    """SourceBuilder is a helper class to create block based code."""

    def __init__(self) -> None:
        """Initializes the SourceBuilder."""
        self._out = StringIO()
        self.indent = IndentManager(" " * 4)

    def writeln(self, code: str = "") -> None:
        """Write a line.

        Args:
            code (str, optional): Code to write to the line. Defaults to "".
        """
        if code:
            self._out.write(str(self.indent))
            self._out.write(code)
        self._out.write("\n")

    def write_lines(self, lines: list[str]) -> None:
        """Write several lines.

        Args:
            lines (list[str]): Lines to append to the SourceBuilders code.
        """
        for line in lines:
            self.writeln(line)

    def get_value(self) -> str:
        """Get current value from buffer.

        Returns:
            str: Written source code
        """
        return self._out.getvalue()

    @contextmanager
    def block(self, code: str) -> Generator[None, None, None]:
        """Write a block using "with" statement.

        Increases the ident level on enter and decreases on exit.

        Args:
            code (str): Block code before ident is increased

        Yields:
            Generator[None, None, None]: Ident block
        """
        self.writeln(code)
        with self.indent:
            yield
