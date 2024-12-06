import os
import time
import numpy as np
import logging

anyboard_logger = logging.getLogger('ANYBOARD')


def init_anyboard_logger(log_dir):
    log_path = os.path.join(log_dir, 'anyboard.log')
    anyboard_logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    anyboard_logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    anyboard_logger.addHandler(ch)

    anyboard_logger.propagate = False
    anyboard_logger.info("Initialized anyboard logger at {}".format(log_path))


numpy_compatible = np.ndarray
try:
    import torch

    numpy_compatible = torch.Tensor
except ImportError:
    pass


def prepare_pytorch(x):
    import torch
    if isinstance(x, torch.autograd.Variable):
        x = x.data
    x = x.cpu().numpy()
    return x


def prepare_mxnet(x):
    x = x.asnumpy()
    return x


def prepare_chainer(x):
    import chainer
    x = chainer.cuda.to_cpu(x.data)
    return x


def make_np(x) -> np.ndarray:
    if isinstance(x, list):
        return check_nan(np.array(x))
    if isinstance(x, np.ndarray):
        return check_nan(x)
    if isinstance(x, str):  # Caffe2 will pass name of blob(s) to fetch
        return check_nan(prepare_caffe2(x))
    if np.isscalar(x):
        return check_nan(np.array([x]))
    if 'torch' in str(type(x)):
        return check_nan(prepare_pytorch(x))
    if 'chainer' in str(type(x)):
        return check_nan(prepare_chainer(x))
    if 'mxnet' in str(type(x)):
        return check_nan(prepare_mxnet(x))
    if 'jax' in str(type(x)):
        return check_nan(np.array(x))
    raise NotImplementedError('Got {}, but expected numpy array or torch tensor.'.format(type(x)))


def check_nan(array):
    tmp = np.sum(array)
    if np.isnan(tmp) or np.isinf(tmp):
        msg = 'NaN or Inf found in input tensor.'
        anyboard_logger.warning(msg)
    return array


def time_start():
    return time.time()


def log_time_delta(t, event_name):
    d = time.time() - t
    anyboard_logger.debug(f"{event_name} time: {d}")
