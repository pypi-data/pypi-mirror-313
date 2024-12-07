r"""Contain the base class to implement an optimizer creator."""

from __future__ import annotations

__all__ = ["BaseOptimizerCreator", "is_optimizer_creator_config", "setup_optimizer_creator"]

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import TYPE_CHECKING
from unittest.mock import Mock

from karbonn.utils.factory import setup_object_typed
from karbonn.utils.imports import check_objectory, is_objectory_available

if is_objectory_available():
    import objectory
    from objectory import AbstractFactory
else:  # pragma: no cover
    objectory = Mock()
    AbstractFactory = ABCMeta

if TYPE_CHECKING:
    from torch.nn import Module, Optimizer

logger = logging.getLogger(__name__)


class BaseOptimizerCreator(ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement an optimizer creator.

    Example usage:

    ```pycon

    >>> from torch import nn
    >>> from karbonn.creator.optimizer import OptimizerCreator
    >>> linear = nn.Linear(4, 6)
    >>> creator = OptimizerCreator({"_target_": "torch.optim.SGD", "lr": 0.001})
    >>> creator
    OptimizerCreator(
      (_target_): torch.optim.SGD
      (lr): 0.001
    )
    >>> creator.create(linear)
    SGD (
    Parameter Group 0
        dampening: 0
        differentiable: False
        foreach: None
        fused: None
        lr: 0.001
        maximize: False
        momentum: 0
        nesterov: False
        weight_decay: 0
    )

    ```
    """

    @abstractmethod
    def create(self, module: Module) -> Optimizer:
        r"""Create an optimizer.

        Args:
            module: The module.

        Returns:
            The created optimizer.

        Example usage:

        ```pycon

        >>> from torch import nn
        >>> from karbonn.creator.optimizer import OptimizerCreator
        >>> linear = nn.Linear(4, 6)
        >>> creator = OptimizerCreator({"_target_": "torch.optim.SGD", "lr": 0.001})
        >>> creator.create(linear)
        SGD (
        Parameter Group 0
            dampening: 0
            differentiable: False
            foreach: None
            fused: None
            lr: 0.001
            maximize: False
            momentum: 0
            nesterov: False
            weight_decay: 0
        )

        ```
        """


def is_optimizer_creator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseOptimizerCreator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseOptimizerCreator`` object,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.creator.optimizer import is_optimizer_creator_config
    >>> is_optimizer_creator_config(
    ...     {
    ...         "_target_": "karbonn.creator.optimizer.OptimizerCreator",
    ...         "optimizer": {"_target_": "torch.optim.SGD", "lr": 0.001},
    ...     }
    ... )
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, BaseOptimizerCreator)


def setup_optimizer_creator(creator: BaseOptimizerCreator | dict) -> BaseOptimizerCreator:
    r"""Set up a ``BaseOptimizerCreator`` object.

    Args:
        creator: The optimizer creator or its configuration.

    Returns:
        The instantiated ``BaseOptimizerCreator`` object.

    Example usage:

    ```pycon

    >>> from karbonn.creator.optimizer import setup_optimizer_creator
    >>> creator = setup_optimizer_creator(
    ...     {
    ...         "_target_": "karbonn.creator.optimizer.OptimizerCreator",
    ...         "optimizer": {"_target_": "torch.optim.SGD", "lr": 0.001},
    ...     }
    ... )
    >>> creator
    OptimizerCreator(
      (_target_): torch.optim.SGD
      (lr): 0.001
    )

    ```
    """
    return setup_object_typed(
        obj_or_config=creator, cls=BaseOptimizerCreator, name="BaseOptimizerCreator"
    )
