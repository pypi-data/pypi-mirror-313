r"""Contain the implementation of a residual block."""

from __future__ import annotations

__all__ = ["ResidualBlock"]


import torch
from torch import nn

from karbonn.utils import setup_module


class ResidualBlock(nn.Module):
    r"""Implementation of a residual block.

    Args:
        residual: The residual mapping module or its configuration
            (dictionary).
        skip: The skip mapping module or its configuration
            (dictionary). If ``None``, the ``Identity`` module is used.

    Example usage:

    ```pycon
    >>> import torch
    >>> from torch import nn
    >>> from karbonn.modules import ResidualBlock
    >>> m = ResidualBlock(residual=nn.Sequential(nn.Linear(4, 6), nn.ReLU(), nn.Linear(6, 4)))
    >>> m
    ResidualBlock(
      (residual): Sequential(
        (0): Linear(in_features=4, out_features=6, bias=True)
        (1): ReLU()
        (2): Linear(in_features=6, out_features=4, bias=True)
      )
      (skip): Identity()
    )
    >>> out = m(torch.rand(6, 4))
    >>> out
    tensor([[...]], grad_fn=<AddBackward0>)

    ```
    """

    def __init__(
        self,
        residual: nn.Module | dict,
        skip: nn.Module | dict | None = None,
    ) -> None:
        super().__init__()
        self.residual = setup_module(residual)
        self.skip = setup_module(skip or nn.Identity())

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return self.skip(input) + self.residual(input)
