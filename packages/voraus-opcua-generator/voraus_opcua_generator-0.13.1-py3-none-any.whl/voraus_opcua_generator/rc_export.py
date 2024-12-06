"""RobotControl nodeset exported."""

from typing import List

from asyncua import ua

from voraus_opcua_generator.generator import generate_code
from voraus_opcua_generator.parser.nodeset_parser import NodesetParser
from voraus_opcua_generator.schema import OverrideOptions


def robot_control() -> None:
    """Defines nodes to export."""
    # setup parser
    schema_parser = NodesetParser("motion_nodes.xml")  # or ClientParser("opc.tcp://<ip>:<port>")

    target_nodes = [
        # variables
        ua.NodeId(100000, 1),  # Robot
        ua.NodeId(100001, 1),  # Axes
        ua.NodeId(100730, 1),  # ImpedanceControlState
        ua.NodeId(100006, 1),  # Interpolator
        ua.NodeId(200000, 1),  # MSC
        ua.NodeId(205000, 1),  # FBIOutputs
        ua.NodeId(202000, 1),  # MSCStatus
        ua.NodeId(100009, 1),  # TCP
        ua.NodeId(100004, 1),  # Tool
        ua.NodeId(100900, 1),  # System
        # methods
        ua.NodeId(100210, 1),  # Motion
        ua.NodeId(100240, 1),  # Control
        ua.NodeId(100280, 1),  # Tool
        ua.NodeId(100182, 1),  # Impedance Control
    ]
    # parse schema
    schema = schema_parser.parse(target_nodes)

    # set override options
    override_options: List[OverrideOptions] = [
        OverrideOptions(
            node_id=ua.NodeId.from_string("ns=1;i=100247"),
            name="resume_command",
        ),
        OverrideOptions(
            node_id=ua.NodeId.from_string("ns=1;i=100280"),
            name="ToolFunctions",
        ),
        OverrideOptions(
            node_id=ua.NodeId.from_string("ns=1;i=100004"),
            name="ToolVariables",
        ),
        OverrideOptions(
            node_id=ua.NodeId.from_string("ns=1;i=202014"),
            name="robot_power_48v_switched_on",
        ),
    ]

    code = generate_code(schema, override_options)
    with open("generated_robot_control_client.py", "w", encoding="utf-8") as file:
        file.write(code)


if __name__ == "__main__":
    robot_control()
