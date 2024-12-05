from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, AsyncContextManager

import torch
from torch.nn import Module
from typing_extensions import Self

from tp_interfaces.serializable import DirectorySerializableMixin
from tp_interfaces.serializable.pickle_mixin import PicklableMixin

DEFAULT_PREFERRED_DEVICE = 'cuda'


class TorchModule(Module, AsyncContextManager, metaclass=ABCMeta):

    def __init__(self, preferred_device: str | torch.device = None):
        super().__init__()
        self._preferred_device = preferred_device or DEFAULT_PREFERRED_DEVICE

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def device(self) -> torch.device:
        try:
            return next(self.parameters()).device
        except StopIteration:
            return torch.device(self._preferred_device)

    @property
    def preferred_device(self) -> torch.device:
        return torch.device(self._preferred_device)

    @abstractmethod
    def forward(self, *args, **kwargs) -> Any:
        pass


class PicklableTorchModule(TorchModule, PicklableMixin, metaclass=ABCMeta):

    def save(self, path: Path, *, rewrite: bool = False) -> None:
        previous_device = self.device
        self.cpu()
        super(PicklableTorchModule, self).save(path, rewrite=rewrite)
        self.to(device=torch.device(previous_device))


class DirectorySerializableTorchModule(TorchModule, DirectorySerializableMixin, metaclass=ABCMeta):
    """
    Base class for torch modules with implementation for serialization and deserialization in directory.
    It uses base strategy for object storing, but also saves weights

    @note this mixin should be initialized before torch model is built
    """

    def __init__(self):
        TorchModule.__init__(self)
        DirectorySerializableMixin.__init__(self)

    @classmethod
    def _load_from_directory(cls, directory_path: Path, info: dict) -> Self:
        model = super()._load_from_directory(directory_path, info)
        if not isinstance(model, DirectorySerializableTorchModule):
            raise ValueError
        model.load_state_dict(torch.load(directory_path / 'weights.pt'), strict=False)
        return model

    def _save_to_directory(self, directory_path: Path) -> None:
        super()._save_to_directory(directory_path)

        state_dict = self.state_dict()
        for name, (value, _, _) in self._serializable.items():
            if isinstance(value, TorchModule):  # assume it was saved with parameters
                for param in value.state_dict():
                    state_dict.pop(f'_{name}.{param}', None)

        torch.save(state_dict, directory_path / 'weights.pt')
