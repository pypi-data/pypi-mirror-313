r"""Contain the implementation of a size finder that automatically finds
the size based on the module type."""

from __future__ import annotations

__all__ = ["AutoSizeFinder", "register_size_finders"]

from typing import TYPE_CHECKING, ClassVar

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from karbonn.utils.size.base import BaseSizeFinder

if TYPE_CHECKING:
    from torch import nn


class AutoSizeFinder(BaseSizeFinder):
    """Implement a size finder that automatically finds the size based
    on the module type.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import AutoSizeFinder
    >>> size_finder = AutoSizeFinder()
    >>> module = torch.nn.Linear(4, 6)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [6]

    ```
    """

    registry: ClassVar[dict[type, BaseSizeFinder]] = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(self.registry))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self.registry))}\n)"

    @classmethod
    def add_size_finder(
        cls, module_type: type[nn.Module], size_finder: BaseSizeFinder, exist_ok: bool = False
    ) -> None:
        r"""Add a size finder for a given module type.

        Args:
            module_type: The module type.
            size_finder: The size finder to use for the given module
                type.
            exist_ok: If ``False``, ``RuntimeError`` is raised if the
                data type already exists. This parameter should be set
                to ``True`` to overwrite the size finder for a module
                type.

        Raises:
            RuntimeError: if a size finder is already registered for
                the module type and ``exist_ok=False``.

        Example usage:

        ```pycon

        >>> from torch import nn
        >>> from karbonn.utils.size import AutoSizeFinder, LinearSizeFinder
        >>> AutoSizeFinder.add_size_finder(nn.Linear, LinearSizeFinder(), exist_ok=True)

        ```
        """
        if module_type in cls.registry and not exist_ok:
            msg = (
                f"A size finder {cls.registry[module_type]} is already registered for the "
                f"module type {module_type}. Please use `exist_ok=True` if you want to overwrite "
                "the size finder for this type"
            )
            raise RuntimeError(msg)
        cls.registry[module_type] = size_finder

    def find_in_features(self, module: nn.Module) -> list[int]:
        return self.find_size_finder(type(module)).find_in_features(module)

    def find_out_features(self, module: nn.Module) -> list[int]:
        return self.find_size_finder(type(module)).find_out_features(module)

    @classmethod
    def has_size_finder(cls, module_type: type) -> bool:
        r"""Indicate if a size finder is registered for the given module
        type.

        Args:
            module_type: The module type.

        Returns:
            ``True`` if a size finder is registered,
                otherwise ``False``.

        Example usage:

        ```pycon

        >>> from torch import nn
        >>> from karbonn.utils.size import AutoSizeFinder
        >>> AutoSizeFinder.has_size_finder(nn.Linear)
        True
        >>> AutoSizeFinder.has_size_finder(str)
        False

        ```
        """
        return module_type in cls.registry

    @classmethod
    def find_size_finder(cls, module_type: type[nn.Module]) -> BaseSizeFinder:
        r"""Find the size finder associated to a module type.

        Args:
            module_type: The module type.

        Returns:
            The size finder associated to the module type.

        Example usage:

        ```pycon

        >>> from torch import nn
        >>> from karbonn.utils.size import AutoSizeFinder
        >>> AutoSizeFinder.find_size_finder(nn.Linear)
        LinearSizeFinder()
        >>> AutoSizeFinder.find_size_finder(nn.Bilinear)
        BilinearSizeFinder()

        ```
        """
        for object_type in module_type.__mro__:
            comparator = cls.registry.get(object_type, None)
            if comparator is not None:
                return comparator
        msg = f"Incorrect module type: {module_type}"
        raise TypeError(msg)


def register_size_finders() -> None:
    r"""Register size finders to ``AutoSizeFinder``.

    Example usage:

    ```pycon

    >>> from karbonn.utils.size import AutoSizeFinder, register_size_finders
    >>> register_size_finders()
    >>> size_finder = AutoSizeFinder()
    >>> size_finder
    AutoSizeFinder(
      ...
    )

    ```
    """
    # Local import to avoid cyclic dependency
    from karbonn.utils.size.utils import get_size_finders

    for module_type, finder in get_size_finders().items():
        if not AutoSizeFinder.has_size_finder(module_type):  # pragma: no cover
            AutoSizeFinder.add_size_finder(module_type, finder)
