from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

from graphlin._exceptions import EdgeAlreadyExists, EdgeNodeNotFound

if TYPE_CHECKING:
    from graphlin.connection import GremlinGraphConnection
    from graphlin.node import Node


class Change(ABC):
    def __init__(self, node: "Node"):
        pass

    @abstractmethod
    def execute(self, conn: "GremlinGraphConnection"):
        pass

    def validate(self, conn: "GremlinGraphConnection"):
        pass

    def rollback(self, conn: "GremlinGraphConnection"):
        pass


class CreateNode(Change):
    def __init__(self, node: "Node", error_on_exist: bool = True):
        self.node_label = node.__node_label__()
        self.node_id = node.get_id()
        self.properties = node.model_dump()
        self.extra_labels = getattr(node, "__extra_labels__", [])
        self.error_on_exist = error_on_exist

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.node_label}({self.node_id}) {self.properties}>"

    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.add_node(self)

    def rollback(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.delete_node(self.node_id)


class UpdateNode(Change):
    def __init__(self, node: "Node", fields_to_update: Dict[str, Any]):
        self.node = node
        self.fields_to_update = fields_to_update

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.node.__class__.__name__}({self.node.node_id}) {self.fields_to_update}>"

    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.update_node_properties(self.node.node_id, self.fields_to_update)


class DeleteNode(Change):
    def __init__(self, node: "Node"):
        self.node_id = node.node_id

    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.delete_node(self.node_id)


class CreateEdge(Change):
    def __init__(
        self,
        start_node: "Node",
        end_node: "Node",
        edge_label: str,
        properties: Optional[Dict[str, Any]] = None,
        error_on_exist: bool = True,
    ):
        self.start_node = start_node
        self.end_node = end_node
        self.edge_label = edge_label
        self.properties = properties or {}
        self.error_on_exist = error_on_exist

    def validate(self, conn: "GremlinGraphConnection"):
        for node_id in (self.start_node, self.end_node):
            if not conn.g.V(node_id).has_next():
                raise EdgeNodeNotFound(node_id.get_id())
        # ensure edge does not already exist
        # TODO: this should be extracted into a utility function
        if self.error_on_exist:
            source_id = self.start_node
            target_id = self.end_node
            edge_id = f"{source_id}-{self.edge_label}-{target_id}"
            existing_edge = conn.g.E(edge_id).to_list()
            if existing_edge:
                raise EdgeAlreadyExists(edge_id)

    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.add_edge(self.start_node, self.end_node, self.edge_label, self.properties, self.error_on_exist)


class UpdateEdge(CreateEdge):
    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.update_edge_properties(self.start_node, self.end_node, self.edge_label, self.properties)


class DeleteEdge(CreateEdge):
    def execute(self, conn: "GremlinGraphConnection"):
        # Use conn: 'GremlinGraphConnection''s methods to execute the specific Gremlin command.
        conn.delete_edge(self.start_node, self.end_node, self.edge_label)
