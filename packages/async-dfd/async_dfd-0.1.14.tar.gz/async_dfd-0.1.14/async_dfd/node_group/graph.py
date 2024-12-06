import logging
from collections import deque, defaultdict

from .node_group import NodeGroup

logger = logging.getLogger(__name__)


class Graph(NodeGroup):
    def start(self):
        self.all_nodes = self.topological_sort(self.all_nodes)
        super().start()
        self.heads = {}
        self.tails = {}

    @property
    def src_nodes(self):
        src_nodes = {}
        for node in self.heads.values():
            src_nodes.update(node.src_nodes)
        return src_nodes

    @property
    def dst_nodes(self):
        dst_nodes = {}
        for node in self.tails.values():
            dst_nodes.update(node.dst_nodes)
        return dst_nodes
    
    @property
    def head(self):
        raise NotImplementedError("Graph has multiple heads, use heads instead")
    
    @property
    def tail(self):
        raise NotImplementedError("Graph has multiple tails, use tails instead")
        

    def topological_sort(self, all_nodes):
        in_degree = defaultdict(int)
        descriptions = {}
        for desc, node in all_nodes:
            descriptions[node] = desc
            for neighbor in node.dst_nodes:
                in_degree[neighbor] += 1

        queue = deque([node for node in all_nodes.values() if in_degree[node] == 0])
        sorted_nodes = {}

        while queue:
            node = queue.popleft()
            sorted_nodes[descriptions[node]] = node
            for neighbor in node.get_neighbors():
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_nodes) != len(all_nodes):
            raise ValueError("Graph has at least one cycle")

        return sorted_nodes
