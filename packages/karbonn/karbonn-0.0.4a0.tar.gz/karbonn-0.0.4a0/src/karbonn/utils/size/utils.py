r"""Contain the default mappings between the module types and their size
finders."""

from __future__ import annotations

__all__ = [
    "get_karbonn_size_finders",
    "get_size_finders",
    "get_torch_size_finders",
]

from typing import TYPE_CHECKING

from torch import nn

if TYPE_CHECKING:
    from karbonn.utils.size import BaseSizeFinder


def get_size_finders() -> dict[type[nn.Module], BaseSizeFinder]:
    r"""Return the default mappings between the module types and their
    size finders.

    Returns:
        The default mappings between the module types and their size
            finders.

    Example usage:

    ```pycon

    >>> from karbonn.utils.size import get_size_finders
    >>> get_size_finders()
    {<class 'torch.nn.modules.module.Module'>: UnknownSizeFinder(), ...}

    ```
    """
    return get_torch_size_finders() | get_karbonn_size_finders()


def get_karbonn_size_finders() -> dict[type[nn.Module], BaseSizeFinder]:
    r"""Return the default mappings between the module types and their
    size finders.

    Returns:
        The default mappings between the module types and their size
            finders.

    Example usage:

    ```pycon

    >>> from karbonn.utils.size import get_karbonn_size_finders
    >>> get_karbonn_size_finders()
    {...}

    ```
    """
    # Local import to avoid cyclic dependencies
    from karbonn.modules import ExU
    from karbonn.utils import size as size_finders

    return {ExU: size_finders.LinearSizeFinder()}


def get_torch_size_finders() -> dict[type[nn.Module], BaseSizeFinder]:
    r"""Return the default mappings between the module types and their
    size finders.

    Returns:
        The default mappings between the module types and their size
            finders.

    Example usage:

    ```pycon

    >>> from karbonn.utils.size import get_torch_size_finders
    >>> get_torch_size_finders()
    {<class 'torch.nn.modules.module.Module'>: UnknownSizeFinder(), ...}

    ```
    """
    # Local import to avoid cyclic dependencies
    from karbonn.utils import size

    return {
        nn.Module: size.UnknownSizeFinder(),
        nn.BatchNorm1d: size.BatchNormSizeFinder(),
        nn.BatchNorm2d: size.BatchNormSizeFinder(),
        nn.BatchNorm3d: size.BatchNormSizeFinder(),
        nn.Bilinear: size.BilinearSizeFinder(),
        nn.Conv1d: size.ConvolutionSizeFinder(),
        nn.Conv2d: size.ConvolutionSizeFinder(),
        nn.Conv3d: size.ConvolutionSizeFinder(),
        nn.ConvTranspose1d: size.ConvolutionSizeFinder(),
        nn.ConvTranspose2d: size.ConvolutionSizeFinder(),
        nn.ConvTranspose3d: size.ConvolutionSizeFinder(),
        nn.Embedding: size.EmbeddingSizeFinder(),
        nn.EmbeddingBag: size.EmbeddingSizeFinder(),
        nn.GRU: size.RecurrentSizeFinder(),
        nn.GroupNorm: size.GroupNormSizeFinder(),
        nn.LSTM: size.RecurrentSizeFinder(),
        nn.Linear: size.LinearSizeFinder(),
        nn.ModuleList: size.ModuleListSizeFinder(),
        nn.MultiheadAttention: size.MultiheadAttentionSizeFinder(),
        nn.RNN: size.RecurrentSizeFinder(),
        nn.Sequential: size.SequentialSizeFinder(),
        nn.SyncBatchNorm: size.BatchNormSizeFinder(),
        nn.TransformerDecoder: size.TransformerSizeFinder(),
        nn.TransformerDecoderLayer: size.TransformerLayerSizeFinder(),
        nn.TransformerEncoder: size.TransformerSizeFinder(),
        nn.TransformerEncoderLayer: size.TransformerLayerSizeFinder(),
    }
