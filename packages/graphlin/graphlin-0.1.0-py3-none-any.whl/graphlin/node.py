from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Set

from pydantic import BaseModel

from graphlin.registry import Registry, default_registry
from graphlin.session import Session
from graphlin.utilities import hash_node

if TYPE_CHECKING:
    pass
_PROTECTED_FIELDS = {"_changes", "_original_data", "_session"}


class TrackableModel(BaseModel):
    def __init__(self, **data: Dict[str, Any]):
        super().__init__(**data)
        self._original_data = self.model_dump()
        self._changes: Dict[str, Any] = {}
        self._session: Optional[Session] = None

    @classmethod
    def __node_label__(cls):
        return getattr(cls, "__label__", cls.__name__)

    @classmethod
    def __full_labels__(cls):
        labels = getattr(cls, "__extra_labels__", [])
        labels.append(cls.__node_label__())
        return labels

    def __setattr__(self, name: str, value: Any) -> None:
        # Override the default __setattr__ to track changes
        super().__setattr__(name, value)

        if name not in _PROTECTED_FIELDS and hasattr(self, "_original_data"):
            original_value = self._original_data.get(name)
            if original_value != value:
                self._changes[name] = value

    @property
    def changes(self) -> Dict[str, Any]:
        return self._changes

    def reset_changes(self):
        self._original_data = self.model_dump()
        self._changes = {}

    def has_changes(self) -> bool:
        return bool(self._changes)


class Node(TrackableModel):
    __hash_fields__: ClassVar[Set[str]] = set()

    def __init_subclass__(cls, registry: Optional["Registry"] = None, **kwargs: Any):
        registry = registry or default_registry
        registry.add(cls)
        return super().__init_subclass__()

    def get_id(self) -> str:
        return f"{self.__node_label__()}:{self._id_value}"

    @property
    def _id_value(self) -> str:
        return f"{hash_node(self)}"

    def __hash__(self):
        return hash(self.get_id())

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__hash_fields__:
            raise ValueError(f"Cannot change field {name} on {self.__class__.__name__}")
        output = super().__setattr__(name, value)
        if getattr(self, "_session", None) is not None and name not in (
            "_changes",
            "_original_data",
            "_session",
        ):
            assert self._session is not None
            self._session.update(self)

        return output

    def add_edge(
        self,
        target: "Node",
        edge_label: str,
        properties: Optional[Dict[str, Any]] = None,
        reverse: bool = False,
        error_on_exist: bool = True
    ) -> "Edge":

        # ensure that both the source and target have been added to a session
        if self._session is None:
            raise ValueError("node must be added to a session before adding edges")
        if target._session is None:
            raise ValueError("The target node must be added to a session before adding edges.")
        properties = properties or {}
        if reverse:
            return self._session.add_edge(
                target.node_id,
                self.node_id,
                edge_label,
                properties,
                error_on_exist
            )
        self._session.add_edge(
            self.node_id,
            target.node_id,
            edge_label,
            properties,
            error_on_exist
        )
        return Edge(source=self, target=target, edge_label=edge_label, properties=properties)

    @property
    def full_labels(self):
        labels = getattr(self, "__extra_labels__", [])
        labels.append(self.__node_label__())
        return labels

    @property
    def node_id(self):
        return self.get_id()

    def _properties(self):
        return self.model_dump(exclude_unset=True, exclude_defaults=True, exclude={"source"})


Node.model_rebuild()


class Edge(BaseModel):
    source: Node
    target: Node
    edge_label: str
    properties: Dict[str, Any]
