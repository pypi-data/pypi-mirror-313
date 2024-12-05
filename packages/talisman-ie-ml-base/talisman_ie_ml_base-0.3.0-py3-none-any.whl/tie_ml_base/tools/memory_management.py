import gc
import inspect
import logging
from functools import wraps
from os import environ
from random import shuffle
from time import sleep
from typing import Any, Callable, Optional, Tuple

import torch
from pynvml import NVMLError, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlDeviceGetUtilizationRates, nvmlInit
from torch.nn import Module

from talisman_tools.helper.log_tools import warn_once
from tie_ml_base.env import get_gpu_oom_repeat_limit, get_gpu_oom_timeout, get_gpu_utilization_limit
from tie_ml_base.torch_wrapper import TorchModule

logger = logging.getLogger(__name__)
try:
    nvmlInit()
    nvml_loaded = True
except NVMLError as nvml_error:
    logger.warning(f'Failed to load NVML library: {nvml_error}')
    nvml_loaded = False


def model_bytes(model: TorchModule) -> int:
    """Returns model size in bytes."""
    param_size = 0
    for param in model.parameters():
        param_size += param.nelement() * param.element_size()

    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()

    return param_size + buffer_size


def get_real_device_id(torch_device_id: int) -> int:
    visible_devices = environ.get('CUDA_VISIBLE_DEVICES')
    if visible_devices is None:
        return torch_device_id

    visible_devices = list(map(int, visible_devices.split(',')))
    real_device_ids = list(range(len(visible_devices)))
    device_mapping = dict(zip(real_device_ids, visible_devices))

    return device_mapping[torch_device_id]


def get_cuda_device_with_most_memory() -> Tuple[Optional[int], int]:
    """Returns CUDA device with most memory, as well as the available memory on the device in bytes."""
    most_unoccupied = 0
    target_gpu_id = None

    if not nvml_loaded:
        warn_once(logger, 'NVML library is not loaded, no information about global state of GPU is available! '
                          'This may lead to suboptimal choice of the GPU.')

    devices = list(range(torch.cuda.device_count()))
    shuffle(devices)
    for device_id in devices:
        total_bytes = torch.cuda.get_device_properties(device_id).total_memory
        allocated_bytes = torch.cuda.memory_allocated(device_id)
        reserved_bytes = torch.cuda.memory_reserved(device_id)

        if nvml_loaded:
            nvml_device_id = get_real_device_id(device_id)
            device_handle = nvmlDeviceGetHandleByIndex(nvml_device_id)

            gpu_utilization = nvmlDeviceGetUtilizationRates(device_handle).gpu / 100.0
            if gpu_utilization > get_gpu_utilization_limit():
                continue

            used_bytes = nvmlDeviceGetMemoryInfo(device_handle).used
            cached_bytes = reserved_bytes - allocated_bytes  # torch caches memory without using it
            available_bytes = total_bytes - (used_bytes - cached_bytes)  # used memory includes cached torch memory
        else:
            available_bytes = total_bytes - allocated_bytes  # does not include information about other processes

        if available_bytes > most_unoccupied:
            most_unoccupied = available_bytes
            target_gpu_id = device_id

    return target_gpu_id, most_unoccupied


def torch_device_handler(f: Callable):
    """Attempts to call the function with the most vacant GPU as a default CUDA device. Repeats until GPU_OOM_REPEAT_LIMIT is reached."""
    def wrapper(*args, **kwargs):
        timeout = get_gpu_oom_timeout()
        repeats = 0

        while True:
            repeats += 1
            try:
                device_id, _ = get_cuda_device_with_most_memory()
                if device_id is None:
                    logger.warning(f'No device is available! Repeating after {timeout} seconds!')
                    sleep(timeout)
                    continue

                with torch.cuda.device(device_id):
                    return f(*args, **kwargs)
            except RuntimeError as e:
                if repeats > get_gpu_oom_repeat_limit():
                    raise RuntimeError('GPU_OOM_REPEAT_LIMIT is reached! Consider either raising the limit or the GPU_OOM_TIMEOUT!')

                logger.warning(f'Caught runtime error while calling function {f}. Repeating after {timeout} seconds!', exc_info=e)
                sleep(timeout)

    if not torch.cuda.is_available():
        logger.warning(f'No CUDA devices available on your system!')
        return f

    return wrapper


def cuda_handler_cleanup(self: TorchModule, e: RuntimeError, f: Callable[[Module, Any], Any]):
    logger.error(f'Caught runtime error while calling async function {f}. Moving {self.__class__.__name__} to CPU!', exc_info=e)
    del e
    self.cpu()
    gc.collect()
    torch.cuda.empty_cache()


def cuda_handler(f: Callable[[Module, Any], Any]):
    """Attempts to place the model (the first argument of the function f) on GPU before calling the function.
    See `try_place_on_cuda` for GPU placement criteria."""
    @wraps(f)
    async def async_wrapper(self: TorchModule, *args, **kwargs):
        if self.preferred_device == torch.device('cpu'):
            warn_once(logger, f'{self.__class__.__name__} preferred device is set to CPU, keeping it on CPU!')
            return await f(self, *args, **kwargs)
        try:
            try_place_on_cuda(self)
            return await f(self, *args, **kwargs)
        except RuntimeError as e:
            cuda_handler_cleanup(self, e, f)
            return await f(self, *args, **kwargs)

    @wraps(f)
    def sync_wrapper(self: TorchModule, *args, **kwargs):
        if self.preferred_device == torch.device('cpu'):
            warn_once(logger, f'{self.__class__.__name__} preferred device is set to CPU, keeping it on CPU!')
            return f(self, *args, **kwargs)
        try:
            try_place_on_cuda(self)
            return f(self, *args, **kwargs)
        except RuntimeError as e:
            cuda_handler_cleanup(self, e, f)
            return f(self, *args, **kwargs)

    if inspect.iscoroutinefunction(f) or inspect.isasyncgenfunction(f):
        return async_wrapper
    return sync_wrapper


def try_place_on_cuda(model: TorchModule):
    """Places model on a GPU if the following criteria are met:
    1. There are GPU devices that are visible.
    2. Model is not already on GPU.
    3. There are enough memory to fit model on GPU.

    If any of these criteria are not satisfied or RuntimeError occurred during model placement on GPU,
    model will be placed on CPU.
    """
    if not torch.cuda.is_available():
        return  # no cuda is available

    if model.device.type == 'cuda':
        return  # model is already on cuda

    device_id, available_memory = get_cuda_device_with_most_memory()
    if available_memory < model_bytes(model) or device_id is None:
        return  # not enough memory available on GPU

    logger.warning(f'Found GPU devices available: {torch.cuda.device_count()}. Placing {model.__class__.__name__} on GPU!')
    try:
        device = torch.device(f'cuda:{device_id}')
        model.to(device)
        logger.warning(f'{model.__class__.__name__} is successfully placed on {model.device}.')
    except RuntimeError as e:
        logger.error(f'Caught runtime error while placing {model.__class__.__name__} on GPU. '
                     f'Moving {model.__class__.__name__} to CPU!', exc_info=e)
        del e

        model.cpu()
        gc.collect()
        torch.cuda.empty_cache()
