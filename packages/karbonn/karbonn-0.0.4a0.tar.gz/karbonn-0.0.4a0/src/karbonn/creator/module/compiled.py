r"""Contain a module creator that returns a compiled module."""

from __future__ import annotations

__all__ = ["CompiledModuleCreator"]

from typing import TYPE_CHECKING

import torch
from coola.utils import str_indent, str_mapping

from karbonn.creator.module import setup_module_creator
from karbonn.creator.module.base import BaseModuleCreator

if TYPE_CHECKING:
    from torch.nn import Module


class CompiledModuleCreator(BaseModuleCreator):
    r"""Implement a module creator that returns a compiled module.

    Args:
        creator: The module creator or its configuration.
        config: Some keyword arguments used to compile the model.
            Please read the documentation of ``torch.compile`` to see
            the possible options.

    Example usage:

    ```pycon

    >>> from karbonn.creator.module import ModuleCreator
    >>> creator = CompiledModuleCreator(
    ...     creator=ModuleCreator(
    ...         {
    ...             "_target_": "torch.nn.Linear",
    ...             "in_features": 4,
    ...             "out_features": 6,
    ...         }
    ...     )
    ... )
    >>> creator
    CompiledModuleCreator(
      (creator): ModuleCreator(
        (_target_): torch.nn.Linear
        (in_features): 4
        (out_features): 6
      )
      (config): {}
    )
    >>> creator.create()
    OptimizedModule(
      (_orig_mod): Linear(in_features=4, out_features=6, bias=True)
    )

    ```
    """

    def __init__(self, creator: BaseModuleCreator | dict, config: dict | None = None) -> None:
        self._creator = setup_module_creator(creator)
        self._config = config or {}

    def __repr__(self) -> str:
        config = {"creator": self._creator, "config": self._config}
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(config))}\n)"

    def create(self) -> Module:
        return torch.compile(self._creator.create(), **self._config)
