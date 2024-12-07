r"""Contain the Snake activation module."""

from __future__ import annotations

__all__ = ["Snake"]

from typing import TYPE_CHECKING

from torch import nn

if TYPE_CHECKING:
    import torch


class Snake(nn.Module):
    r"""Implement the Snake activation layer.

    Snake was proposed in the following paper:

        Neural Networks Fail to Learn Periodic Functions and How to Fix It.
        Ziyin L., Hartwig T., Ueda M.
        NeurIPS, 2020. (http://arxiv.org/pdf/2006.08195)

    Args:
        frequency: The frequency.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import Snake
    >>> m = Snake()
    >>> m
    Snake(frequency=1.0)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[0.0000, 1.7081, 2.8268, 3.0199],
            [4.5728, 5.9195, 6.0781, 7.4316]])

    ```
    """

    def __init__(self, frequency: float = 1.0) -> None:
        super().__init__()
        self._frequency = float(frequency)

    def extra_repr(self) -> str:
        return f"frequency={self._frequency}"

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        two_freq = 2 * self._frequency
        return input - input.mul(two_freq).cos().div(two_freq) + 1 / two_freq
