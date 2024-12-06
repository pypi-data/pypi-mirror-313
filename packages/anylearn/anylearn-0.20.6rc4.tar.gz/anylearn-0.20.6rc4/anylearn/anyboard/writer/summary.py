# Filename: summary.py
import re
from enum import Enum
import io
from ..utils import make_np, anyboard_logger as logger

try:
    import numpy as np
except ImportError:
    msg = "numpy is not installed, please install 'numpy' first."
    logger.error(msg)


class Summary:

    def __init__(self, name, value, step, walltime, input_dict=None):
        self.name = name
        self.value = value
        self.step = step
        self.walltime = walltime
        self.input_dict = input_dict  # ??


class ValueType(Enum):
    SCALAR = "scalar"
    IMAGE = "image"
    HISTOGRAM = "histogram"


class ValueBase:
    def __init__(self, type):
        self.type = type
        self.give_up = False


class ScalarValue(ValueBase):

    def __init__(self, value):
        super().__init__(ValueType.SCALAR)
        self.value = self.clean_value(value)
        self.give_up = False

    def clean_value(self, value):
        try:
            return float(value)
        except Exception as e:
            msg = f"Value {value} can not be converted to float: {e}"
            logger.error(msg)
            self.give_up = True


class ImageValue(ValueBase):
    def __init__(self, image_tensor, dataformats="CHW", file_format="PNG"):
        super().__init__(ValueType.IMAGE)
        self.file_format = self.clean_file_format(file_format.upper())
        tensor = self.transform_tensor(image_tensor, dataformats.upper())
        if self.give_up:
            return
        self.image_bytes = self.make_image(tensor)
        if self.give_up is None:
            return
        self.size = len(self.image_bytes)  # ...
        self.height = tensor.shape[0]
        self.width = tensor.shape[1]
        self.channel = tensor.shape[2]

    def clean_file_format(self, file_format):
        if file_format not in ["PNG"]:
            msg = f"file_format {file_format} is not supported in ImageValue, set to PNG"
            logger.error(msg)
            return "PNG"
        return file_format

    def transform_tensor(self, image_tensor, tensor_format):
        tensor = make_np(image_tensor)
        if tensor_format not in ["HW", "HWC", "CHW", "NCHW"]:
            msg = f"tensor_format {tensor_format} is not supported in ImageValue"
            logger.error(msg)
            self.give_up = True
            return None
        tensor = self.convert_to_hwc(tensor, tensor_format)
        if self.give_up:
            return None
        if tensor.dtype != np.uint8:
            tensor = (tensor * 255.0).astype(np.uint8)  # 对错误的数据范围做了自动处理
        return tensor

    def make_image(self, tensor):
        try:
            from PIL import Image
        except ImportError:
            msg = "PIL is not installed, please install 'pillow' first."
            logger.error(msg)
            self.give_up = True
            return None
        image = Image.fromarray(tensor)
        output = io.BytesIO()
        image.save(output, format=self.file_format)
        image_bytes = output.getvalue()
        output.close()
        return image_bytes

    def convert_to_hwc(self, tensor, input_format):
        if len(tensor.shape) != len(input_format):
            msg = f"input tensor shape {tensor.shape} and input format {input_format} are inconsistent."
            logger.error(msg)
            self.give_up = True
            return None
        input_format = input_format.upper()

        if len(input_format) == 4:
            index = [input_format.find(c) for c in 'NCHW']
            tensor_nchw = tensor.transpose(index)
            if tensor_nchw.shape[1] not in [1, 3, 4]:
                self.give_up = True
                msg = f"The channel of input tensor is {tensor_nchw.shape[1]}, only 1, 3, 4 are supported."
                logger.error(msg)
                return None
            tensor_chw = self.make_grid(tensor_nchw)
            return tensor_chw.transpose((1, 2, 0))
        if len(input_format) == 3:
            index = [input_format.find(c) for c in 'HWC']
            tensor_hwc = tensor.transpose(index)
            if tensor_hwc.shape[2] not in [1, 3, 4]:
                self.give_up = True
                msg = f"The channel of input tensor is {tensor_hwc.shape[2]}, only 1, 3, 4 are supported."
                logger.error(msg)
                return None
            if tensor_hwc.shape[2] == 1:
                tensor_hwc = np.concatenate([tensor_hwc, tensor_hwc, tensor_hwc], 2)
            return tensor_hwc

        if len(input_format) == 2:
            index = [input_format.find(c) for c in 'HW']
            tensor = tensor.transpose(index)
            tensor = np.stack([tensor, tensor, tensor], 2)
            return tensor

    def make_grid(self, nchw_tensor, ncols=8):
        num = nchw_tensor.shape[0]
        channel = nchw_tensor.shape[1]
        height = nchw_tensor.shape[2]
        width = nchw_tensor.shape[3]
        if channel == 1:
            nchw_tensor = np.concatenate([nchw_tensor, nchw_tensor, nchw_tensor], 1)
        ncols = min(num, ncols)
        nrows = int(np.ceil(float(num) / ncols))
        canvas = np.zeros((nchw_tensor.shape[1], height * nrows, width * ncols), dtype=nchw_tensor.dtype)
        i = 0
        for y in range(nrows):
            for x in range(ncols):
                if i >= num:
                    break
                canvas[:, y * height:(y + 1) * height, x * width:(x + 1) * width] = nchw_tensor[i]
                i = i + 1
        return canvas


class HistogramValue(ValueBase):

    def __init__(self):
        super().__init__(ValueType.HISTOGRAM)
        self.min = None
        self.max = None
        self.num = None
        self.sum = None
        self.sum_squares = None
        self.bucket_limits = None
        self.bucket_counts = None

    def make_default_bins(self):
        v = 1E-12
        buckets = []
        neg_buckets = []
        while v < 1E20:
            buckets.append(v)
            neg_buckets.append(-v)
            v *= 1.1
        bins = neg_buckets[::-1] + [0] + buckets
        return bins

    def init_from_histogram(self, values, bins, max_bins=None):
        if bins == 'tensorflow':
            bins = self.make_default_bins()
        values = make_np(values).astype(float)
        if values.size == 0:
            msg = 'The input has no element.'
            logger.error(msg)
            self.give_up = True
            return
        values = values.reshape(-1)
        counts, limits = np.histogram(values, bins=bins)
        num_bins = len(counts)
        # Deal with max bins using subsampling and np.pad
        if max_bins is not None and num_bins > max_bins:
            subsampling = num_bins // max_bins
            subsampling_remainder = num_bins % subsampling
            if subsampling_remainder != 0:
                counts = np.pad(counts, pad_width=[[0, subsampling - subsampling_remainder]],
                                mode="constant", constant_values=0)
            counts = counts.reshape(-1, subsampling).sum(axis=-1)
            new_limits = np.empty((counts.size + 1,), limits.dtype)
            new_limits[:-1] = limits[:-1:subsampling]
            new_limits[-1] = limits[-1]
            limits = new_limits

        # Find the first and the last bin defining the support of the histogram:
        cum_counts = np.cumsum(np.greater(counts, 0))
        start, end = np.searchsorted(cum_counts, [0, cum_counts[-1] - 1], side="right")
        start = int(start)
        end = int(end) + 1

        counts = counts[start - 1:end] if start > 0 else np.concatenate([[0], counts[:end]])
        limits = limits[start:end + 1]

        if counts.size == 0 or limits.size == 0:
            msg = 'The histogram is empty, please file a bug report.'
            logger.error(msg)
            self.give_up = True
            return

        sum_clipped = np.clip(values.sum(), np.finfo(np.float32).min, np.finfo(np.float32).max)
        sum_sq_clipped = np.clip((values ** 2).sum(), np.finfo(np.float32).min, np.finfo(np.float32).max)

        # 初始化
        self.min = values.min()
        self.max = values.max()
        self.num = len(values)
        self.sum = sum_clipped
        self.sum_squares = sum_sq_clipped
        self.bucket_limits = limits.tolist()
        self.bucket_counts = counts.tolist()

    def init_from_histogram_raw(self, min, max, num, sum, sum_squares, bucket_limits, bucket_counts):
        if len(bucket_limits) != len(bucket_counts):
            msg = f"Length of bucket_limits {len(bucket_limits)} and bucket_counts {len(bucket_counts)} are different."
            logger.error(msg)
            self.give_up = True
            return
        self.min = min
        self.max = max
        self.num = num
        self.sum = sum
        self.sum_squares = sum_squares
        self.bucket_limits = bucket_limits
        self.bucket_counts = bucket_counts
