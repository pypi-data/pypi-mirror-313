r"""Contain object creator implementations."""

from __future__ import annotations

__all__ = ["CreatorList", "CreatorTuple", "ListCreator", "TupleCreator"]

from typing import TYPE_CHECKING, TypeVar

from coola.utils import repr_indent, repr_sequence, str_indent, str_sequence

from karbonn.creator.base import BaseCreator, setup_creator
from karbonn.utils.factory import setup_object

if TYPE_CHECKING:
    from collections.abc import Sequence

T = TypeVar("T")


class CreatorList(BaseCreator[T]):
    r"""Implement a list object creator.

    Args:
        items: The sequence of objects or their configurations.

    Example usage:

    ```pycon

    >>> from karbonn.creator import CreatorList
    >>> creator = CreatorList(
    ...     [
    ...         {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         },
    ...         {"_target_": "torch.nn.Identity"},
    ...     ]
    ... )
    >>> creator
    CreatorList(
      (0): {'_target_': 'torch.nn.Linear', 'in_features': 4, 'out_features': 6}
      (1): {'_target_': 'torch.nn.Identity'}
    )
    >>> creator.create()
    [Linear(in_features=4, out_features=6, bias=True), Identity()]

    ```
    """

    def __init__(self, items: Sequence[T | dict]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_sequence(self._items))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_sequence(self._items))}\n)"

    def create(self) -> list[T]:
        return [setup_object(item) for item in self._items]


class CreatorTuple(BaseCreator[T]):
    r"""Implement a tuple object creator.

    Args:
        items: The sequence of objects or their configurations.

    Example usage:

    ```pycon

    >>> from karbonn.creator import CreatorTuple
    >>> creator = CreatorTuple(
    ...     [
    ...         {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         },
    ...         {"_target_": "torch.nn.Identity"},
    ...     ]
    ... )
    >>> creator
    CreatorTuple(
      (0): {'_target_': 'torch.nn.Linear', 'in_features': 4, 'out_features': 6}
      (1): {'_target_': 'torch.nn.Identity'}
    )
    >>> creator.create()
    (Linear(in_features=4, out_features=6, bias=True), Identity())

    ```
    """

    def __init__(self, items: Sequence[T | dict]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_sequence(self._items))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_sequence(self._items))}\n)"

    def create(self) -> tuple[T, ...]:
        return tuple(setup_object(item) for item in self._items)


class ListCreator(BaseCreator[T]):
    r"""Implement a list object creator.

    Args:
        creators: The sequence of object creators or their
            configurations.

    Example usage:

    ```pycon

    >>> from karbonn.creator import ListCreator, Creator
    >>> creator = ListCreator(
    ...     [
    ...         Creator(
    ...             {
    ...                 "_target_": "torch.nn.Linear",
    ...                 "in_features": 4,
    ...                 "out_features": 6,
    ...             }
    ...         ),
    ...         Creator({"_target_": "torch.nn.Identity"}),
    ...     ]
    ... )
    >>> creator
    ListCreator(
      (0): Creator(
          (_target_): torch.nn.Linear
          (in_features): 4
          (out_features): 6
        )
      (1): Creator(
          (_target_): torch.nn.Identity
        )
    )
    >>> creator.create()
    [Linear(in_features=4, out_features=6, bias=True), Identity()]

    ```
    """

    def __init__(self, creators: Sequence[BaseCreator[T] | dict]) -> None:
        self._creators = tuple(setup_creator(creator) for creator in creators)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_sequence(self._creators))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_sequence(self._creators))}\n)"

    def create(self) -> list[T]:
        return [creator.create() for creator in self._creators]


class TupleCreator(BaseCreator[T]):
    r"""Implement a tuple object creator.

    Args:
        creators: The sequence of object creators or their
            configurations.

    Example usage:

    ```pycon

    >>> from karbonn.creator import TupleCreator, Creator
    >>> creator = TupleCreator(
    ...     [
    ...         Creator(
    ...             {
    ...                 "_target_": "torch.nn.Linear",
    ...                 "in_features": 4,
    ...                 "out_features": 6,
    ...             }
    ...         ),
    ...         Creator({"_target_": "torch.nn.Identity"}),
    ...     ]
    ... )
    >>> creator
    TupleCreator(
      (0): Creator(
          (_target_): torch.nn.Linear
          (in_features): 4
          (out_features): 6
        )
      (1): Creator(
          (_target_): torch.nn.Identity
        )
    )
    >>> creator.create()
    (Linear(in_features=4, out_features=6, bias=True), Identity())

    ```
    """

    def __init__(self, creators: Sequence[BaseCreator[T] | dict]) -> None:
        self._creators = tuple(setup_creator(creator) for creator in creators)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_sequence(self._creators))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_sequence(self._creators))}\n)"

    def create(self) -> tuple[T, ...]:
        return tuple(creator.create() for creator in self._creators)
