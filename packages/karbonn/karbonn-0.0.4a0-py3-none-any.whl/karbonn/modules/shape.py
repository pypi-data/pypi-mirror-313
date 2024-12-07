r"""Contain ``torch.nn.Module``s to change tensor's shape."""

from __future__ import annotations

__all__ = ["MulticlassFlatten", "Squeeze", "View"]

from typing import Any

import torch
from torch import nn

from karbonn.utils import setup_module


class MulticlassFlatten(nn.Module):
    r"""Implement a wrapper to flat the multiclass inputs of a
    ``torch.nn.Module``.

    The input prediction tensor shape is ``(d1, d2, ..., dn, C)``
    and is reshaped to ``(d1 * d2 * ... * dn, C)``.
    The input target tensor shape is ``(d1, d2, ..., dn)``
    and is reshaped to ``(d1 * d2 * ... * dn,)``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import MulticlassFlatten
    >>> m = MulticlassFlatten(torch.nn.CrossEntropyLoss())
    >>> m
    MulticlassFlatten(
      (module): CrossEntropyLoss()
    )
    >>> out = m(torch.ones(6, 2, 4, requires_grad=True), torch.zeros(6, 2, dtype=torch.long))
    >>> out
    tensor(1.3863, grad_fn=<NllLossBackward0>)

    ```
    """

    def __init__(self, module: nn.Module | dict) -> None:
        super().__init__()
        self.module = setup_module(module)

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> Any:
        target = torch.flatten(target)
        return self.module(prediction.view(target.numel(), prediction.shape[-1]), target)


class Squeeze(nn.Module):
    r"""Implement a ``torch.nn.Module`` to squeeze the input tensor.

    Args:
        dim: The dimension to squeeze the input tensor. If ``None``,
            all the dimensions of the input tensor of size 1 are
            removed.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import Squeeze
    >>> m = Squeeze()
    >>> m
    Squeeze(dim=None)
    >>> out = m(torch.ones(2, 1, 3, 1))
    >>> out.shape
    torch.Size([2, 3])

    ```
    """

    def __init__(self, dim: int | None = None) -> None:
        super().__init__()
        self._dim = dim

    def extra_repr(self) -> str:
        return f"dim={self._dim}"

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        if self._dim is None:
            return input.squeeze()
        return input.squeeze(self._dim)


class View(nn.Module):
    r"""Implement a ``torch.nn.Module`` to return a new tensor with the
    same data as the input tensor but of a different shape.

    Args:
        shape: The desired shape.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import View
    >>> m = View(shape=(-1, 2, 3))
    >>> m
    View(shape=(-1, 2, 3))
    >>> out = m(torch.ones(4, 5, 2, 3))
    >>> out.shape
    torch.Size([20, 2, 3])

    ```
    """

    def __init__(self, shape: tuple[int, ...] | list[int]) -> None:
        super().__init__()
        self._shape = tuple(shape)

    def extra_repr(self) -> str:
        return f"shape={self._shape}"

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.view(*self._shape)
