r"""Contain utility functions to manage the mode of a
``torch.nn.Module``."""

from __future__ import annotations

__all__ = ["module_mode", "top_module_mode"]

from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

    from torch import nn


@contextmanager
def module_mode(module: nn.Module) -> Generator[None]:
    r"""Implement a context manager that restores the mode (train or
    eval) of every submodule individually.

    Args:
        module: The module to restore the mode.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import module_mode
    >>> module = torch.nn.ModuleDict(
    ...     {"module1": torch.nn.Linear(4, 6), "module2": torch.nn.Linear(2, 4).eval()}
    ... )
    >>> print(module["module1"].training, module["module2"].training)
    True False
    >>> with module_mode(module):
    ...     module.eval()
    ...     print(module["module1"].training, module["module2"].training)
    ...
    ModuleDict(
      (module1): Linear(in_features=4, out_features=6, bias=True)
      (module2): Linear(in_features=2, out_features=4, bias=True)
    )
    False False
    >>> print(module["module1"].training, module["module2"].training)
    True False

    ```
    """
    modes = {}
    for name, submodule in module.named_modules():
        modes[name] = submodule.training
    try:
        yield
    finally:
        for name, submodule in module.named_modules():
            submodule.train(modes[name])


@contextmanager
def top_module_mode(module: nn.Module) -> Generator[None]:
    r"""Implement a context manager that restores the mode (train or
    eval) of a given module.

    This context manager only restores the mode at the top-level.

    Args:
        module: The module to restore the mode.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils import top_module_mode
    >>> module = torch.nn.Linear(4, 6)
    >>> print(module.training)
    True
    >>> with top_module_mode(module):
    ...     module.eval()
    ...     print(module.training)
    ...
    Linear(in_features=4, out_features=6, bias=True)
    False
    >>> print(module.training)
    True

    ```
    """
    mode = module.training
    try:
        yield
    finally:
        module.train(mode)
