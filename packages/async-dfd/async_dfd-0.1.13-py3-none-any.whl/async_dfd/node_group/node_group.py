import logging
from abc import ABC, abstractmethod

import gevent
from gevent import spawn
from ..node.abstract_node import AbstractNode

logger = logging.getLogger(__name__)


class NodeGroup(AbstractNode, ABC):
    def __init__(self, all_nodes):
        super().__init__()
        assert len(all_nodes) != 0, f"No node to compose the node group {self.__name__}"
        self.all_nodes = {node.__name__: node for node in all_nodes}
        self._connect_nodes()

    @abstractmethod
    def _connect_nodes(self):
        logger.error(
            f"Not implemented the self._connect_nodes method in {self.__name__}"
        )

    def start(self):
        if self.serial_number is None:
            self.serial_number = [0]
        for i, node in enumerate(self.all_nodes.values()):
            node.set_serial_number(self.serial_number + [i])
            node.start()
        self.is_start = True
        return

    def end(self):
        self.is_start = False
        end_tasks = []
        for node in self.all_nodes.values():
            end_tasks.append(spawn(node.end))
        gevent.joinall(end_tasks)
