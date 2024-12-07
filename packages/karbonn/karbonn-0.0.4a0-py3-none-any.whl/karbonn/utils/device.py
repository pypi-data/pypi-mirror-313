r"""Contain utility functions to manage the device(s) of a
``torch.nn.Module``."""

from __future__ import annotations

__all__ = ["get_module_device", "get_module_devices", "is_module_on_device"]

import torch
from torch import nn

from karbonn.utils.params import has_parameters


def get_module_device(module: nn.Module) -> torch.device:
    r"""Get the device used by this module.

    This function assumes the module uses a single device. If the
    module uses several devices, you should use
    ``get_module_devices``. It returns ``torch.device('cpu')`` if
    the model does not have parameters.

    Args:
        module: The module.

    Returns:
        The device

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import get_module_device
    >>> get_module_device(torch.nn.Linear(4, 6))
    device(type='cpu')

    ```
    """
    if not has_parameters(module):
        return torch.device("cpu")
    return next(module.parameters()).device


def get_module_devices(module: nn.Module) -> tuple[torch.device, ...]:
    r"""Get the devices used in a module.

    Args:
        module: The module.

    Returns:
        The tuple of ``torch.device``s used in the module.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import get_module_devices
    >>> get_module_devices(torch.nn.Linear(4, 6))
    (device(type='cpu'),)

    ```
    """
    return tuple({param.device for param in module.parameters()})


def is_module_on_device(module: nn.Module, device: torch.device) -> bool:
    r"""Indicate if all the parameters of a module are on the specified
    device.

    Args:
        module: The module.
        device: The device.

    Returns:
        ``True`` if all the parameters of the module are on the
            specified device, otherwise ``False``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import is_module_on_device
    >>> is_module_on_device(torch.nn.Linear(4, 6), torch.device("cpu"))
    True

    ```
    """
    return all(p.device == device for p in module.parameters())
