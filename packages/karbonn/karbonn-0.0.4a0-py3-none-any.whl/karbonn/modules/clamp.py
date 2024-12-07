r"""Contain ``torch.nn.Module`` to clamp values."""

from __future__ import annotations

__all__ = ["Clamp"]

import torch


class Clamp(torch.nn.Module):
    r"""Implement a module to clamp all elements in input into the range
    ``[min, max]``.

    Args:
        min: The lower-bound of the range to be clamped to.
            ``None`` means there is no minimum value.
        max: The upper-bound of the range to be clamped to.
            ``None`` means there is no maximum value.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon
    >>> import torch
    >>> from karbonn.modules import Clamp
    >>> m = Clamp(min=-1, max=2)
    >>> m
    Clamp(min=-1, max=2)
    >>> out = m(torch.tensor([[-2.0, -1.0, 0.0], [1.0, 2.0, 3.0]]))
    >>> out
    tensor([[-1., -1.,  0.], [ 1.,  2.,  2.]])

    ```
    """

    def __init__(self, min: float | None = -1.0, max: float | None = 1.0) -> None:  # noqa: A002
        super().__init__()
        self._min = min
        self._max = max

    def extra_repr(self) -> str:
        return f"min={self._min}, max={self._max}"

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.clamp(min=self._min, max=self._max)
