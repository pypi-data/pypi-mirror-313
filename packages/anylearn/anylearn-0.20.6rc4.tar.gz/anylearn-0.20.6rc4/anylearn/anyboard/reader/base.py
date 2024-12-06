from enum import Enum


class ReaderType(Enum):
    CLOUD = "iotdb"
    CSV = "csv"


class ReaderBase:
    type: ReaderType

    def __init__(self, type):
        self.type = type

    def get_metric_meta(self, project_id):
        pass

    def get_metric_scalar(self, project_id, scalar_metric_query_list):
        pass

    def get_metric_image(self, project_id, image_metric_query_list):
        pass

    def get_metric_histogram(self, project_id, histogram_metric_query_list):
        pass
