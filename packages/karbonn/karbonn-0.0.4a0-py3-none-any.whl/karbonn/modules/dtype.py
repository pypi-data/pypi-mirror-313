r"""Contain ``torch.nn.Module``s to change tensor's data type."""

from __future__ import annotations

__all__ = ["ToFloat", "ToLong"]

import torch
from torch import nn


class ToFloat(nn.Module):
    r"""Implement a ``torch.nn.Module`` to convert a tensor to a float
    tensor.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon
    >>> import torch
    >>> from karbonn.modules import ToFloat
    >>> m = ToFloat()
    >>> m
    ToFloat()
    >>> out = m(torch.tensor([[2, -1, 0], [1, 2, 3]]))
    >>> out
    tensor([[ 2., -1.,  0.],
            [ 1.,  2.,  3.]])

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.float()


class ToLong(nn.Module):
    r"""Implement a ``torch.nn.Module`` to convert a tensor to a long
    tensor.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon
    >>> import torch
    >>> from karbonn.modules import ToLong
    >>> m = ToLong()
    >>> m
    ToLong()
    >>> out = m(torch.tensor([[2.0, -1.0, 0.0], [1.0, 2.0, 3.0]]))
    >>> out
    tensor([[ 2, -1,  0],
            [ 1,  2,  3]])

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.long()
