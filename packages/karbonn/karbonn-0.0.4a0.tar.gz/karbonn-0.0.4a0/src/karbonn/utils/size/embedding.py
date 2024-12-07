r"""Contain a size finder for ``torch.nn.Embedding`` layer or similar
layers."""

from __future__ import annotations

__all__ = ["EmbeddingSizeFinder"]


from torch import nn

from karbonn.utils.size.base import BaseSizeFinder, SizeNotFoundError


class EmbeddingSizeFinder(BaseSizeFinder[nn.Module]):
    r"""Implement a size finder for embedding layers like
    ``torch.nn.Embedding``.

    This module size finder assumes the module has a single input and
    output, and the input size is always 1, and the output size is
    given by the attribute ``embedding_dim``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.size import EmbeddingSizeFinder
    >>> size_finder = EmbeddingSizeFinder()
    >>> module = torch.nn.Embedding(num_embeddings=5, embedding_dim=6)
    >>> in_features = size_finder.find_in_features(module)
    >>> in_features
    [1]
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

    def find_in_features(self, module: nn.Module) -> list[int]:  # noqa: ARG002
        return [1]

    def find_out_features(self, module: nn.Module) -> list[int]:
        if not hasattr(module, "embedding_dim"):
            msg = f"module {module} does not have attribute embedding_dim"
            raise SizeNotFoundError(msg)
        return [module.embedding_dim]
