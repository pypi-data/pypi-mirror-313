r"""Contain aggregation fusion modules."""

from __future__ import annotations

__all__ = ["AverageFusion", "MultiplicationFusion", "SumFusion"]

import torch
from torch import nn


class MultiplicationFusion(nn.Module):
    r"""Implement a fusion layer that multiplies the inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import MultiplicationFusion
    >>> module = MultiplicationFusion()
    >>> module
    MultiplicationFusion()
    >>> x1 = torch.tensor([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]], requires_grad=True)
    >>> x2 = torch.tensor([[12.0, 13.0, 14.0], [15.0, 16.0, 17.0]], requires_grad=True)
    >>> out = module(x1, x2)
    >>> out
    tensor([[ 24.,  39.,  56.],
            [ 75.,  96., 119.]], grad_fn=<MulBackward0>)
    >>> out.mean().backward()

    ```
    """

    def forward(self, *inputs: torch.Tensor) -> torch.Tensor:
        if not inputs:
            msg = f"{self.__class__.__qualname__} needs at least one tensor as input"
            raise RuntimeError(msg)
        output = inputs[0]
        for xi in inputs[1:]:
            output = output.mul(xi)
        return output


class SumFusion(nn.Module):
    r"""Implement a layer to sum the inputs.

    Args:
        normalized: The output is normalized by the number of inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import SumFusion
    >>> module = SumFusion()
    >>> module
    SumFusion(normalized=False)
    >>> x1 = torch.tensor([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]], requires_grad=True)
    >>> x2 = torch.tensor([[12.0, 13.0, 14.0], [15.0, 16.0, 17.0]], requires_grad=True)
    >>> out = module(x1, x2)
    >>> out
    tensor([[14., 16., 18.],
            [20., 22., 24.]], grad_fn=<AddBackward0>)
    >>> out.mean().backward()

    ```
    """

    def __init__(self, normalized: bool = False) -> None:
        super().__init__()
        self._normalized = bool(normalized)

    def extra_repr(self) -> str:
        return f"normalized={self._normalized}"

    def forward(self, *inputs: torch.Tensor) -> torch.Tensor:
        if not inputs:
            msg = f"{self.__class__.__qualname__} needs at least one tensor as input"
            raise RuntimeError(msg)

        output = inputs[0]
        for x in inputs[1:]:
            output = output.add(x)

        if self._normalized:
            output = output.div(len(inputs))
        return output


class AverageFusion(SumFusion):
    r"""Implement a layer to average the inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import AverageFusion
    >>> module = AverageFusion()
    >>> module
    AverageFusion(normalized=True)
    >>> x1 = torch.tensor([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]], requires_grad=True)
    >>> x2 = torch.tensor([[12.0, 13.0, 14.0], [15.0, 16.0, 17.0]], requires_grad=True)
    >>> out = module(x1, x2)
    >>> out
    tensor([[ 7.,  8.,  9.],
            [10., 11., 12.]], grad_fn=<DivBackward0>)
    >>> out.mean().backward()

    ```
    """

    def __init__(self) -> None:
        super().__init__(normalized=True)
