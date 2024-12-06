from typing import Optional, List
from ..utils import anyboard_logger as logger
from .manager import WriterManager
from anylearn.utils.singleton import Singleton

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

_global_watch_idx = 0

try:
    import torch
except ImportError:
    msg = "torch is not installed, please install 'torch' first."
    logger.error(msg)
    torch = None

LOG_TRACK_COUNT, LOG_TRACK_THRESHOLD = range(2)


def log_track_init(log_freq: int) -> List[int]:
    """create tracking structure used by log_track_update"""
    l = [0] * 2
    l[LOG_TRACK_THRESHOLD] = log_freq
    return l


def log_track_update(log_track: List[int]) -> bool:
    """count (log_track[0]) up to threshold (log_track[1]), reset count (log_track[0]) and return true when reached"""
    log_track[LOG_TRACK_COUNT] += 1
    if log_track[LOG_TRACK_COUNT] < log_track[LOG_TRACK_THRESHOLD]:
        return False
    log_track[LOG_TRACK_COUNT] = 0
    return True


def log_track_get_count(log_track: List[int]) -> int:
    return log_track[LOG_TRACK_COUNT]


def _no_finite_values(tensor: "torch.Tensor") -> bool:
    return tensor.shape == torch.Size([0]) or (~torch.isfinite(tensor)).all().item()


def _remove_infs_nans(tensor: "torch.Tensor") -> "torch.Tensor":
    if not torch.isfinite(tensor).all():
        tensor = tensor[torch.isfinite(tensor)]

    return tensor


def _torch_hook_handle_is_valid(handle):
    d = handle.hooks_dict_ref()
    if d is None:
        return False
    else:
        return handle.id in d


class PytorchWatcher(metaclass=Singleton):

    def __init__(self):
        global _global_watch_idx
        _global_watch_idx = 0
        self._hook_handles = {}
        self._num_bins = 64
        self._is_cuda_histc_supported = None
        # self.hook_torch = TorchGraph.hook_torch

    def watch(
            self,
            models,
            criterion=None,
            log: Optional[Literal["gradients", "parameters", "feature", "all"]] = "all",
            log_freq: int = 1000,
            idx: Optional[int] = None,
            log_graph: bool = False,
    ):
        global _global_watch_idx

        logger.info("Watching")
        logger.debug(f"watch models: {models}")

        if log not in {"gradients", "parameters", "all", None}:
            msg = f"log must be one of 'gradients', 'parameters', 'all', or None. Received {log}. Setting to 'all'."
            logger.warning(msg)
            log = "all"

        log_parameters = log in {"parameters", "all"}
        log_gradients = log in {"gradients", "all"}
        log_features = log in {"features", "all"}

        if not isinstance(models, (tuple, list)):
            models = (models,)

        try:
            import torch
        except ImportError:
            msg = "torch is not installed, please install 'torch' first."
            logger.error(msg)
            return

        for model in models:
            if not isinstance(model, torch.nn.Module):
                # raise ValueError("Expected a pytorch model (torch.nn.Module). Received " + str(type(model)))
                msg = "Expected a pytorch model (torch.nn.Module). Received " + str(type(model))
                logger.error(msg)
                return

        graphs = []

        if idx is None:
            idx = _global_watch_idx
        for local_idx, model in enumerate(models):
            global_idx = idx + local_idx
            _global_watch_idx += 1
            # prefix = "graph_%i" % global_idx
            # moduleClass
            prefix = str(global_idx) + '-' + model.__class__.__name__

            if log_parameters:
                self.add_log_parameters_hook(model, prefix=prefix, log_freq=log_freq, )

            if log_gradients:
                self.add_log_gradients_hook(model, prefix=prefix, log_freq=log_freq, )

            if log_graph:
                # graph = wandb.run._torch.hook_torch(model, criterion, graph_idx=global_idx)
                # graphs.append(graph)
                pass
                # NOTE: the graph is set in run.summary by hook_torch on the backward pass
        return graphs

    def add_log_parameters_hook(
            self,
            module: "torch.nn.Module",
            prefix: str = "",
            log_freq: int = 0,
    ) -> None:
        """This instruments hooks into the pytorch module
        log parameters after a forward pass
        log_freq - log gradients/parameters every N batches
        """

        module_full_name = '/'.join(["parameters", prefix])

        if not hasattr(module, "_anyboard_hook_names"):
            module._wandb_hook_names = []

        def parameter_log_hook(module, input_, output, log_track):
            if not log_track_update(log_track):
                return
            for name, parameter in module.named_parameters():
                # for pytorch 0.3 Variables
                var_full_name = '/'.join([module_full_name, name])
                if isinstance(parameter, torch.autograd.Variable):
                    data = parameter.data
                else:
                    data = parameter
                self.log_tensor_stats(data.cpu(), var_full_name, log_track_get_count(log_track))

        log_track_params = log_track_init(log_freq)
        try:
            hook = module.register_forward_hook(
                lambda mod, inp, outp: parameter_log_hook(
                    mod, inp, outp, log_track_params
                )
            )
            self._hook_handles[module_full_name] = hook
            module._wandb_hook_names.append(module_full_name)
        except RuntimeError as e:
            msg = f"Trying to register forward_hook failed ({e}) - skipping parameter tracking."
            logger.warning(msg)

    def add_log_gradients_hook(
            self,
            module: "torch.nn.Module",
            prefix: str = "",
            log_freq: int = 0,
    ) -> None:
        """This instruments hooks into the pytorch module
        log gradients after a backward pass
        log_freq - log gradients/parameters every N batches
        """

        if not hasattr(module, "_wandb_hook_names"):
            module._wandb_hook_names = []

        for name, parameter in module.named_parameters():
            if parameter.requires_grad:
                log_track_grad = log_track_init(log_freq)
                var_full_name = '/'.join(["gradients", prefix, name])
                module._wandb_hook_names.append(var_full_name)
                self._hook_variable_gradient_stats(parameter, var_full_name, log_track_grad)
                # if not isinstance(parameter, torch.autograd.Variable):
                #     cls = type(parameter)
                #     raise TypeError(
                #         f"Expected torch.Variable, not {cls.__module__}.{cls.__name__}"
                #     )
                #
                # handle = self._hook_handles.get(var_full_name)
                # if handle is not None and _torch_hook_handle_is_valid(handle):
                #     raise ValueError(f'A hook has already been set under name "{var_full_name}"')
                #
                # handle = parameter.register_hook(lambda grad: _callback(grad, var_full_name, log_track_grad))
                # self._hook_handles[var_full_name] = handle

    def _hook_variable_gradient_stats(self, var, name, log_track):
        # lamda函数特性：会传引用 -》解决方案：新写此函数保证每个var的name和log_track都被记录，而不是只有最后一个！
        # 让不同的var注册的是不同的hook，而不是同一个hook！
        if not isinstance(var, torch.autograd.Variable):
            cls = type(var)
            raise TypeError(
                f"Expected torch.Variable, not {cls.__module__}.{cls.__name__}"
            )

        handle = self._hook_handles.get(name)
        if handle is not None and _torch_hook_handle_is_valid(handle):
            raise ValueError(f'A hook has already been set under name "{name}"')

        def _callback(grad, name, log_track):
            if not log_track_update(log_track):
                return
            self.log_tensor_stats(grad.data, name, log_track_get_count(log_track))

        handle = var.register_hook(lambda grad: _callback(grad, name, log_track))
        self._hook_handles[name] = handle
        return handle

    def log_tensor_stats(self, tensor, name, step):
        """Add distribution statistics on a tensor's elements to the current History entry"""
        # TODO Handle the case of duplicate names.
        if isinstance(tensor, (tuple, list)):
            while isinstance(tensor, (tuple, list)) and isinstance(tensor[0], (tuple, list)):
                tensor = [item for sublist in tensor for item in sublist]
            tensor = torch.cat([t.detach().clone().reshape(-1) for t in tensor])

        tensor = tensor.detach().clone()
        # checking for inheritance from _TensorBase didn't work for some reason
        if not hasattr(tensor, "shape"):
            cls = type(tensor)
            raise TypeError(f"Expected Tensor, not {cls.__module__}.{cls.__name__}")

        # Sparse tensors have a bunch of implicit zeros. In order to histo them correctly,
        # we have to count them up and add them to the histo ourselves.
        sparse_zeros = None
        if tensor.is_sparse:
            # Have to call this on a sparse tensor before most other ops.
            tensor = tensor.cpu().coalesce()

            backing_values = tensor._values()
            sparse_zeros = tensor.numel() - backing_values.numel()
            tensor = backing_values

        flat = tensor.reshape(-1)

        if flat.is_cuda:
            if self._is_cuda_histc_supported is None:
                try:
                    flat.histc(bins=self._num_bins)
                except RuntimeError:
                    self._is_cuda_histc_supported = False
                else:
                    self._is_cuda_histc_supported = True

            # As of torch 1.0.1.post2+nightly, float16 cuda summary ops are not supported (convert to float32)
            if not self._is_cuda_histc_supported:
                flat = flat.cpu()
            elif not isinstance(flat, (torch.cuda.FloatTensor, torch.cuda.DoubleTensor)):
                flat = flat.type(torch.cuda.FloatTensor)

        # Since we use histc, we need to make sure that torch supports the operation on CPU,
        # otherwise we'll get a runtime error. Hence, we need to upcast to float32.
        if not flat.is_cuda and not isinstance(flat, (torch.FloatTensor, torch.DoubleTensor)):
            flat = flat.type(torch.FloatTensor)

        # Skip logging if all values are nan or inf or the tensor is empty.
        if _no_finite_values(flat):
            return

        # Remove nans and infs if present. There's no good way to represent that in histograms.
        flat = _remove_infs_nans(flat)

        tmin = flat.min().item()
        tmax = flat.max().item()
        if sparse_zeros:
            # If we've got zeros to add in, make sure zero is in the hist range.
            tmin = 0 if tmin > 0 else tmin
            tmax = 0 if tmax < 0 else tmax
        # Anecdotally, this can somehow happen sometimes. Maybe a precision error
        # in min()/max() above. Swap here to prevent a runtime error.
        if tmin > tmax:
            tmin, tmax = tmax, tmin
        tensor = flat.histc(bins=self._num_bins, min=tmin, max=tmax)
        tensor = tensor.cpu().detach().clone()
        bins = torch.linspace(tmin, tmax, steps=self._num_bins + 1)

        # Add back zeroes from a sparse tensor.
        if sparse_zeros:
            bins_np = bins.numpy()
            tensor_np = tensor.numpy()
            bin_idx = 0
            num_buckets = len(bins_np) - 1
            for i in range(num_buckets):
                start = bins_np[i]
                end = bins_np[i + 1]
                # There are 3 cases to consider here, all of which mean we've found the right bucket
                # 1. The bucket range contains zero.
                # 2. The bucket range lower bound *is* zero.
                # 3. This is the last bucket and the bucket range upper bound is zero.
                if (start <= 0 and end > 0) or (i == num_buckets - 1 and end == 0):
                    bin_idx = i
                    break

            tensor_np[bin_idx] += sparse_zeros
            tensor = torch.Tensor(tensor_np)
            bins = torch.Tensor(bins_np)

        bucket_limits = bins.tolist()
        bucket_counts = tensor.tolist()
        bucket_counts.append(0)  # ...
        WriterManager().add_histogram_raw(name, tmin, tmax, len(flat), flat.sum().item(), (flat ** 2).sum().item(),
                                          bucket_limits, bucket_counts, step)

    def unhook_all(self):
        for handle in self._hook_handles.values():
            handle.remove()
        self._hook_handles = []

    def unhook(self, name):
        handle = self._hook_handles.pop(name)
        handle.remove()
