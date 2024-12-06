import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Union
from uuid import UUID

from graphlin.connection import GremlinGraphConnection

if TYPE_CHECKING:
    from graphlin.node import Node
# Initialize logging
logger = logging.getLogger(__name__)


N = TypeVar("N", bound="Node")
ID = TypeVar("ID", bound=Union[str, int, UUID])


class AbstractGraphEngine(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def test_connection(self):
        pass


class GraphEngine(AbstractGraphEngine):
    def __init__(self, endpoint: str, port: int, echo: bool = True):
        self.endpoint = endpoint
        self.port = port
        self.echo = echo
        self._logger = logger
        if self.echo:
            self._logger.setLevel(logging.DEBUG)

    def connect(self):
        return GremlinGraphConnection(self.endpoint, self.port)

    def clear(self):
        self._logger.info("Clearing graph")
        with self.connect() as conn:
            conn.clear()

        with self.connect() as conn:
            assert not conn.g.V().has_next()

    def test_connection(self):
        with self.connect() as conn:
            conn.test_connection()
