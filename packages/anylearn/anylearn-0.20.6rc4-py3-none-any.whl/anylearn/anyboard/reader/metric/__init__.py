from typing import Dict

from .base import MetricQuery, MetricMeta, MetricType, MetricBase
from .scalar import ScalarMetric, ScalarRecord
from .histogram import HistogramMetric, HistogramRecord
from .utils import dict_keys_to_snake_case

metric_class_map: Dict[MetricType, type] = {
    MetricType.SCALAR: ScalarMetric,
    MetricType.HISTOGRAM: HistogramMetric,
    # MetricType.IMAGE: ImageMetric,
}

record_class_map: Dict[MetricType, type] = {
    MetricType.SCALAR: ScalarRecord,
    MetricType.HISTOGRAM: HistogramRecord,
    # MetricType.IMAGE: ImageRecord,
}


__all__ = [
    'MetricQuery',
    'MetricMeta',
    'MetricType',
    'MetricBase',
    'ScalarMetric',
    'ScalarRecord',
    'HistogramMetric',
    'HistogramRecord',
    'metric_class_map',
    'record_class_map',
    'dict_keys_to_snake_case'
]
