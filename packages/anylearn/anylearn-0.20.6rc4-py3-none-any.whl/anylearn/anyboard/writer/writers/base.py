from enum import Enum
from ..summary import ValueType


class WriterType(Enum):
    IOTDB = "iotdb"
    CSV = "csv"
    # TENSORBOARD = "tensorboard"  # 内生支持（封装之前直接生效）
    # SQLITE = "sqlite" # 之后支持
    # TSFILE = "tsfile" # 之后支持


class WriterBase:
    def __init__(self, type: WriterType):
        self.type = type
        self.give_up = False

    def start(self):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError

    def create(self, name, type: ValueType):
        raise NotImplementedError

    def add(self, summary_obj):
        raise NotImplementedError
