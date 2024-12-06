import csv
import os

from ..summary import Summary, ValueType
from .base import WriterBase, WriterType
from ...utils import anyboard_logger as logger


class CsvWriter(WriterBase):
    def __init__(self, csv_dir):
        super().__init__(WriterType.CSV)
        self.csv_dir = os.path.abspath(csv_dir)

    def start(self):
        # - 创建目录：csv_dir
        if not os.path.exists(self.csv_dir):
            os.makedirs(self.csv_dir)

    def end(self):
        logger.debug("CsvWriter end")

    def create(self, name, type: ValueType):
        # 创建文件 csv_dir/name.csv csv_dir已知
        file_path = os.path.join(self.csv_dir, type.name.lower(), name + ".csv")
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            if type == ValueType.SCALAR:
                writer.writerow(["walltime", "step", "single_value"])
            elif type == ValueType.IMAGE:
                columns = ["walltime", "step", "height", "width", "channel", "size", "file_format"]
                writer.writerow(columns)
                image_dir = os.path.join(self.csv_dir, name)
                os.makedirs(image_dir)
            elif type == ValueType.HISTOGRAM:
                c = ["walltime", "step", "min", "max", "num", "sum", "sum_squares", "bucket_limits", "bucket_counts"]
                writer.writerow(c)
            else:
                msg = f"Type {type} is not supported in CsvWriter"
                logger.error(msg)
                return

    def add(self, summary: Summary):
        file_path = os.path.join(self.csv_dir, summary.value.type.name.lower(), summary.name + ".csv")
        with open(file_path, mode='a', newline='') as file:
            if summary.value.type == ValueType.SCALAR:
                writer = csv.writer(file)
                writer.writerow([summary.walltime, summary.step, summary.value.value])
            elif summary.value.type == ValueType.IMAGE:
                writer = csv.writer(file)
                image_path = os.path.join(self.csv_dir, summary.name, f"{summary.step}.png")
                with open(image_path, mode='wb') as image_file:
                    image_file.write(summary.value.image_bytes)
                # insert_img_str = base64.b64encode(summary.value.image_bytes).decode('utf-8')
                writer.writerow(
                    [summary.walltime, summary.step, summary.value.height, summary.value.width,
                     summary.value.channel, summary.value.size, summary.value.file_format])
            elif summary.value.type == ValueType.HISTOGRAM:
                writer = csv.writer(file)
                writer.writerow(
                    [summary.walltime, summary.step, summary.value.min, summary.value.max,
                     summary.value.num, summary.value.sum, summary.value.sum_squares,
                     summary.value.bucket_limits, summary.value.bucket_counts])
            else:
                msg = f"Type {summary.value.type} is not supported in CsvWriter"
                logger.error(msg)
                return
