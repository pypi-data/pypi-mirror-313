class GraphlinException(Exception):
    """Base class for all Graphlin exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class GraphlinConnectionError(GraphlinException):
    """Raised when Gremlin connection fails."""


class GraphlinValidationError(GraphlinException):
    """Raised when validation of a change fails."""

class GremlinServerInternalError(GraphlinException):
    """Raised when gremlin server fails to commit changes."""

class NodeNotFound(GraphlinException):
    """Raised when a node is not found."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Node with ID {node_id} not found.")


class EdgeNodeNotFound(GraphlinException):
    """Raised when a node is not found."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Cannot create edge to node with ID {node_id} because it does not exist.")


class EdgeAlreadyExists(GraphlinException):
    """Raised when a edge already present in DB."""

    def __init__(self, edge_id: str):
        self.edge_id = edge_id
        super().__init__(f"Cannot create edge with id {edge_id}, it is already present in the graph.")

