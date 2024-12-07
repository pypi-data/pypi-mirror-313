r"""Contain code to find the input and output size of some
``torch.nn.Module``s."""

from __future__ import annotations

__all__ = [
    "AutoSizeFinder",
    "BaseSizeFinder",
    "BatchNormSizeFinder",
    "BilinearSizeFinder",
    "ConvolutionSizeFinder",
    "EmbeddingSizeFinder",
    "GroupNormSizeFinder",
    "LinearSizeFinder",
    "ModuleListSizeFinder",
    "MultiheadAttentionSizeFinder",
    "RecurrentSizeFinder",
    "SequentialSizeFinder",
    "TransformerLayerSizeFinder",
    "TransformerSizeFinder",
    "UnknownSizeFinder",
    "find_in_features",
    "find_out_features",
    "get_karbonn_size_finders",
    "get_size_finders",
    "get_torch_size_finders",
    "register_size_finders",
]

from karbonn.utils.size.attention import MultiheadAttentionSizeFinder
from karbonn.utils.size.auto import AutoSizeFinder, register_size_finders
from karbonn.utils.size.base import BaseSizeFinder
from karbonn.utils.size.conv import ConvolutionSizeFinder
from karbonn.utils.size.embedding import EmbeddingSizeFinder
from karbonn.utils.size.functional import find_in_features, find_out_features
from karbonn.utils.size.linear import BilinearSizeFinder, LinearSizeFinder
from karbonn.utils.size.list import ModuleListSizeFinder
from karbonn.utils.size.norm import BatchNormSizeFinder, GroupNormSizeFinder
from karbonn.utils.size.recurrent import RecurrentSizeFinder
from karbonn.utils.size.sequential import SequentialSizeFinder
from karbonn.utils.size.transformer import (
    TransformerLayerSizeFinder,
    TransformerSizeFinder,
)
from karbonn.utils.size.unknown import UnknownSizeFinder
from karbonn.utils.size.utils import (
    get_karbonn_size_finders,
    get_size_finders,
    get_torch_size_finders,
)

register_size_finders()
