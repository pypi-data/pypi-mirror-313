r"""Contain utility functions to analyze and manage ``torch.nn.Module``
parameters."""

from __future__ import annotations

__all__ = [
    "freeze_module",
    "has_learnable_parameters",
    "has_parameters",
    "num_learnable_parameters",
    "num_parameters",
    "unfreeze_module",
]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import nn


def has_parameters(module: nn.Module) -> bool:
    r"""Indicate if the module has parameters.

    Args:
        module: The module to test.

    Returns:
        ``True`` if the module has at least one parameter,
            ``False`` otherwise.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import has_parameters
    >>> has_parameters(torch.nn.Linear(4, 6))
    True
    >>> has_parameters(torch.nn.Identity())
    False

    ```
    """
    try:
        next(module.parameters())
    except StopIteration:
        return False
    else:
        return True


def has_learnable_parameters(module: nn.Module) -> bool:
    r"""Indicate if the module has learnable parameters.

    Args:
        module: The module to test.

    Returns:
        ``True`` if the module has at least one learnable parameter,
            ``False`` otherwise.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import has_learnable_parameters, freeze_module
    >>> has_learnable_parameters(torch.nn.Linear(4, 6))
    True
    >>> module = torch.nn.Linear(4, 6)
    >>> freeze_module(module)
    >>> has_learnable_parameters(module)
    False
    >>> has_learnable_parameters(torch.nn.Identity())
    False

    ```
    """
    return num_learnable_parameters(module) > 0


def num_parameters(module: nn.Module) -> int:
    r"""Return the number of parameters in the module.

    Args:
        module: The module to compute the number of parameters.

    Returns:
        The number of parameters.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import num_parameters
    >>> num_parameters(torch.nn.Linear(4, 6))
    30
    >>> num_parameters(torch.nn.Identity())
    0

    ```
    """
    return sum(params.numel() for params in module.parameters())


def num_learnable_parameters(module: nn.Module) -> int:
    r"""Return the number of learnable parameters in the module.

    Args:
        module: The module to compute the number of learnable
            parameters.

    Returns:
        int: The number of learnable parameters.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import num_learnable_parameters
    >>> num_learnable_parameters(torch.nn.Linear(4, 6))
    30
    >>> module = torch.nn.Linear(4, 6)
    >>> freeze_module(module)
    >>> num_learnable_parameters(module)
    0
    >>> num_learnable_parameters(torch.nn.Identity())
    0

    ```
    """
    return sum(params.numel() for params in module.parameters() if params.requires_grad)


def freeze_module(module: nn.Module) -> None:
    r"""Freeze the parameters of the given module.

    Args:
        module: The module to freeze.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import freeze_module
    >>> module = torch.nn.Linear(4, 6)
    >>> freeze_module(module)
    >>> for name, param in module.named_parameters():
    ...     print(name, param.requires_grad)
    ...
    weight False
    bias False

    ```
    """
    for param in module.parameters():
        param.requires_grad = False


def unfreeze_module(module: nn.Module) -> None:
    r"""Unfreeze the parameters of the given module.

    Args:
        module: The module to unfreeze.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import unfreeze_module
    >>> module = torch.nn.Linear(4, 6)
    >>> unfreeze_module(module)
    >>> for name, param in module.named_parameters():
    ...     print(name, param.requires_grad)
    ...
    weight True
    bias True

    ```
    """
    for param in module.parameters():
        param.requires_grad = True
