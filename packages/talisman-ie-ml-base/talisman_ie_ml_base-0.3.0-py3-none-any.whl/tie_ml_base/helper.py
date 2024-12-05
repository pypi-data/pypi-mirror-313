from dataclasses import dataclass, fields
from typing import Any, Sequence, TypeVar

import numpy as np
import torch
from torch import Tensor


def fill_roll_np(arr: np.ndarray, *, shift: int, fill: Any) -> np.ndarray:
    rolled = np.roll(arr, shift=shift)
    if shift > 0:
        rolled[:shift] = fill
    if shift < 0:
        rolled[shift:] = fill
    return rolled


def fill_roll(arr: Tensor, *, shift: int, fill: Any) -> Tensor:
    rolled = torch.roll(arr, shifts=shift)
    if shift > 0:
        rolled[:shift] = fill
    if shift < 0:
        rolled[shift:] = fill
    return rolled


def one_hot(arr: np.ndarray, *, num_classes: int, dtype: object = int) -> np.ndarray:
    incorrect_mask = ((arr >= num_classes) | (arr < 0))
    if incorrect_mask.any():
        incorrect_values = set(arr[incorrect_mask])
        raise ValueError(
            f'Cannot create one-hot vector (num_classes={num_classes}) from array with the following values present: {incorrect_values}!'
        )

    out = np.zeros((arr.size, num_classes), dtype=dtype)
    out[np.arange(arr.size), arr.ravel()] = 1
    out.shape = arr.shape + (num_classes,)
    return out


def pad_sequence(sequence: Sequence[np.ndarray], *, padding_value: Any) -> np.ndarray:
    padded_size = max(map(len, sequence))

    def padder(arr: np.ndarray) -> np.ndarray:
        pad_shape = [[0, 0] for _ in arr.shape]
        pad_shape[0][-1] = padded_size - len(arr)
        return np.pad(arr, pad_shape, 'constant', constant_values=padding_value)

    return np.stack(tuple(map(padder, sequence)))


def safe_concat(arrays: Sequence[np.ndarray], *, dtype: object) -> np.ndarray:
    if len(arrays):
        return np.concatenate(arrays)
    return np.empty(0, dtype=dtype)


@dataclass
class TupleLike:
    def __iter__(self):  # so it behaves like a NamedTuple
        return iter(self.as_tuple())

    def as_tuple(self):
        return tuple(self.__getattribute__(field.name) for field in fields(self))


_TensorStorage = TypeVar('_TensorStorage', bound='TensorStorage')


class TensorStorage:

    def to(self: _TensorStorage, device: torch.device) -> _TensorStorage:
        for field in fields(self):
            value = self.__getattribute__(field.name)
            if torch.is_tensor(value):
                self.__setattr__(field.name, value.to(device))
        return self
