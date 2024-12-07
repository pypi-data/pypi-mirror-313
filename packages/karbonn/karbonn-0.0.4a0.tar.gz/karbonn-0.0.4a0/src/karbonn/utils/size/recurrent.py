r"""Contain a size finder for recurrent layers like ``torch.nn.RNN``,
``torch.nn.GRU``, and ``torch.nn.LSTM``."""

from __future__ import annotations

__all__ = ["RecurrentSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError


class RecurrentSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for recurrent layers like
    ``torch.nn.RNN``, ``torch.nn.GRU``, and ``torch.nn.LSTM``.

    This module size finder assumes the module has a single input and
    output, and the input size is given by the attribute
    ``input_size`` and the output size is given by the attribute
    ``hidden_size``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import RecurrentSizeFinder
    >>> size_finder = RecurrentSizeFinder()
    >>> module = torch.nn.RNN(input_size=4, hidden_size=6)
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
        if not hasattr(module, "input_size"):
            msg = f"module {module} does not have attribute input_size"
            raise SizeNotFoundError(msg)
        return [module.input_size]

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "hidden_size"):
            msg = f"module {module} does not have attribute hidden_size"
            raise SizeNotFoundError(msg)
        return [module.hidden_size]
