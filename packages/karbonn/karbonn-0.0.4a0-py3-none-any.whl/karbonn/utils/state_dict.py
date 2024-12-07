r"""Contain utility functions to manipulate ``torch.nn.Module``'s state
dict."""

from __future__ import annotations

__all__ = ["find_module_state_dict", "load_state_dict_to_module"]

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import nn

logger = logging.getLogger(__name__)


def find_module_state_dict(state_dict: dict | list | tuple | set, module_keys: set) -> dict:
    r"""Try to find automatically the part of the state dict related to a
    module.

    The user should specify the set of module's keys:
    ``set(module.state_dict().keys())``. This function assumes that
    the set of keys only exists at one location in the state dict.
    If the set of keys exists at several locations in the state dict,
    only the first one is returned.

    Args:
        state_dict: The state dict. This function is called recursively
            on this input to find the queried state dict.
        module_keys: The set of module keys.

    Returns:
        The part of the state dict related to a module if it is
            found, otherwise an empty dict.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import find_module_state_dict
    >>> state = {
    ...     "model": {
    ...         "weight": 42,
    ...         "network": {
    ...             "weight": torch.ones(5, 4),
    ...             "bias": 2 * torch.ones(5),
    ...         },
    ...     }
    ... }
    >>> module = torch.nn.Linear(4, 5)
    >>> state_dict = find_module_state_dict(state, module_keys=set(module.state_dict().keys()))
    >>> state_dict
    {'weight': tensor([[1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]]), 'bias': tensor([2., 2., 2., 2., 2.])}

    ```
    """
    if isinstance(state_dict, dict):
        if set(state_dict.keys()) == module_keys:
            return state_dict
        for value in state_dict.values():
            state_dict = find_module_state_dict(value, module_keys)
            if state_dict:
                return state_dict
    elif isinstance(state_dict, (list, tuple, set)):
        for value in state_dict:
            state_dict = find_module_state_dict(value, module_keys)
            if state_dict:
                return state_dict
    return {}


def load_state_dict_to_module(state_dict: dict, module: nn.Module, strict: bool = True) -> None:
    r"""Load a state dict into a given module.

    This function will automatically try to find the module state dict
    in the given state dict.

    Args:
        state_dict: The state dict.
        module: The module. This function changes the weights of this
            module.
        strict: whether to strictly enforce that the
            keys in ``state_dict`` match the keys returned by this
            module's ``torch.nn.Module.state_dict`` function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import load_state_dict_to_module
    >>> state = {
    ...     "model": {
    ...         "weight": 42,
    ...         "network": {
    ...             "weight": torch.ones(5, 4),
    ...             "bias": 2 * torch.ones(5),
    ...         },
    ...     }
    ... }
    >>> module = torch.nn.Linear(4, 5)
    >>> load_state_dict_to_module(state, module)
    >>> out = module(torch.ones(2, 4))
    >>> out
    tensor([[6., 6., 6., 6., 6.],
            [6., 6., 6., 6., 6.]], grad_fn=<AddmmBackward0>)

    ```
    """
    try:
        module.load_state_dict(state_dict, strict)
    except RuntimeError:
        logger.warning(
            "Could not load the state dict. Try to find automatically the part of the state dict "
            "that matches with the module."
        )
        state_dict = find_module_state_dict(state_dict, set(module.state_dict().keys()))
        if not state_dict:
            logger.info("Could not find a part of the state dict that matches with the module.")
            raise
        logger.info(
            "Found a part of the state dict that matches with the module. Try to load it in the "
            "module."
        )
        module.load_state_dict(state_dict, strict)
    logger.info("The weights are loaded in the module.")
