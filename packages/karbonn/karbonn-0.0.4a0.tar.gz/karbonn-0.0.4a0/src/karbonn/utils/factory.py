r"""Contain functions to instantiate a ``torch.nn.Module`` object from
its configuration."""

from __future__ import annotations

__all__ = [
    "create_sequential",
    "is_dataset_config",
    "is_module_config",
    "is_optimizer_config",
    "setup_dataset",
    "setup_module",
    "setup_object",
    "setup_object_typed",
    "setup_optimizer",
    "str_target_object",
]

import logging
from typing import TYPE_CHECKING, TypeVar
from unittest.mock import Mock

from torch.nn import Module, Sequential
from torch.optim import Optimizer
from torch.utils.data import Dataset

from karbonn.utils.imports import check_objectory, is_objectory_available

if TYPE_CHECKING:
    from collections.abc import Sequence

if is_objectory_available():
    import objectory
else:  # pragma: no cover
    objectory = Mock()

T = TypeVar("T")


logger = logging.getLogger(__name__)


def is_dataset_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``torch.nn.Module``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``torch.nn.Module`` object, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import is_dataset_config
    >>> is_dataset_config(
    ...     {
    ...         "_target_": "karbonn.testing.dummy.DummyDataset",
    ...         "num_examples": 10,
    ...         "feature_size": 4,
    ...     }
    ... )
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, Dataset)


def is_module_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``torch.nn.Module``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``torch.nn.Module`` object, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import is_module_config
    >>> is_module_config({"_target_": "torch.nn.Identity"})
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, Module)


def is_optimizer_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``torch.optim.Optimizer``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``torch.optim.Optimizer`` object, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from torch import nn
    >>> from karbonn.utils.factory import is_optimizer_config
    >>> linear = nn.Linear(4, 6)
    >>> is_optimizer_config({"_target_": "torch.optim.SGD", "params": linear.parameters()})
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, Optimizer)


def setup_dataset(dataset: Dataset | dict) -> Dataset:
    r"""Set up a ``torch.utils.data.Dataset`` object.

    Args:
        dataset: The dataset or its configuration.

    Returns:
        The instantiated ``torch.utils.data.Dataset`` object.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import setup_dataset
    >>> dataset = setup_dataset(
    ...     {
    ...         "_target_": "karbonn.testing.dummy.DummyDataset",
    ...         "num_examples": 10,
    ...         "feature_size": 4,
    ...     }
    ... )
    >>> dataset
    DummyDataset(num_examples=10, feature_size=4, rng_seed=14700295087918620795)

    ```
    """
    return setup_object_typed(obj_or_config=dataset, cls=Dataset, name="torch.utils.data.Dataset")


def setup_module(module: Module | dict) -> Module:
    r"""Set up a ``torch.nn.Module`` object.

    Args:
        module: The module or its configuration.

    Returns:
        The instantiated ``torch.nn.Module`` object.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import setup_module
    >>> linear = setup_module(
    ...     {"_target_": "torch.nn.Linear", "in_features": 4, "out_features": 6}
    ... )
    >>> linear
    Linear(in_features=4, out_features=6, bias=True)

    ```
    """
    return setup_object_typed(obj_or_config=module, cls=Module, name="torch.nn.Module")


def setup_optimizer(optimizer: Optimizer | dict) -> Optimizer:
    r"""Set up a ``torch.optim.Optimizer`` object.

    Args:
        optimizer: The optimizer or its configuration.

    Returns:
        The instantiated ``torch.optim.Optimizer`` object.

    Example usage:

    ```pycon

    >>> from torch import nn
    >>> from karbonn.utils.factory import setup_optimizer
    >>> linear = nn.Linear(4, 6)
    >>> sgd = setup_optimizer({"_target_": "torch.optim.SGD", "params": linear.parameters()})
    >>> sgd
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
    return setup_object_typed(obj_or_config=optimizer, cls=Optimizer, name="torch.optim.Optimizer")


def create_sequential(modules: Sequence[Module | dict]) -> Sequential:
    r"""Create a ``torch.nn.Sequential`` from a sequence of modules.

    Args:
        modules: The sequence of modules or their configuration.

    Returns:
        The instantiated ``torch.nn.Sequential`` object.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import create_sequential
    >>> seq = create_sequential(
    ...     [
    ...         {"_target_": "torch.nn.Linear", "in_features": 4, "out_features": 6},
    ...         {"_target_": "torch.nn.ReLU"},
    ...         {"_target_": "torch.nn.Linear", "in_features": 6, "out_features": 6},
    ...     ]
    ... )
    >>> seq
    Sequential(
      (0): Linear(in_features=4, out_features=6, bias=True)
      (1): ReLU()
      (2): Linear(in_features=6, out_features=6, bias=True)
    )

    ```
    """
    return Sequential(*[setup_module(module) for module in modules])


def setup_object(obj_or_config: T | dict) -> T:
    r"""Set up an object from its configuration.

    Args:
        obj_or_config: The object or its configuration.

    Returns:
        The instantiated object.

    Raises:
        RuntimeError: if the ``objectory`` package is not installed.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import setup_object
    >>> linear = setup_object(
    ...     {"_target_": "torch.nn.Linear", "in_features": 4, "out_features": 6}
    ... )
    >>> linear
    Linear(in_features=4, out_features=6, bias=True)
    >>> setup_object(linear)  # Do nothing because the module is already instantiated
    Linear(in_features=4, out_features=6, bias=True)

    ```
    """
    if isinstance(obj_or_config, dict):
        check_objectory()
        logger.info(
            f"Initializing {str_target_object(obj_or_config)} object from its configuration... "
        )
        return objectory.factory(**obj_or_config)
    return obj_or_config


def setup_object_typed(obj_or_config: T | dict, cls: type, name: str | None = None) -> T:
    r"""Set up an object from its configuration.

    Args:
        obj_or_config: The object or its configuration.
        cls: The targeted class to check the instantiated object type.
        name: An optional custom name for the targeted class.

    Returns:
        The instantiated object.

    Raises:
        RuntimeError: if the ``objectory`` package is not installed.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.factory import setup_object_typed
    >>> linear = setup_object_typed(
    ...     {"_target_": "torch.nn.Linear", "in_features": 4, "out_features": 6},
    ...     cls=torch.nn.Module,
    ... )
    >>> linear
    Linear(in_features=4, out_features=6, bias=True)
    >>> setup_object_typed(
    ...     linear, cls=torch.nn.Module
    ... )  # Do nothing because the module is already instantiated
    Linear(in_features=4, out_features=6, bias=True)

    ```
    """
    if name is None:
        name = cls.__qualname__
    if isinstance(obj_or_config, dict):
        check_objectory()
        logger.info(f"Initializing a '{name}' from its configuration... ")
        obj = objectory.factory(**obj_or_config)
    else:
        obj = obj_or_config
    if not isinstance(obj, cls):
        logger.warning(f"object is not a '{name}' (received: {type(obj)})")
    return obj


def str_target_object(config: dict) -> str:
    r"""Get a string that indicates the target object in the config.

    Args:
        config: A config using the ``objectory`` library.
            This dict is expected to have a key ``'_target_'`` to
            indicate the target object.

    Returns:
        str: A string with the target object.

    Example usage:

    ```pycon

    >>> from karbonn.utils.factory import str_target_object
    >>> str_target_object({"_target_": "something.MyClass"})
    something.MyClass
    >>> str_target_object({})
    N/A

    ```
    """
    return config.get(objectory.OBJECT_TARGET, "N/A")
