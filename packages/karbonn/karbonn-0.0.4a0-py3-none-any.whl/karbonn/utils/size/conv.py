r"""Contain a size finder for ``torch.nn.ConvNd`` and
``torch.nn.ConvTransposeNd`` layers or similar layers."""

from __future__ import annotations

__all__ = ["ConvolutionSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError


class ConvolutionSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for convolution layers like
    ``torch.nn.ConvNd`` and ``torch.nn.ConvTransposeNd``.

    This module size finder assumes the module has a single input and
    output, and the input size is given by the attribute
    ``in_channels`` and the output size is given by the attribute
    ``out_channels``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import ConvolutionSizeFinder
    >>> size_finder = ConvolutionSizeFinder()
    >>> module = torch.nn.Conv2d(in_channels=4, out_channels=6, kernel_size=1)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [4]
    >>> out_features = size_finder.find_out_features(module)
    >>> out_features
    [6]

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def find_in_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "in_channels"):
            msg = f"module {module} does not have attribute in_channels"
            raise SizeNotFoundError(msg)
        return [module.in_channels]

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "out_channels"):
            msg = f"module {module} does not have attribute out_channels"
            raise SizeNotFoundError(msg)
        return [module.out_channels]
