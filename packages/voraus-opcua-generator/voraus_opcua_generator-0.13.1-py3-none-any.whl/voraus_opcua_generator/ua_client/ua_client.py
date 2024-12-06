"""This module contains a ua client wrapper."""

from __future__ import annotations

from typing import Any, List, Union

from asyncua.sync import Client, SyncNode, ua


class UaClient:
    """Wraps the asyncua client."""

    def __init__(self, url: str) -> None:
        """Initializes a Client.

        Args:
            url (str): url to server
        """
        self._client = Client(url)

    def connect(self) -> None:
        """Connects to server."""
        self._client.connect()

    def disconnect(self) -> None:
        """Disconnects from server."""
        self._client.disconnect()

    def get_node(self, nodeid: ua.NodeId) -> UaNode:
        """Return a variable node.

        Args:
            nodeid (ua.NodeId): Node Id of wanted variable

        Returns:
            VariableNode: variable node found
        """
        return self._client.get_node(nodeid)

    def read_values(self, nodeids: List[ua.NodeId]) -> List[ua.Variant]:
        """Reads multiple variable values.

        Args:
            nodeids (List[ua.NodeId]): _description_

        Returns:
            List[ua.Variant]: _description_
        """
        nodes = [self._client.get_node(nodeid) for nodeid in nodeids]
        return self._client.read_values(nodes)

    def call(
        self, object_id: ua.NodeId, method_id: ua.NodeId, arguments: List[ua.Variant]
    ) -> Union[None, Any, List[Any]]:
        """Calls an ua method.

        Args:
            object_id (ua.NodeId): Parent object identifier
            method_id (ua.NodeId): Method identifier
            arguments (List[ua.Variant]): Call arguments

        Returns:
            Union[None, Any, List[Any]]: None if no return values.
                Any if one return value. List[Any] if many return values.
        """
        return self._client.get_node(object_id).call_method(method_id, *arguments)


class UaNode:
    """SyncNode Wrapper."""

    def __init__(self, client: UaClient, nodeid: ua.NodeId):
        """Initializes UaNode with SyncNode.

        Args:
            client (UaClient): OPC UA Client
            nodeid (ua.NodeId): Target NodeId
        """
        self._node = SyncNode(client._client.tloop, client._client.aio_obj.get_node(nodeid))

    @property
    def nodeid(self) -> ua.NodeId:
        """Get nodeid of variable.

        Returns:
            ua.NodeId: Variables NodeId
        """
        return self._node.nodeid

    def read_value(self) -> Any:
        """Read variables value.

        Returns:
            Any: Variables value
        """
        return self._node.read_value()
