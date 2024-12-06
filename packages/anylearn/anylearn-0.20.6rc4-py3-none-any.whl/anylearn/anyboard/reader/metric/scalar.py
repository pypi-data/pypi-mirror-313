from typing import List

from .base import MetricBase, MetricMeta, RecordBase


class ScalarRecord(RecordBase):
    def __init__(self,
                 step: int = None,
                 walltime: int = None,
                 value: float = None,
                 ):
        super().__init__(step, walltime)
        self.value = value

    def __repr__(self):
        return f"ScalarRecord(step={self.step}, walltime={self.walltime}, value={self.value})"


class ScalarMetric(MetricBase):
    def __init__(self,
                 meta: MetricMeta = None,
                 record_list: List[ScalarRecord] = None
                 ):
        super().__init__(meta, record_list)
        self.record_list = record_list

    def __repr__(self):
        return f"ScalarMetric(meta={self.meta}, record_list={self.record_list})"

    def get_min(self):
        return min([record.value for record in self.record_list])

    def get_max(self):
        return max([record.value for record in self.record_list])

    def get_value_by_mode(self, mode: str):
        if mode == 'minimize':
            return self.get_min()
        elif mode == 'maximize':
            return self.get_max()
        else:
            raise ValueError(f"mode {mode} not supported")

    def get_last(self):
        return self.record_list[-1].value
