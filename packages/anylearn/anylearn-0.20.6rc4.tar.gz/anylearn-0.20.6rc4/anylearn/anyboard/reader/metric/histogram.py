from typing import List

from .base import RecordBase, MetricMeta, MetricBase


class HistogramRecord(RecordBase):
    def __init__(self,
                 step: int = None,
                 walltime: int = None,
                 min: float = None,
                 max: float = None,
                 num: int = None,
                 sum: float = None,
                 sum_squares: float = None,
                 limit_list: List[float] = None,
                 value_list: List[float] = None):
        super().__init__(step, walltime)
        self.min = min
        self.max = max
        self.num = num
        self.sum = sum
        self.sum_squares = sum_squares
        self.limit_list = limit_list or []
        self.value_list = value_list or []

    def __repr__(self):
        return f"HistogramRecord(step={self.step}, walltime={self.walltime}, min={self.min}, max={self.max}, num={self.num}, sum={self.sum}, sum_squares={self.sum_squares}, limit_list={self.limit_list}, value_list={self.value_list})"

    def calculate_average(self):
        return self.sum / self.num if self.num else 0

    def calculate_variance(self):
        if not self.num:
            return 0
        mean = self.calculate_average()
        return (self.sum_squares / self.num) - (mean ** 2)


class HistogramMetric(MetricBase):
    def __init__(self,
                 meta: MetricMeta = None,
                 record_list: List[HistogramRecord] = None
                 ):
        super().__init__(meta, record_list)
        self.record_list = record_list

    def __repr__(self):
        return f"HistogramMetric(meta={self.meta}, record_list={self.record_list})"

    def get_latest_record(self):
        return self.record_list[-1] if self.record_list else None
