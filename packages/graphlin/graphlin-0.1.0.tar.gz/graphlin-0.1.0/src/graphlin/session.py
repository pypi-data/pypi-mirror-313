import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Type, TypeVar

from graphlin._exceptions import GremlinServerInternalError
from graphlin.changes import Change, CreateEdge, CreateNode, DeleteNode, UpdateNode

if TYPE_CHECKING:
    from graphlin.connection import GremlinGraphConnection
    from graphlin.node import Node

logger = logging.getLogger(__name__)


class AbstractSession(ABC):
    @abstractmethod
    def add(self, node):
        pass

    @abstractmethod
    def merge(self, node):
        pass

    @abstractmethod
    def delete(self, node):
        pass

    @abstractmethod
    def commit(self):
        pass


T = TypeVar("T", bound="Node")


class Session(AbstractSession):
    def __init__(self, conn: "GremlinGraphConnection"):
        self.conn = conn
        self._changes: List[Change] = []
        self._completed_changes: List[Change] = []
        self._entities: Dict[str, "Node"] = {}

    def get(self, cls: Type[T], id_: str) -> T:
        """
        Get an node by ID.
        """
        if id_ in self._entities:
            node = self._entities[id_]
            if not isinstance(node, cls):
                raise ValueError(f"node with ID {id_} is not of type {cls}")
            return node
        db_node = self.conn.get_node_by_id(cls, id_)
        self._entities[id_] = db_node
        # set the session on the node
        db_node._session = self
        return db_node

    def _include(self, node: "Node"):
        """
        Include an node in the session. This will create a new node if the node doesn't have an ID,
        or update the existing node if it does.
        """
        if node.node_id in self._entities and self._entities[node.node_id] is node:
            return
        elif node.node_id in self._entities:
            raise ValueError("Cannot add an node that is already in the session.")
        self._entities[node.node_id] = node
        node._session = self

    def add(self, node: "Node", error_on_exist: bool = True):
        """
        Add an node to the session. This will create a new node if the node doesn't have an ID,
        or update the existing node if it does.
        """
        if node.node_id in self._entities and self._entities[node.node_id] is node:
            return
        elif node.node_id in self._entities:
            raise ValueError("Cannot add an node that is already in the session.")
        change = CreateNode(node, error_on_exist=error_on_exist)
        self._changes.append(change)
        self._include(node)

    def merge(self, node: "Node"):
        """
        Merge changes of an node into the session. If the node doesn't exist in the database,
        it's equivalent to an add.
        """
        # check if the node is already in the session
        if node.node_id in self._entities:
            raise ValueError(
                f"Node ID {node.node_id} already in the session."
                "Please work directly with the session-associated node."
            )
        # Load existing node data from the database
        existing_node_data = self.conn.get_node_by_id(node.__class__, node.get_id())
        if not existing_node_data:
            db_node = node.model_copy()
            self.add(db_node, error_on_exist=False)
            return db_node

        # Include the node in the session
        self._include(existing_node_data)
        # Check for differences and generate UpdateNode changes
        diffs = self._compare_entities(existing_node_data, node)
        self._changes.extend(diffs)
        self._entities[node.node_id] = node
        return existing_node_data

    def add_edge(
        self,
        start_node: "Node",
        end_node: "Node",
        edge_label: str,
        properties: Optional[Dict[str, Any]] = None,
        error_on_exist: bool = True,
    ):
        """
        Add an edge between two entities.
        """
        properties = properties or {}
        change = CreateEdge(start_node, end_node, edge_label, properties, error_on_exist)
        self._changes.append(change)

    def _compare_entities(self, existing_node: "Node", new_node: "Node") -> Sequence[Change]:
        changes = []
        for field, new_value in new_node.model_dump(exclude_unset=True).items():
            old_value = getattr(existing_node, field)
            if old_value != new_value:
                changes.append(UpdateNode(new_node, {field: new_value}))

        return changes

    def update(self, node: "Node"):
        """
        Update an node in the session. This will update the existing node if it exists,
        or raise an error if it doesn't.
        """
        if node.node_id not in self._entities:
            raise ValueError("Cannot update an node that is not in the session")

        change = UpdateNode(node, node.changes)
        self._changes.append(change)
        self._entities[node.node_id] = node

    def delete(self, node: "Node"):
        """
        Mark an node for deletion.
        """
        self._changes.append(DeleteNode(node))
        self._entities[node.node_id] = node

    def commit(self):
        """
        Commit all changes to the database.
        """
        for change in self._changes:
            change.validate(self.conn)
            try:
                change.execute(self.conn)
                self._completed_changes.append(change)
            except GremlinServerInternalError as e:
                logger.exception(f"Error executing change: {change}")
                logger.info("Rolling back changes")
                self.rollback()
                raise GremlinServerInternalError(f"Error executing change: {change}") from e

        self._reset()

    def _reset(self):
        """
        Clear all changes and entities from the session.
        """
        self._changes.clear()
        self._entities.clear()
        self._completed_changes.clear()

    def rollback(self):
        """
        Clear all changes without committing.
        """
        for change in self._completed_changes:
            change.rollback(self.conn)
        self._reset()

    def query(self, cls: Type[T]) -> List[T]:
        """
        Query for entities of a given type.
        """
        return self.conn.query_lambda(lambda g: g.V().hasLabel(cls.__node_label__()).to_list())
