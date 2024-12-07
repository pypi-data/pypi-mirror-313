r"""Contain concatenation fusion modules."""

from __future__ import annotations

__all__ = ["ConcatFusion"]

import torch
from torch import nn


class ConcatFusion(nn.Module):
    r"""Implement a module to concatenate inputs.

    Args:
        dim: The fusion dimension. ``-1`` means the last dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import ConcatFusion
    >>> module = ConcatFusion()
    >>> module
    ConcatFusion(dim=-1)
    >>> x1 = torch.tensor([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]], requires_grad=True)
    >>> x2 = torch.tensor([[12.0, 13.0, 14.0], [15.0, 16.0, 17.0]], requires_grad=True)
    >>> out = module(x1, x2)
    >>> out
    tensor([[ 2.,  3.,  4., 12., 13., 14.],
            [ 5.,  6.,  7., 15., 16., 17.]], grad_fn=<CatBackward0>)
    >>> out.mean().backward()

    ```
    """

    def __init__(self, dim: int = -1) -> None:
        super().__init__()
        self._dim = dim

    def extra_repr(self) -> str:
        return f"dim={self._dim}"

    def forward(self, *inputs: torch.Tensor) -> torch.Tensor:
        if not inputs:
            msg = f"{self.__class__.__qualname__} needs at least one tensor as input"
            raise RuntimeError(msg)
        return torch.cat(inputs, dim=self._dim)
