r"""Define the base class to find the input and output feature sizes."""

from __future__ import annotations

__all__ = ["BaseSizeFinder"]

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from torch import nn

T = TypeVar("T", bound=nn.Module)


class BaseSizeFinder(ABC, Generic[T]):
    r"""Define the base class to find the input or output feature size of
    a module.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import AutoSizeFinder
    >>> size_finder = AutoSizeFinder()
    >>> module = torch.nn.Linear(4, 6)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [6]

    ```
    """

    @abstractmethod
    def find_in_features(self, module: T) -> list[int]:
        r"""Find the input feature sizes of a given module.

        Args:
            module: The module.

        Returns:
            The input feature sizes.

        Raises:
            SizeNotFound: if the input feature size could not be
                found.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.size import AutoSizeFinder
        >>> module = torch.nn.Linear(4, 6)
        >>> size_finder = AutoSizeFinder()
        >>> in_features = size_finder.find_in_features(module)
        >>> in_features
        [4]
        >>> module = torch.nn.Bilinear(in1_features=4, in2_features=6, out_features=8)
        >>> in_features = size_finder.find_in_features(module)
        >>> in_features
        [4, 6]

        ```
        """

    @abstractmethod
    def find_out_features(self, module: T) -> list[int]:
        r"""Find the output feature sizes of a given module.

        Args:
            module: The module.

        Returns:
            The output feature sizes.

        Raises:
            SizeNotFoundError: if the output feature size could not be
                found.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.size import AutoSizeFinder
        >>> module = torch.nn.Linear(4, 6)
        >>> size_finder = AutoSizeFinder()
        >>> out_features = size_finder.find_out_features(module)
        >>> out_features
        [6]
        >>> module = torch.nn.Bilinear(in1_features=4, in2_features=6, out_features=8)
        >>> out_features = size_finder.find_out_features(module)
        >>> out_features
        [8]

        ```
        """


class SizeNotFoundError(Exception):
    r"""Raised if the size could not be found,."""
