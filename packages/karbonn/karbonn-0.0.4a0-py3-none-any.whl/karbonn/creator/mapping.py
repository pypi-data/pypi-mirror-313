r"""Contain object creator implementations."""

from __future__ import annotations

__all__ = ["DictCreator"]

from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from karbonn.creator.base import BaseCreator, setup_creator

if TYPE_CHECKING:
    from collections.abc import Mapping

T = TypeVar("T")


class DictCreator(BaseCreator[dict[Hashable, T]]):
    r"""Implement a list object creator.

    Args:
        creators: The mapping of object creators or their
            configurations.

    Example usage:

    ```pycon

    >>> from karbonn.creator import DictCreator, Creator
    >>> creator = DictCreator(
    ...     {
    ...         "key1": Creator(
    ...             {
    ...                 "_target_": "torch.nn.Linear",
    ...                 "in_features": 4,
    ...                 "out_features": 6,
    ...             }
    ...         ),
    ...         "key2": Creator({"_target_": "torch.nn.Identity"}),
    ...     }
    ... )
    >>> creator
    DictCreator(
      (key1): Creator(
          (_target_): torch.nn.Linear
          (in_features): 4
          (out_features): 6
        )
      (key2): Creator(
          (_target_): torch.nn.Identity
        )
    )
    >>> creator.create()
    {'key1': Linear(in_features=4, out_features=6, bias=True), 'key2': Identity()}

    ```
    """

    def __init__(self, creators: Mapping[Hashable, BaseCreator[T] | dict]) -> None:
        self._creators = {key: setup_creator(creator) for key, creator in creators.items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(self._creators))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self._creators))}\n)"

    def create(self) -> dict[Hashable, T]:
        return {key: creator.create() for key, creator in self._creators.items()}
