from abc import ABC
from abc import abstractmethod

from tecton_core.query.node_interface import NodeRef


class Rewrite(ABC):
    @abstractmethod
    def rewrite(self, node: NodeRef) -> None:
        raise NotImplementedError
