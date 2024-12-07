r"""Contain a size finder for Transformer layers like
``torch.nn.TransformerEncoderLayer``,
``torch.nn.TransformerDecoderLayer``, ``torch.nn.TransformerEncoder``,
or ``torch.nn.TransformerDecoder``."""

from __future__ import annotations

__all__ = ["TransformerLayerSizeFinder", "TransformerSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError
from karbonn.utils.size.functional import find_in_features, find_out_features


class TransformerLayerSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for layers like
    ``torch.nn.TransformerEncoderLayer`` or
    ``torch.nn.TransformerDecoderLayer``.

    This module size finder assumes the module has an attribute
    ``self_attn`` which is used to find the input and output feature
    sizes.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import TransformerLayerSizeFinder
    >>> size_finder = TransformerLayerSizeFinder()
    >>> module = torch.nn.TransformerEncoderLayer(d_model=4, nhead=1)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
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
        if not hasattr(module, "self_attn"):
            msg = f"module {module} does not have attribute self_attn"
            raise SizeNotFoundError(msg)
        return [find_in_features(module.self_attn)[0]]

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "self_attn"):
            msg = f"module {module} does not have attribute self_attn"
            raise SizeNotFoundError(msg)
        return [find_out_features(module.self_attn)[0]]


class TransformerSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for layers like
    ``torch.nn.TransformerEncoder`` or ``torch.nn.TransformerDecoder``.

    This module size finder assumes the module has an attribute
    ``self_attn`` which is used to find the input and output feature
    sizes.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import TransformerSizeFinder
    >>> size_finder = TransformerSizeFinder()
    >>> module = torch.nn.TransformerEncoder(
    ...     torch.nn.TransformerEncoderLayer(d_model=4, nhead=1),
    ...     num_layers=1,
    ... )
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
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
        if not hasattr(module, "layers"):
            msg = f"module {module} does not have attribute layers"
            raise SizeNotFoundError(msg)
        return find_in_features(module.layers)

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "layers"):
            msg = f"module {module} does not have attribute layers"
            raise SizeNotFoundError(msg)
        return find_out_features(module.layers)
