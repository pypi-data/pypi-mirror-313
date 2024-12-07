r"""Contain a size finder for ``torch.nn.Linear`` layer or similar
layers."""

from __future__ import annotations

__all__ = ["SequentialSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError
from karbonn.utils.size.functional import find_in_features, find_out_features


class SequentialSizeFinder(BaseSizeFinder[nn.Sequential]):
    r"""Implement a size finder for ``torch.nn.Sequential`` layer.

    This module size finder iterates over the child modules until to
    find one where it can compute the size.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import SequentialSizeFinder
    >>> size_finder = SequentialSizeFinder()
    >>> module = torch.nn.Sequential(
    ...     torch.nn.Linear(4, 6), torch.nn.ReLU(), torch.nn.Linear(6, 8)
    ... )
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [8]

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def find_in_features(self, module: nn.Sequential) -> list[int]:
        for child in module:
            try:
                return find_in_features(child)
            except SizeNotFoundError:  # noqa: PERF203
                pass
        msg = "cannot find the input feature sizes because the child modules are not supported"
        raise SizeNotFoundError(msg)

    def find_out_features(self, module: nn.Sequential) -> list[int]:
        for child in module[::-1]:
            try:
                return find_out_features(child)
            except SizeNotFoundError:  # noqa: PERF203
                pass
        msg = "cannot find the output feature sizes because the child modules are not supported"
        raise SizeNotFoundError(msg)
