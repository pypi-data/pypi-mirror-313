r"""Contain a size finder for ``torch.nn.MultiheadAttention`` layer or
similar layers."""

from __future__ import annotations

__all__ = ["MultiheadAttentionSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError


class MultiheadAttentionSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for ``torch.nn.MultiheadAttention`` layer
    or similar layers.

    This module size finder assumes the module has a single input and
    output, and the input size is given by the attribute
    ``embed_dim`` and the output size is given by the attribute
    ``embed_dim``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import MultiheadAttentionSizeFinder
    >>> size_finder = MultiheadAttentionSizeFinder()
    >>> module = torch.nn.MultiheadAttention(embed_dim=4, num_heads=2)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4, 4, 4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [4]

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def find_in_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "embed_dim"):
            msg = f"module {module} does not have attribute embed_dim"
            raise SizeNotFoundError(msg)
        return [module.embed_dim, module.kdim, module.vdim]

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "embed_dim"):
            msg = f"module {module} does not have attribute embed_dim"
            raise SizeNotFoundError(msg)
        return [module.embed_dim]
