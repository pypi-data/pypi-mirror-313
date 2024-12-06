"""Torch implementation of the TensorTree library
"""

import numpy as np
import torch

from .core import General_Impl


class Torch_Impl(General_Impl):
    """Specialize torch operations"""

    def __init__(self, device):
        super().__init__(torch, "dim")
        self.device = device

    def zeros(self, *args, **kwargs) -> torch.Tensor:
        kwargs["device"] = self.device
        return torch.zeros(*args, **kwargs)

    def ones(self, *args, **kwargs) -> torch.Tensor:
        kwargs["device"] = self.device
        return torch.ones(*args, **kwargs)

    @staticmethod
    def copy(data: torch.Tensor) -> torch.Tensor:
        return data.clone()

    @staticmethod
    def shape(data: torch.Tensor) -> torch.Tensor:
        return data.size()

    @staticmethod
    def to_numpy(data: torch.Tensor) -> np.array:
        chunk = data.cpu().detach()
        if isinstance(chunk, torch.masked.MaskedTensor):
            return np.ma.array(
                chunk._masked_data.numpy(), mask=~chunk._masked_mask.numpy()
            )
        elif isinstance(chunk, torch.Tensor):
            return chunk.numpy()
        else:
            raise ValueError("Non handable tensor instance!")

    def array(self, *args, **kwargs):
        kwargs["device"] = self.device
        return torch.tensor(*args, **kwargs)

    @staticmethod
    def masked_array(data, mask, *args, **kwargs):
        return torch.masked.masked_tensor(data, ~mask, *args, **kwargs)

    @staticmethod
    def mean(data: torch.Tensor, axis) -> torch.Tensor:
        return data.mean(dim=axis)

    @staticmethod
    def repeat(data: torch.Tensor, *args):
        return data.repeat(*args)

    @staticmethod
    def all(data: torch.Tensor, axis) -> torch.Tensor:
        return torch.all(data, axis)

    @staticmethod
    def any(data: torch.Tensor, axis) -> torch.Tensor:
        return torch.any(data, axis)
