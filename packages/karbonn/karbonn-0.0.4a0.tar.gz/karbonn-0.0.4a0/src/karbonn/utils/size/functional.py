r"""Contain functions to easily manage randomness."""

from __future__ import annotations

__all__ = ["find_in_features", "find_out_features"]

from typing import TYPE_CHECKING

from karbonn.utils.size.auto import AutoSizeFinder

if TYPE_CHECKING:
    from torch import nn

_size_finder = AutoSizeFinder()


def find_in_features(module: nn.Module) -> list[int]:
    r"""Find the input feature sizes of a given module.

    Args:
        module: The module.

    Returns:
        The input feature sizes.

    Raises:
        SizeNotFound: if the input feature sizes could not be
            found.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import find_in_features
    >>> module = torch.nn.Linear(4, 6)
    >>> in_features = find_in_features(module)
    >>> in_features
    [4]
    >>> module = torch.nn.Bilinear(in1_features=4, in2_features=6, out_features=8)
    >>> in_features = find_in_features(module)
    >>> in_features
    [4, 6]

    ```
    """
    return _size_finder.find_in_features(module)


def find_out_features(module: nn.Module) -> list[int]:
    r"""Find the output feature sizes of a given module.

    Args:
        module: The module.

    Returns:
        The output feature sizes.

    Raises:
        SizeNotFound: if the output feature sizes could not be
            found.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import find_out_features
    >>> module = torch.nn.Linear(4, 6)
    >>> out_features = find_out_features(module)
    >>> out_features
    [6]
    >>> module = torch.nn.Bilinear(in1_features=4, in2_features=6, out_features=8)
    >>> out_features = find_out_features(module)
    >>> out_features
    [8]

    ```
    """
    return _size_finder.find_out_features(module)
