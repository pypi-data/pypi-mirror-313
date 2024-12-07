import json
from hashlib import md5
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphlin.node import Node


def hash_json(data):
    return md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


def hash_node(node: "Node"):
    return hash_json(node.model_dump(mode="json", include=node.__hash_fields__))
