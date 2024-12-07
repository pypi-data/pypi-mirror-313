r"""Contain the base class to implement a module creator."""

from __future__ import annotations

__all__ = ["BaseModuleCreator", "is_module_creator_config", "setup_module_creator"]

import logging
from abc import abstractmethod
from unittest.mock import Mock

from torch.nn import Module

from karbonn.creator.base import BaseCreator
from karbonn.utils.factory import setup_object_typed
from karbonn.utils.imports import check_objectory, is_objectory_available

if is_objectory_available():
    import objectory
else:  # pragma: no cover
    objectory = Mock()


logger = logging.getLogger(__name__)


class BaseModuleCreator(BaseCreator[Module]):
    r"""Define the base class to implement a module creator.

    Example usage:

    ```pycon

    >>> from karbonn.creator.module import ModuleCreator
    >>> creator = ModuleCreator(
    ...     {
    ...         "_target_": "torch.nn.Linear",
    ...         "in_features": 4,
    ...         "out_features": 6,
    ...     }
    ... )
    >>> creator
    ModuleCreator(
      (_target_): torch.nn.Linear
      (in_features): 4
      (out_features): 6
    )
    >>> creator.create()
    Linear(in_features=4, out_features=6, bias=True)

    ```
    """

    @abstractmethod
    def create(self) -> Module:
        r"""Create a module.

        Returns:
            The created module.

        Example usage:

        ```pycon

        >>> from karbonn.creator.module import ModuleCreator
        >>> creator = ModuleCreator(
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


def is_module_creator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseModuleCreator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseModuleCreator`` object,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.creator.module import is_module_creator_config
    >>> is_module_creator_config(
    ...     {
    ...         "_target_": "karbonn.creator.module.ModuleCreator",
    ...         "module": {
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
    return objectory.utils.is_object_config(config, BaseModuleCreator)


def setup_module_creator(creator: BaseModuleCreator | dict) -> BaseModuleCreator:
    r"""Set up a ``BaseModuleCreator`` object.

    Args:
        creator: The module creator or its configuration.

    Returns:
        The instantiated ``BaseModuleCreator`` object.

    Example usage:

    ```pycon

    >>> from karbonn.creator.module import setup_module_creator
    >>> creator = setup_module_creator(
    ...     {
    ...         "_target_": "karbonn.creator.module.ModuleCreator",
    ...         "module": {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         },
    ...     }
    ... )
    >>> creator
    ModuleCreator(
      (_target_): torch.nn.Linear
      (in_features): 4
      (out_features): 6
    )

    ```
    """
    return setup_object_typed(
        obj_or_config=creator, cls=BaseModuleCreator, name="BaseModuleCreator"
    )
