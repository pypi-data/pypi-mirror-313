import logging
import functools
import itertools
from typing import List, Iterable
from gevent.lock import Semaphore
from copy import deepcopy
from .label_pipeline import LabelPipeline
from ...node import Node
from ...label import generate_label, LabelData

logger = logging.getLogger(__name__)


class IterablePipeline(LabelPipeline):
    class ProcessingTask:
        def __init__(self, data):
            assert isinstance(data, Iterable), f"The data {data} is not an iterable"
            self.index = 0
            self.over_results = {}
            self.original_data = data
            self._iter = deepcopy(data)
            next(
                self._iter
            )  # if they are the same, it will not raise StopIteration, should be shortened
            self.is_generator_exhausted = False
            self.task_label = generate_label(self.original_data)

        def get_label(self, data: tuple):
            try:
                next(self._iter)
            except StopIteration:
                self.is_generator_exhausted = True
            finally:
                index = self.index
                self.index += 1
                self.over_results[index] = None
                return (self.task_label, index)

    def __init__(self, all_nodes: List[Node], is_refresh_iter_data: bool = False):
        super().__init__(all_nodes=all_nodes)
        self.is_refresh_iter_data = is_refresh_iter_data
        self.processing_tasks = {}
        self.head.add_get_decorator(self._iterable_get_data_decorator)
        self.tail.add_put_decorator(self._iterable_put_data_decorator)
        self.head.is_data_iterable = True
        self.set_label_function(self.get_label)
        self.ppl_put_func = None

    def get_label(self, data_point, data_gen):
        task = self.processing_tasks[generate_label(data_gen)]
        label = task.get_label(data_point)
        return label

    def _iterable_get_data_decorator(self, get_func):
        @functools.wraps(get_func)
        def _iterable_get_data_wrapper(iter_data):
            if self.is_refresh_iter_data:
                iter_data = iter(iter_data)
            try:
                new_tasks = self.ProcessingTask(iter_data)
                self.processing_tasks[new_tasks.task_label] = new_tasks
            except StopIteration:  # no data
                task_label = "No Iterable Data"
                data = LabelData((iter_data, {}), task_label)
                self.ppl_put_func(data)
                try:
                    del self.processing_tasks[task_label]
                except KeyError:
                    pass
            ret = get_func(iter_data)
            return ret

        return _iterable_get_data_wrapper

    def _iterable_put_data_decorator(self, put_func):

        @functools.wraps(put_func)
        def _iterable_put_data_wrapper(label_data):
            assert isinstance(
                label_data, LabelData
            ), f"The data {label_data} is not a LabelData"
            content = label_data.data
            label = label_data.label
            label = self.get_data_func_label(label_data, self.get_label)

            # put data to the right place
            task = self.processing_tasks[label[0]]
            task.over_results[label[1]] = content

            # check if all results ready
            if task.is_generator_exhausted and all(
                [v is not None for v in task.over_results.values()]
            ):
                over_results = list(task.over_results.values())
                data = LabelData(
                    (deepcopy(task.original_data), deepcopy(over_results)), label[0]
                )
                put_func(data)
                del self.processing_tasks[label[0]]

        self.ppl_put_func = put_func
        return _iterable_put_data_wrapper
