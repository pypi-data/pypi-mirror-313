#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module defines the cli entry points."""


import typer
from voraus_logging_lib.logging import LogLevel, configure_logger

import voraus_opcua_generator
from voraus_opcua_generator.cli.data_legacy_builder import build_data_legacy
from voraus_opcua_generator.cli.doc_builder import build_docs
from voraus_opcua_generator.cli.py_client_builder import build_client_package
from voraus_opcua_generator.cli.xml_builder import build_xml

app = typer.Typer()
app.command()(build_data_legacy)
app.command()(build_docs)
app.command()(build_client_package)
app.command()(build_xml)


def print_version(do_print: bool) -> None:
    """Prints the version of the package.

    Args:
        do_print: If the version shall be printed.

    Raises:
        typer.Exit: After the version was printed.
    """
    if do_print:
        print(voraus_opcua_generator.__version__)
        raise typer.Exit()


@app.callback()
def _common(
    _version: bool = typer.Option(
        False,
        "--version",
        callback=print_version,
        is_eager=True,
        help="Print the installed version of the package.",
    ),
    log_level: LogLevel = typer.Option(LogLevel.INFO, help="The log level."),
) -> None:
    """Callback structure for common typer options."""
    configure_logger(log_level=log_level)


if __name__ == "__main__":
    app()
