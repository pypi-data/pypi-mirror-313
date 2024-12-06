import gevent
import sys
import trio # do not delete this line, it will be effected by monkey patch that will cause fault
from gevent import monkey
monkey.patch_all()
print("Monkey patching gevent in async dfd")
gevent.get_hub().exception_stream = sys.stderr

import json

try:
    with open("./config/async_dfd_config.json", "r") as f:
        ASYNC_DFD_CONFIG = json.load(f)
except FileNotFoundError:
    ASYNC_DFD_CONFIG = {}

from .node import Node, decorator
from .node_group import (
    Graph,
    Pipeline,
    Sequential,
    CyclePipeline,
    LabelPipeline,
    IterablePipeline,
    OrderPipeline,
)
from .analyser import Analyser, Monitor, PipelineAnalyser

__all__ = [
    "Node",
    "Graph",
    "Pipeline",
    "Sequential",
    "CyclePipeline",
    "LabelPipeline",
    "IterablePipeline",
    "OrderPipeline",
    "Analyser",
    "Monitor",
    "PipelineAnalyser",
    "decorator",
]
