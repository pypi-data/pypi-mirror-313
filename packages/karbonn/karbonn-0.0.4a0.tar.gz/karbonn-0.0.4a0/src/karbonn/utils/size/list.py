r"""Contain a size finder for ``torch.nn.ModuleList`` layer or similar
layers."""

from __future__ import annotations

__all__ = ["ModuleListSizeFinder"]


import contextlib

from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError
from karbonn.utils.size.functional import find_in_features, find_out_features


class ModuleListSizeFinder(BaseSizeFinder[nn.ModuleList]):
    r"""Implement a size finder for ``torch.nn.ModuleList`` layer or
    similar layers.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import ModuleListSizeFinder
    >>> size_finder = ModuleListSizeFinder()
    >>> module = nn.ModuleList(
    ...     [nn.Linear(4, 6), nn.ReLU(), nn.LSTM(input_size=4, hidden_size=6)]
    ... )
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [6]

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def find_in_features(self, module: nn.ModuleList) -> list[int]:
        sizes = set()
        for child in module:
            with contextlib.suppress(SizeNotFoundError):
                sizes.add(tuple(find_in_features(child)))
            if len(sizes) > 1:
                break
        if len(sizes) == 1:
            return list(sizes.pop())
        if len(sizes) == 0:
            msg = (
                "cannot find the input feature sizes because the indexed modules are not supported"
            )
            raise SizeNotFoundError(msg)
        msg = "cannot find the input feature sizes because the indexed modules have different sizes"
        raise SizeNotFoundError(msg)

    def find_out_features(self, module: nn.ModuleList) -> list[int]:
        sizes = set()
        for child in module:
            with contextlib.suppress(SizeNotFoundError):
                sizes.add(tuple(find_out_features(child)))
            if len(sizes) > 1:
                break
        if len(sizes) == 1:
            return list(sizes.pop())
        if len(sizes) == 0:
            msg = (
                "cannot find the output feature sizes because the indexed modules are not supported"
            )
            raise SizeNotFoundError(msg)
        msg = (
            "cannot find the output feature sizes because the indexed modules have different sizes"
        )
        raise SizeNotFoundError(msg)
