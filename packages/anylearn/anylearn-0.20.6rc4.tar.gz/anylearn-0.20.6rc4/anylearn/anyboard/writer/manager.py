import os
import re
import time
import atexit
from typing import Optional, Union
from datetime import datetime
from .summary import Summary, ValueType, ScalarValue, ImageValue, HistogramValue
from .writers.csv_writer import CsvWriter
from .writers.iotdb_writer import IotdbWriter
from ..utils import init_anyboard_logger, anyboard_logger as logger, numpy_compatible
from ..utils import time_start, log_time_delta
from anylearn.utils.singleton import Singleton

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class WriterManager(metaclass=Singleton):
    def __init__(self, log_dir=None, writer_config=None):
        _t = time_start()
        self.time_str = datetime.now().strftime('%b%d_%H-%M-%S')
        self._log_dir = os.path.abspath(os.getenv("ANYLEARN_TASK_OUTPUT_PATH", "./") if log_dir is None else log_dir)
        self.log_dir = os.path.join(self._log_dir, "anyboard_runs", self.time_str)
        os.makedirs(self.log_dir)
        init_anyboard_logger(self.log_dir)

        default_writer_config = {
            "enable_list": {
                "iotdb_writer": True if os.getenv("ANYLEARN_ANYBOARD_IOTDB_HOST") else False,
                "csv_writer": True,
                "tensorboard_writer": True,
            }
        }
        self.writer_config = writer_config if writer_config is not None else default_writer_config

        self.writer_list = self._make_writer_list()
        self.tensorboard_writer = self._make_tensorboard_writer()
        self.count_dict = {}
        log_time_delta(_t, "init")

    def _make_writer_list(self):
        writer_list = []
        if self.writer_config["enable_list"]["csv_writer"]:
            writer_list.append(CsvWriter(os.path.join(self.log_dir, "csv")))
            writer_list[-1].start()
            atexit.register(writer_list[-1].end)
        if self.writer_config["enable_list"]["iotdb_writer"]:
            writer_list.append(IotdbWriter())
            writer_list[-1].start()
            atexit.register(writer_list[-1].end)
        return writer_list

    def _make_tensorboard_writer(self):
        if not self.writer_config["enable_list"]["tensorboard_writer"]:
            return None
        logdir = os.path.join(self._log_dir)  # + comment?
        try:
            from tensorboardX import SummaryWriter
        except ImportError:
            msg = "Tensorboard is not available"
            logger.error(msg)
            return None
        return SummaryWriter(logdir)  # 希望兼容anylearn上已有的tensorboard功能

    def _standardize(self, name, value_type, step=None):
        walltime = int(round(time.time() * 1000))
        # name 格式要求：参考tensorboard，只允许字母数字下划线横杠斜杠点
        invalid_tag_characters = re.compile(r'[^-/\w\.]')
        if name is not None:
            new_name = invalid_tag_characters.sub('_', name)
            new_name = new_name.lstrip('/')
            if new_name != name:
                msg = f"Summary name {name} is illegal; using {new_name} instead."
                logger.warning(msg)
                name = new_name

        if name not in self.count_dict:
            for writer_obj in self.writer_list:
                if writer_obj.give_up:
                    continue
                writer_obj.create(name, value_type)
            self.count_dict[name] = 0
        else:
            self.count_dict[name] += 1

        # 再判断step是否合法，若不合法则使用默认的count
        if step is not None:
            try:
                step = int(step)
            except ValueError:
                # 转换不了，使用默认的count
                new_step = self.count_dict[name]
                msg = f"Step {step} can not be converted to int, set to {new_step}"
                logger.error(msg)
                step = new_step
        else:
            step = self.count_dict[name]

        return name, step, walltime

    def _writers_add(self, summary_obj):
        value_type_str = summary_obj.value.type.name.lower()
        for writer_obj in self.writer_list:
            writer_type_str = writer_obj.type.name.lower()
            t = time_start()
            if writer_obj.give_up:
                log_time_delta(t, f"anyboard.{value_type_str}.{writer_type_str}.give_up")
                continue
            writer_obj.add(summary_obj)
            log_time_delta(t, f"anyboard.{value_type_str}.{writer_type_str}.write")

    def close(self):
        pass

    def add_scalar(self,
                   tag: str,
                   scalar_value: Union[float, numpy_compatible],
                   global_step: Optional[int] = None,
                   walltime: Optional[float] = None,
                   **kwargs):
        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_scalar(tag, scalar_value, global_step, walltime, **kwargs)
            log_time_delta(start_time, "tensorboard.scalar.total")
        t1 = time_start()
        name, step, walltime = self._standardize(tag, ValueType.SCALAR, global_step)
        scalar_value = ScalarValue(scalar_value)
        log_time_delta(t1, "anyboard.scalar.pack")
        if scalar_value.give_up:
            log_time_delta(t1, "anyboard.scalar.write.give_up")
            return
        summary_obj = Summary(name, scalar_value, step, walltime)
        t2 = time_start()
        self._writers_add(summary_obj)
        log_time_delta(t2, "anyboard.scalar.write")
        log_time_delta(t1, "anyboard.scalar.total")

    def add_image(self,
                  tag: str,
                  img_tensor: numpy_compatible,
                  global_step: Optional[int] = None,
                  walltime: Optional[float] = None,
                  dataformats: Optional[str] = 'CHW'):
        # TODO 加Optional[str] = 'CHW' 学Optional
        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_image(tag, img_tensor, global_step, walltime, dataformats)
            log_time_delta(start_time, "tensorboard.image.total")
        t1 = time_start()
        name, step, walltime = self._standardize(tag, ValueType.IMAGE, global_step)
        image_value = ImageValue(img_tensor, dataformats=dataformats, file_format="PNG")
        log_time_delta(t1, "anyboard.image.pack")
        if image_value.give_up:
            log_time_delta(t1, "anyboard.image.write.give_up")
            return
        summary_obj = Summary(name, image_value, step, walltime)
        t2 = time_start()
        self._writers_add(summary_obj)
        log_time_delta(t2, "anyboard.image.write")
        log_time_delta(t1, "anyboard.image.total")

    def add_histogram(
            self,
            tag: str,
            values: numpy_compatible,
            global_step: Optional[int] = None,
            bins: Optional[str] = 'tensorflow',  # ref to np.histogram
            walltime: Optional[float] = None,
            max_bins=None,
    ):
        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_histogram(tag, values, global_step, bins, walltime, max_bins)
            log_time_delta(start_time, "tensorboard.histogram.total")
        try:
            import numpy as np
        except ImportError:
            msg = "numpy is not installed, please install 'numpy' first."
            logger.error(msg)
            return
        t1 = time_start()
        name, step, walltime = self._standardize(tag, ValueType.HISTOGRAM, global_step)
        histogram_value = HistogramValue()
        histogram_value.init_from_histogram(values, bins, max_bins)
        log_time_delta(t1, "anyboard.histogram.pack")
        if histogram_value.give_up:
            log_time_delta(t1, "anyboard.histogram.write.give_up")
            return
        summary_obj = Summary(name, histogram_value, step, walltime)
        t2 = time_start()
        self._writers_add(summary_obj)
        log_time_delta(t2, "anyboard.histogram.write")
        log_time_delta(t1, "anyboard.histogram.total")

    def add_histogram_raw(
            self,
            tag: str,
            min,
            max,
            num,
            sum,
            sum_squares,
            bucket_limits,
            bucket_counts,
            global_step: Optional[int] = None,
            walltime: Optional[float] = None):
        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_histogram_raw(tag, min, max, num, sum, sum_squares,
                                                      bucket_limits, bucket_counts, global_step, walltime)
            log_time_delta(start_time, "tensorboard.histogram_raw.total")
        t1 = time_start()
        name, step, walltime = self._standardize(tag, ValueType.HISTOGRAM, global_step)
        histogram_value = HistogramValue()
        histogram_value.init_from_histogram_raw(min, max, num, sum, sum_squares, bucket_limits, bucket_counts)
        log_time_delta(t1, "anyboard.histogram_raw.pack")
        if histogram_value.give_up:
            log_time_delta(t1, "anyboard.histogram_raw.write.give_up")
            return
        summary_obj = Summary(name, histogram_value, step, walltime)
        t2 = time_start()
        self._writers_add(summary_obj)
        log_time_delta(t2, "anyboard.histogram_raw.write")
        log_time_delta(t1, "anyboard.histogram_raw.total")

    def add_figure(
            self,
            tag: str,
            figure,
            global_step: Optional[int] = None,
            close: Optional[bool] = True,
            walltime: Optional[float] = None):

        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_figure(tag, figure, global_step, close, walltime)
            log_time_delta(start_time, "tensorboard.figure.total")
        try:
            import matplotlib.pyplot as plt
            import matplotlib.backends.backend_agg as plt_backend_agg
        except ImportError:
            logger.error("Matplotlib is not available")
            return

        try:
            import numpy as np
        except ImportError:
            msg = "numpy is not installed, please install 'numpy' first."
            logger.error(msg)
            return

        def render_to_rgb(figure, close=True):
            canvas = plt_backend_agg.FigureCanvasAgg(figure)
            canvas.draw()
            data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
            w, h = figure.canvas.get_width_height()
            image_hwc = data.reshape([h, w, 4])[:, :, 0:3]
            image_chw = image_hwc.transpose([2, 0, 1])
            if close:
                plt.close(figure)
            return image_chw

        def figure_to_image(figures, close=True):
            if isinstance(figures, list):
                images = [render_to_rgb(figure, close) for figure in figures]
                return np.stack(images)
            else:
                image = render_to_rgb(figures)
                return image

        if self.tensorboard_writer is not None:
            start_time = time_start()
            self.tensorboard_writer.add_figure(tag, figure, global_step, close, walltime)
            log_time_delta(start_time, "tensorboard.figure.total")

        t1 = time_start()
        data_formats = 'NCHW' if isinstance(figure, list) else 'CHW'
        img_tensor = figure_to_image(figure, close)
        if img_tensor is None:
            log_time_delta(t1, "anyboard.figure.figure_to_image.give_up")
            return
        log_time_delta(t1, "anyboard.figure.figure_to_image")
        t2 = time_start()
        self.add_image(tag, img_tensor, global_step, walltime, dataformats=data_formats)
        log_time_delta(t2, "anyboard.figure.add_image")
        log_time_delta(t1, "anyboard.figure.total")

    def watch(
            self,
            models,
            criterion=None,
            log: Optional[Literal["gradients", "parameters", "all"]] = "all",
            log_freq: int = 1000,
            idx: Optional[int] = None,
            log_graph: bool = False,
    ):
        from .watch import PytorchWatcher
        PytorchWatcher().watch(models, criterion, log, log_freq, idx, log_graph)

    def unwatch(self, models=None):
        """Remove pytorch model topology, gradient and parameter hooks.

        Args:
            models: (list) Optional list of pytorch models that have had watch called on them
        """
        from .watch import PytorchWatcher

        if models:
            if not isinstance(models, (tuple, list)):
                models = (models,)
            for model in models:
                if not hasattr(model, "_anyboard_hook_names"):
                    # wandb.termwarn("%s model has not been watched" % model)
                    msg = f"{model} model has not been watched"
                    logger.warning(msg)
                else:
                    for name in model._wandb_hook_names:
                        # wandb.run._torch.unhook(name)
                        PytorchWatcher().unhook(name)
                    delattr(model, "_wandb_hook_names")
                    # TODO: we should also remove recursively model._wandb_watch_called

        else:
            # wandb.run._torch.unhook_all()
            PytorchWatcher().unhook_all()
