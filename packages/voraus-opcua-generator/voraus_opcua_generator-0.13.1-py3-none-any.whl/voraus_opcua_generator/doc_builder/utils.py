"""Contains utilities for the OPC UA documentation builder."""

import re
from pathlib import Path

NODE_ID_NAMESPACE_REGEX = re.compile(r"ns=(\d+);i=(\d+)")
NODE_ID_REGEX = re.compile(r"i=(\d+)")
WORD_BOUND_REGEX = re.compile(r"\d+|[a-zA-Z][^A-Z \d]*")


def escape_rst_special_chars(text: str) -> str:
    """Escapes the "_" or newline special chars in the rst file.

    Args:
        text: RST File

    Returns:
        :Rst with escaped special chars
    """
    return text.replace("_", " ")


def split_mixed_case_words(text: str) -> list[str]:
    """Convert mixed case words in a text into a list of them.

    Retain acronyms as words. Treat numbers as words.

    Args:
        text: The string to split.

    Returns:
        A list of words contained in the provided text name.
        The first word is guaranteed to be rather empty instead of a number.
    """
    words: list[str] = re.findall(WORD_BOUND_REGEX, str(text))

    acc = ""
    output_words = []

    if len(words) >= 1:
        first_word = words[0]
        if first_word[0].isdigit():
            output_words.append("")

    for input_word in words:
        if len(input_word) == 1 and not input_word.isdigit():
            acc += input_word
        else:
            if len(acc) != 0:
                output_words.append(acc)
                acc = ""
            output_words.append(input_word)
    if len(acc) != 0:
        output_words.append(acc)
    return output_words


def mixed_to_pascal_case(text: str) -> str:
    """Convert the mixed cased object names to PascalCase.

    Args:
        text: The text to format.

    Returns:
        Text in PascalCase.
    """
    output_words = split_mixed_case_words(text)

    return "".join(word.capitalize() if word != word.upper() else word for word in output_words)


def mixed_to_snake_case(text: str) -> str:
    """Converts the mixed cased argument names to snake case.

    Args:
        text: The text to format.

    Returns:
        Text in snake_case.
    """
    output_words = split_mixed_case_words(text)

    return "_".join(word.lower() for word in output_words)


def check_gitignore(rst_dir: Path, gitignore_file: Path) -> None:
    """Initializes the gitignore.

    Args:
        rst_dir : Directory of the rst file.
        gitignore_file : Path of the gitignore file.

    Raises:
        KeyError: Raises KeyError if the gitignore_entry is not included in the gitignore file.
    """
    if gitignore_file.is_file():
        with open(gitignore_file, "r", encoding="utf-8") as file:
            gitignore_content = file.read()

        gitignore_entry = f"{rst_dir.relative_to(Path.cwd()) if rst_dir.is_absolute() else rst_dir}/"
        if gitignore_entry not in gitignore_content:
            raise KeyError(f"You must ignore '{gitignore_entry}' in your .gitignore file.")


def check_index_content(doc_dir: Path, rst_file_prefix: str) -> None:
    """Checks if the name of the created rst file is included in the index.rst.

    Args:
        doc_dir : Directory of the documentation.
        rst_file_prefix : Name of the xml file. Used to name the rst file.

    Raises:
        KeyError: Raises a KeyError if the rst toc (table of contents) entry is missing in the index file.
    """
    rst_index_file = doc_dir / "index.rst"
    with open(rst_index_file, "r", encoding="utf-8") as file:
        index_content = file.read()

    rst_toc_entry = f"{rst_file_prefix}/{rst_file_prefix}"
    if rst_toc_entry not in index_content:
        raise KeyError(f"RST toc (table of contents) entry '{rst_toc_entry}' is missing in '{rst_index_file}'.")
