from functools import wraps
from typing import Any, Callable

import torch
from torch import amp

from tie_ml_base.env import get_amp_optimize
from tie_ml_base.torch_wrapper import PicklableTorchModule


def optimize(f: Callable[[PicklableTorchModule, Any], Any]):
    @wraps(f)
    @torch.no_grad()
    def amp_wrapper(self: PicklableTorchModule, *args, **kwargs):
        if self.device.type == 'cuda' and get_amp_optimize():  # for some reason AMP with CPU is very slow
            with amp.autocast(device_type='cuda'):
                return f(self, *args, **kwargs)
        return f(self, *args, **kwargs)
    return amp_wrapper
