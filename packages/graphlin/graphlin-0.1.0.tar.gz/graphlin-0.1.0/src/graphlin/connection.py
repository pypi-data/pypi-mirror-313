import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID
from venv import create

from aiohttp import ClientConnectionError, ServerConnectionError
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.anonymous_traversal import AnonymousTraversalSource, traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T

from graphlin._exceptions import GraphlinConnectionError
from graphlin.changes import CreateNode
from graphlin.configuration import settings
from graphlin.node import Edge
from graphlin.session import Session

if TYPE_CHECKING:
    from graphlin.node import Node
# Initialize logging
logger = logging.getLogger(__name__)

# Constant
EDGE_ID_ERROR_MESSAGE = "Edge with id already"

N = TypeVar("N", bound="Node")
Out = TypeVar("Out")
ID = TypeVar("ID", bound=Union[str, int, UUID])


class AbstractGraphConnection(ABC, Generic[ID]):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def get_node_by_id(self, node_class: Type[N], node_id: ID) -> N:
        pass

    @abstractmethod
    def add_node(self, create_change: CreateNode) -> None:
        pass

    @abstractmethod
    def add_edge(
        self,
        source_id: ID,
        target_id: ID,
        edge_label: str,
        properties: Optional[Dict[str, Any]] = None,
        edge_id: Optional[ID] = None,
    ) -> Any:
        pass

    @abstractmethod
    def update_node_properties(self, node_id: ID, properties: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def delete_node(self, node_id: ID) -> None:
        pass


class GremlinGraphConnection(AbstractGraphConnection[ID]):
    endpoint: str
    port: int
    g: AnonymousTraversalSource
    remote_connection: DriverRemoteConnection

    def __init__(self, endpoint, port):
        self.endpoint = endpoint
        self.port = port

    def session(self) -> Session:
        return Session(self)

    def test_connection(self):
        try:
            self.g.V().limit(1).to_list()
        except (ClientConnectionError, ServerConnectionError):
            raise GraphlinConnectionError(f"Could not connect to {self.endpoint}:{self.port}")
        return True

    def query_lambda(self, query: Callable[[AnonymousTraversalSource], Out]) -> Out:
        return query(self.g)

    def clear(self):
        self.g.V().drop().iterate()

    def close(self):
        self._disconnect()

    # Create methods
    def add_node(self, create_change: CreateNode) -> None:
        if create_change.error_on_exist and self.g.V().has_id(create_change.node_id).has_next():
            raise ValueError(f"Node with ID {create_change.node_id} already exist")
        labels = (
            [create_change.node_label, *create_change.extra_labels]
            if settings.MULTIPLE_LABELS
            else [create_change.node_label]
        )
        try:
            vertex = self.g.add_v("::".join(labels)).property(T.id, create_change.node_id)
            for key, value in create_change.properties.items():
                vertex = vertex.property(key, value)
            return vertex.next()
        except GremlinServerError as exc:
            if "Vertex with id already exists" not in exc.status_message or create_change.error_on_exist:
                raise exc

    def add_edge(
        self,
        source_id: ID,
        target_id: ID,
        edge_label: str,
        properties: Optional[Dict[str, Any]] = None,
        error_on_exist: bool = True,
        edge_id: Optional[ID] = None,
    ) -> Any:
        properties = properties or {}
        edge_id = edge_id or f"{source_id}-{edge_label}-{target_id}"
        try:
            edge = self.g.V(source_id).add_e(edge_label).to(__.V(target_id)).property(T.id, edge_id)
            for key, value in properties.items():
                edge = edge.property(key, value)
            return edge.next()
        except GremlinServerError as exc:
            if EDGE_ID_ERROR_MESSAGE not in exc.status_message or error_on_exist:
                raise exc

    def update_node_properties(self, node_id: ID, properties: Dict[str, Any]) -> Any:
        node = self.g.V(node_id)
        for key, value in properties.items():
            node = node.property(key, value)
        return node.next()

    def delete_node(self, node_id: ID) -> None:
        self.g.V(node_id).drop().iterate()

    # Read methods
    def get_node_by_id(self, node_class: Type[N], node_id: ID) -> Optional[N]:
        output = self.g.V(node_id).value_map(True).limit(1).to_list()
        if not output:
            return None
        properties = {key: value[0] for key, value in output[0].items() if isinstance(key, str)}
        return node_class(**properties)

    def get_edge(self, edge_id: ID) -> Edge | None:
        if not self.g.E(edge_id).has_next():
            return None

        return self.g.E(edge_id).value_map(True).limit(1).to_list()

    def update_edge_properties(self, edge_id: str, properties: Dict[str, Any]) -> Any:
        edge = self.g.E(edge_id)
        for key, value in properties.items():
            edge = edge.property(key, value)
        return edge.next()

    def delete_edge(self, edge_id: str) -> None:
        self.g.E(edge_id).drop().iterate()

    # connection methods
    def _connect(self):
        self.remote_connection = DriverRemoteConnection(f"{self.endpoint}:{self.port}/gremlin", "g")
        self.g = traversal().with_remote(self.remote_connection)

    def _disconnect(self):
        if self.remote_connection:
            try:
                self.remote_connection.close()
            except Exception:
                raise GraphlinConnectionError("Could not close connection.")
            self.remote_connection = None
            self.g = None

    # context manager methods
    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._disconnect()
