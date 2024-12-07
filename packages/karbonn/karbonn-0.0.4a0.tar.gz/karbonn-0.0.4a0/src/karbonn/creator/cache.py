r"""Contain a simple object creator implementation."""

from __future__ import annotations

__all__ = ["CacheCreator"]

import copy
from typing import TypeVar

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from karbonn.creator.base import BaseCreator, setup_creator

T = TypeVar("T")


class CacheCreator(BaseCreator[T]):
    r"""Implement a simple object creator that caches the value after the
    first creation.

    Args:
        creator: The object creator or its configuration.
        copy: If ``True``, it returns a copy of the created object.

    Example usage:

    ```pycon

    >>> from karbonn.creator import Creator, CacheCreator
    >>> creator = CacheCreator(
    ...     Creator(
    ...         {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         }
    ...     )
    ... )
    >>> creator
    CacheCreator(
      (creator): Creator(
          (_target_): torch.nn.Linear
          (in_features): 4
          (out_features): 6
        )
      (copy): True
      (is_initialized): False
      (value): None
    )
    >>> creator.create()
    Linear(in_features=4, out_features=6, bias=True)
    >>> creator
    CacheCreator(
      (creator): Creator(
          (_target_): torch.nn.Linear
          (in_features): 4
          (out_features): 6
        )
      (copy): True
      (is_initialized): True
      (value): Linear(in_features=4, out_features=6, bias=True)
    )

    ```
    """

    def __init__(self, creator: BaseCreator[T] | dict, copy: bool = True) -> None:
        self._creator = setup_creator(creator)
        self._copy = bool(copy)

        self._is_initialized = False
        self._value = None

    def __repr__(self) -> str:
        config = {
            "creator": self._creator,
            "copy": self._copy,
            "is_initialized": self._is_initialized,
            "value": self._value,
        }
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(config))}\n)"

    def __str__(self) -> str:
        config = {"creator": self._creator, "copy": self._copy}
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(config))}\n)"

    def create(self) -> T:
        if not self._is_initialized:
            self._value = self._creator.create()
            self._is_initialized = True
        if self._copy:
            return copy.deepcopy(self._value)
        return self._value
