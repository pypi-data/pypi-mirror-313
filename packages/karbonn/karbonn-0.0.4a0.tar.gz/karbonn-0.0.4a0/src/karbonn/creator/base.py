r"""Contain the base class to implement a generic object creator."""

from __future__ import annotations

__all__ = ["BaseCreator", "is_creator_config", "setup_creator"]

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Generic, TypeVar
from unittest.mock import Mock

from karbonn.utils.factory import setup_object_typed
from karbonn.utils.imports import check_objectory, is_objectory_available

if is_objectory_available():
    import objectory
    from objectory import AbstractFactory
else:  # pragma: no cover
    objectory = Mock()
    AbstractFactory = ABCMeta


logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseCreator(Generic[T], ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement an object creator.

    Example usage:

    ```pycon

    >>> from karbonn.creator import Creator
    >>> creator = Creator(
    ...     {
    ...         "_target_": "torch.nn.Linear",
    ...         "in_features": 4,
    ...         "out_features": 6,
    ...     }
    ... )
    >>> creator
    Creator(
      (_target_): torch.nn.Linear
      (in_features): 4
      (out_features): 6
    )
    >>> creator.create()
    Linear(in_features=4, out_features=6, bias=True)

    ```
    """

    @abstractmethod
    def create(self) -> T:
        r"""Create an object.

        Returns:
            The created object.

        Example usage:

        ```pycon

        >>> from karbonn.creator import Creator
        >>> creator = Creator(
        ...     {
        ...         "_target_": "torch.nn.Linear",
        ...         "in_features": 4,
        ...         "out_features": 6,
        ...     }
        ... )
        >>> creator.create()
        Linear(in_features=4, out_features=6, bias=True)

        ```
        """


def is_creator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseCreator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseCreator`` object, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.creator import is_creator_config
    >>> is_creator_config(
    ...     {
    ...         "_target_": "karbonn.creator.Creator",
    ...         "obj_or_config": {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         },
    ...     }
    ... )
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, BaseCreator)


def setup_creator(creator: BaseCreator | dict) -> BaseCreator:
    r"""Set up a ``BaseCreator`` object.

    Args:
        creator: The object creator or its configuration.

    Returns:
        The instantiated ``BaseCreator`` object.

    Example usage:

    ```pycon

    >>> from karbonn.creator import setup_creator
    >>> creator = setup_creator(
    ...     {
    ...         "_target_": "karbonn.creator.Creator",
    ...         "obj_or_config": {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         },
    ...     }
    ... )
    >>> creator
    Creator(
      (_target_): torch.nn.Linear
      (in_features): 4
      (out_features): 6
    )

    ```
    """
    return setup_object_typed(obj_or_config=creator, cls=BaseCreator, name="BaseCreator")
