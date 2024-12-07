r"""Contain a simple module creator implementation."""

from __future__ import annotations

__all__ = ["ModuleCreator"]

from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from karbonn.creator.module.base import BaseModuleCreator
from karbonn.utils import setup_module

if TYPE_CHECKING:
    from torch.nn import Module


class ModuleCreator(BaseModuleCreator):
    r"""Implement a simple module creator.

    Args:
        module: The module or its configuration.

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

    def __init__(self, module: Module | dict) -> None:
        self._module = module

    def __repr__(self) -> str:
        config = (
            repr_mapping(self._module, sorted_keys=True)
            if isinstance(self._module, dict)
            else self._module
        )
        return f"{self.__class__.__qualname__}(\n  {repr_indent(config)}\n)"

    def __str__(self) -> str:
        config = (
            str_mapping(self._module, sorted_keys=True)
            if isinstance(self._module, dict)
            else self._module
        )
        return f"{self.__class__.__qualname__}(\n  {str_indent(config)}\n)"

    def create(self) -> Module:
        return setup_module(self._module)
