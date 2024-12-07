from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from gremlin_python.process.graph_traversal import GraphTraversalSource

    from graphlin.connection import GremlinGraphConnection


def serialize_vertex_command(command: dict, conn: "GremlinGraphConnection"):
    conn.g = cast("GraphTraversalSource", conn.g)
    vertex = conn.g.addV(command["label"])
    for key, value in command["properties"].items():
        vertex = vertex.property(key, value)
    return vertex


def serialize_edge_command(command: dict, conn: "GremlinGraphConnection"):
    conn.g = cast("GraphTraversalSource", conn.g)
    edge = conn.g.add_e(command["label"]).from_(conn.g.V(command["from"])).to(conn.g.V(command["to"]))
    return edge
