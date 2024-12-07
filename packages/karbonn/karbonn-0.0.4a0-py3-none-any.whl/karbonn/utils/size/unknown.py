r"""Contain a size finder for ``torch.nn.Linear`` layer or similar
layers."""

from __future__ import annotations

__all__ = ["UnknownSizeFinder"]


from typing import TYPE_CHECKING, NoReturn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError

if TYPE_CHECKING:
    from torch import nn


class UnknownSizeFinder(BaseSizeFinder):
    r"""Implement a size finder for the modules where the input and
    output feature sizes are unknown.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import UnknownSizeFinder
    >>> size_finder = UnknownSizeFinder()
    >>> module = torch.nn.ReLU()
    >>> in_features = size_finder.find_in_features(module)  # doctest: +SKIP
    >>> out_features = size_finder.find_out_features(module)  # doctest: +SKIP

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def find_in_features(self, module: nn.Module) -> NoReturn:
        msg = f"cannot find the input feature sizes of {module}"
        raise SizeNotFoundError(msg)

    def find_out_features(self, module: nn.Module) -> NoReturn:
        msg = f"cannot find the output feature sizes of {module}"
        raise SizeNotFoundError(msg)
