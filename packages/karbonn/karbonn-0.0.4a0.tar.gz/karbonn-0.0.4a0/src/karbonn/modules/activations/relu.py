r"""Contain relu-like activation modules."""

from __future__ import annotations

__all__ = ["ReLUn", "SquaredReLU"]

from typing import TYPE_CHECKING

from torch import nn
from torch.nn import functional

if TYPE_CHECKING:
    import torch


class ReLUn(nn.Module):
    r"""Implement the ReLU-n module.

    The ReLU-n equation is: ``ReLUn(x, n)=min(max(0,x),n)``

    Args:
        max: The maximum value a.k.a. ``n`` in the equation above.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import ReLUn
    >>> m = ReLUn(max=5)
    >>> m
    ReLUn(max=5.0)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[0., 1., 2., 3.],
            [4., 5., 5., 5.]])

    ```
    """

    def __init__(self, max: float = 1.0) -> None:  # noqa: A002
        super().__init__()
        self._max = float(max)

    def extra_repr(self) -> str:
        return f"max={self._max}"

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.clamp(min=0.0, max=self._max)


class SquaredReLU(nn.Module):
    r"""Implement the Squared ReLU.

    Squared ReLU is defined in the following paper:

        Primer: Searching for Efficient Transformers for Language Modeling.
        So DR., Mańke W., Liu H., Dai Z., Shazeer N., Le QV.
        NeurIPS, 2021. (https://arxiv.org/pdf/2109.08668.pdf)

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import SquaredReLU
    >>> m = SquaredReLU()
    >>> m
    SquaredReLU()
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[ 0.,  1.,  4.,  9.],
            [16., 25., 36., 49.]])

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        x = functional.relu(input)
        return x * x
