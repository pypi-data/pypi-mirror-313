import json
from typing import List

import requests

from anylearn import AnylearnConfig

from .base import ReaderBase, ReaderType
from .metric import MetricQuery, MetricMeta, MetricType, record_class_map, metric_class_map
from .metric import dict_keys_to_snake_case
from ..utils import anyboard_logger as logger


class CloudReader(ReaderBase):
    def __init__(self, cluster_address=None, token=None):
        super().__init__(ReaderType.CLOUD)
        self.cluster_address = AnylearnConfig.cluster_address if cluster_address is None else cluster_address
        self.token = AnylearnConfig.token if token is None else token
        self.headers = {
            'Authorization': f'Bearer {self.token}'
        }

    def get_metric_meta(self, project_id) -> List[MetricMeta]:
        url = f"{self.cluster_address}/api/anyboard/{project_id}/metric/meta"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            logger.error(f"get metric meta failed: {resp.json()}")
        return [MetricMeta(meta['taskId'], meta['name'], MetricType(meta['type'].upper()), meta['count'])
                for meta in resp.json()['metricMetaList']]

    def get_metric(self, metric_type: MetricType, project_id: str, metric_query_list: List[MetricQuery]):
        metric_meta_list = self.get_metric_meta(project_id)
        # (task_id, name, type) 联合做字典的键
        metric_meta_dict = {(meta.task_id, meta.name, meta.type.name): meta for meta in metric_meta_list}

        url = f"{self.cluster_address}/api/anyboard/{project_id}/metric/{metric_type.name.lower()}s"
        data = {
            f'{metric_type.name.lower()}_metric_query_list': json.dumps(
                [query.to_dict() for query in metric_query_list])
        }
        resp = requests.get(url, params=data, headers=self.headers)

        if resp.status_code != 200:
            logger.error(f"[anyboard] get metric {metric_type.name.lower()} failed: {resp.json()}")
            return []
        res = resp.json()

        metric_obj_list = []
        for metric in res[f'{metric_type.name.lower()}MetricList']:
            record_class = record_class_map[metric_type]
            record_list = [record_class(**dict_keys_to_snake_case(record)) for record in
                           metric[f'{metric_type.name.lower()}RecordList']]
            metric_class = metric_class_map[metric_type]
            metric_meta = metric_meta_dict.get((metric['taskId'], metric['metricName'], metric_type.name))
            metric_obj_list.append(metric_class(meta=metric_meta, record_list=record_list))
        return metric_obj_list
