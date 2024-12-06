"""Contains all templating functions."""

from copy import deepcopy
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from voraus_opcua_generator.client_generator_python.utils import escape_keywords, input_typehint, to_module
from voraus_opcua_generator.doc_builder.types import default_value, py_type
from voraus_opcua_generator.doc_builder.utils import escape_rst_special_chars, mixed_to_pascal_case, mixed_to_snake_case

TEMPLATES_DIRECTORY = Path(__file__).parent / "templates"
TEMPLATES_ENVIRONMENT = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False,  # Allowed since we can trust the templates.
)

# custom filters
TEMPLATES_ENVIRONMENT.filters["default_value"] = default_value
TEMPLATES_ENVIRONMENT.filters["escape_keywords"] = escape_keywords
TEMPLATES_ENVIRONMENT.filters["escape_rst_special_chars"] = escape_rst_special_chars
TEMPLATES_ENVIRONMENT.filters["input_typehint"] = input_typehint
TEMPLATES_ENVIRONMENT.filters["pascal_case"] = mixed_to_pascal_case
TEMPLATES_ENVIRONMENT.filters["snake_case"] = mixed_to_snake_case
TEMPLATES_ENVIRONMENT.filters["to_module"] = to_module
TEMPLATES_ENVIRONMENT.filters["py_type"] = py_type

TEMPLATES_ENVIRONMENT_KEEP_NEW_LINES = deepcopy(TEMPLATES_ENVIRONMENT)
TEMPLATES_ENVIRONMENT_KEEP_NEW_LINES.keep_trailing_newline = True

# client builder python
INIT_HEADER_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/_module/__init__.py.j2")
INIT_PACKAGE_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT_KEEP_NEW_LINES.get_template("client_python/__init__.py.j2")
OVERVIEW_INIT_HEADER_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/overview.__init__.py.j2")
OVERVIEW_PY_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/_overview.py.j2")
UTIL_INIT_HEADER_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/util.__init__.py.j2")
UTIL_PY_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/_util.py.j2")
MODULE_INTERNAL_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("client_python/module.py.j2")

# data
DATA_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("data_legacy/data.py.j2")

# doc builder
VARIABLE_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/variable.j2")
NODE_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/node.j2")
METHOD_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/method.j2")
ROOT_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/root_node.j2")
NODE_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/get_node_python.j2")
VARIABLE_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/get_variable_python.j2")
METHOD_PYTHON_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/get_method_python.j2")
OVERVIEW_TEMPLATE = TEMPLATES_ENVIRONMENT.get_template("doc_builder/overview.j2")
