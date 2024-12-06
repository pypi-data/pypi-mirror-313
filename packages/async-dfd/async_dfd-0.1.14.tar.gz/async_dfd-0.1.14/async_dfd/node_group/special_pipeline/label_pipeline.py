import logging
import functools

from ..pipeline import Pipeline
from ...node.decorator import label_proc_decorator
from ...label import LabelData

logger = logging.getLogger(__name__)


class LabelPipeline(Pipeline):
    """
    A pipeline that processes data in an iterable format.

    This pipeline extends the base `Pipeline` class and provides additional functionality for processing data in an iterable format.
    It supports putting data into the pipeline, starting the pipeline, and getting processed data from the pipeline.

    Attributes:
        over_data_points (Queue): A queue that buffers the processed data points, waiting for assembling.
        proc_data_task: An task that retrieves processed data from the `over_data_points` queue and assemble them

    """

    def __init__(self, all_nodes):
        super().__init__(all_nodes=all_nodes)
        self.label_functions = []
        for node in self.all_nodes.values():
            node.add_proc_decorator(label_proc_decorator)
        self.head.add_get_decorator(self._label_get_data_decorator)
        self.tail.add_put_decorator(self._unlabel_put_data_decorator)

    def set_label_function(self, label_function):
        assert callable(
            label_function
        ), f"The label function {label_function} is not callable"
        self.label_functions.append(label_function)

    def get_data_func_label(self, label_data, func):
        assert isinstance(
            label_data, LabelData
        ), f"The data {label_data} is not a LabelData"
        assert (
            func in self.label_functions
        ), f"The function {func} is not in the label functions"
        label = label_data.label[0][func.__qualname__]
        return label

    def _label_get_data_decorator(self, get_func):
        @functools.wraps(get_func)
        def _label_get_data_wrapper(data):
            ret_data = get_func(data)
            for d in ret_data:
                label = {}
                for label_function in self.label_functions:
                    label[label_function.__qualname__] = label_function(d, data)
                label = (label,)
                label_data = LabelData(d, label)
                yield label_data

        return _label_get_data_wrapper

    def _unlabel_put_data_decorator(self, put_func):
        @functools.wraps(put_func)
        def _unlabel_put_data_wrapper(label_data):
            assert isinstance(
                label_data, LabelData
            ), f"The data {label_data} is not a LabelData"
            put_func(label_data.data)

        return _unlabel_put_data_wrapper
