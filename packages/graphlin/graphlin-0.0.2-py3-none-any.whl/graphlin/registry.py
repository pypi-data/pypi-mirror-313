from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Optional, Type

if TYPE_CHECKING:
    from graphlin.node import Node


class AbstractRegistry(ABC):
    @abstractmethod
    def add(self, node):
        pass

    @abstractmethod
    def remove(self, node):
        pass

    @abstractmethod
    def get(self, label: str) -> Optional[Type["Node"]]:
        pass


class Registry(AbstractRegistry):
    _registry: Dict[str, Type["Node"]]

    def __init__(self):
        self._registry = {}

    def add(self, node_cls: Type["Node"]):
        for label in node_cls.__full_labels__():
            if label in self._registry:
                raise ValueError(f"Label {label} already registered")
            self._registry[label] = node_cls

    def remove(self, node: "Node"):
        for label in node.full_labels:
            self._registry.pop(label)

    def get(self, label: str) -> Optional[Type["Node"]]:
        return self._registry.get(label)


default_registry = Registry()
