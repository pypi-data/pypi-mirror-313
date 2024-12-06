import logging
import functools
from typing import List
from gevent.queue import Queue

from .label_pipeline import LabelPipeline
from ...node import Node
from ...label import LabelData

logger = logging.getLogger(__name__)


class OrderPipeline(LabelPipeline):
    MAX_IDX = 1_000_000  # Define a maximum value for the index

    def __init__(self, all_nodes: List[Node]):
        super().__init__(all_nodes=all_nodes)
        self.data_idx = 0
        self.idx_queue = Queue()
        self.set_label_function(self.order_index_label_func)
        self.output_dict = {}

    def order_index_label_func(self, data):
        self.data_idx = (self.data_idx + 1) % self.MAX_IDX  # Circular incremen
        self.idx_queue.put(self.data_idx)
        return self.data_idx

    def _order_put_data_decorator(self, put_func):
        @functools.wraps(put_func)
        def _order_put_data_wrapper(label_data):
            assert isinstance(
                label_data, LabelData
            ), f"The data {label_data} is not a LabelData"
            label = self.get_data_func_label(label_data, self.order_index_label_func)
            self.output_dict[label] = label_data

            while not self.idx_queue.empty():
                next_idx = self.idx_queue.queue[0]  # Non-destructive check
                if next_idx in self.output_dict:
                    self.idx_queue.get()  # Remove the item from the queue
                    put_func(self.output_dict.pop(next_idx))
                else:
                    break

        return _order_put_data_wrapper
