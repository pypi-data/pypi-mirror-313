from enum import Enum
from typing import List


class MetricType(Enum):
    SCALAR = "SCALAR"
    IMAGE = "IMAGE"
    HISTOGRAM = "HISTOGRAM"


class MetricMeta:
    def __init__(self, task_id: str, name: str, type: MetricType, count: int):
        self.task_id = task_id
        self.name = name
        self.type = type
        self.count = count

    def __repr__(self):
        return f"MetricMeta(task_id={self.task_id}, name={self.name}, type={self.type}, count={self.count})"


class MetricQuery:
    def __init__(self, task_id: str, metric_name: str, offset: int, limit: int):
        self.task_id = task_id
        self.metric_name = metric_name
        self.offset = offset
        self.limit = limit

    def __repr__(self):
        return f"MetricQuery(task_id={self.task_id}, metric_name={self.metric_name}, offset={self.offset}, limit={self.limit})"

    def to_dict(self):
        return {
            'taskId': self.task_id,
            'metricName': self.metric_name,
            'offset': self.offset,
            'limit': self.limit
        }


class RecordBase:
    def __init__(self, step: int = None, walltime: int = None):
        self.step = step
        self.walltime = walltime


class MetricBase:
    def __init__(self, meta: MetricMeta, record_list: List[RecordBase]):
        self.meta = meta
        self.record_list = record_list
