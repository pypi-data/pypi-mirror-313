r"""Contain iterators on ``torch.nn.Module``."""

from __future__ import annotations

__all__ = ["get_named_modules"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

    from torch import nn


def get_named_modules(module: nn.Module, depth: int = 0) -> Generator[tuple[str, nn.Module]]:
    r"""Return an iterator over the modules, yielding both the name of
    the module as well as the module itself.

    Args:
        module: The input module.
        depth: The maximum depth of module to yield.

    Returns:
        The iterator over the modules and their names.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.iterator import get_named_modules
    >>> module = torch.nn.Linear(4, 6)
    >>> named_modules = list(get_named_modules(module))
    >>> named_modules
    [('[root]', Linear(in_features=4, out_features=6, bias=True))]
    >>> module = torch.nn.Sequential(
    ...     torch.nn.Linear(4, 6), torch.nn.ReLU(), torch.nn.Linear(6, 3)
    ... )
    >>> named_modules = list(get_named_modules(module))
    >>> named_modules
    [('[root]', Sequential(
      (0): Linear(in_features=4, out_features=6, bias=True)
      (1): ReLU()
      (2): Linear(in_features=6, out_features=3, bias=True)
    ))]
    >>> named_modules = list(get_named_modules(module, depth=1))
    >>> named_modules
    [('[root]', Sequential(
      (0): Linear(in_features=4, out_features=6, bias=True)
      (1): ReLU()
      (2): Linear(in_features=6, out_features=3, bias=True)
    )),
    ('0', Linear(in_features=4, out_features=6, bias=True)),
    ('1', ReLU()), ('2', Linear(in_features=6, out_features=3, bias=True))]

    ```
    """
    yield ("[root]", module)
    if depth == 1:
        yield from module.named_children()
    elif depth > 1:
        for name, layer in list(module.named_modules())[1:]:
            if name.count(".") <= depth - 1:
                yield (name, layer)
