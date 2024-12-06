"""This module contains IndentManager class."""

from __future__ import annotations

from typing import Any


class IdentException(Exception):
    """Exception of IdentManager."""


class IndentManager:
    """Manages indent and indent str output."""

    def __init__(self, indent_with: str) -> None:
        """Initializes the IndentManager.

        Args:
            indent_with (str): Indent string
        """
        self.indent_with: str = indent_with
        self.level: int = 0

    def __str__(self) -> str:
        """Indent string representation.

        Returns:
            str: Indent level as str
        """
        return self.indent_with * self.level

    def __enter__(self: IndentManager) -> IndentManager:
        """With enter handling.

        Returns:
            IndentManager: self
        """
        self.increase()
        return self

    def __exit__(self, *_: Any) -> None:
        """With exit handling."""
        self.decrease()

    def increase(self) -> None:
        """Increases indent level."""
        self.level += 1

    def decrease(self) -> None:
        """Decreases indent level.

        Raises:
            Exception: If ident is below zero
        """
        if self.level == 0:
            raise IdentException("Indent level is zero, dedent not possible")

        self.level -= 1

    def reset(self) -> None:
        """Resets indent level to zero."""
        self.level = 0
