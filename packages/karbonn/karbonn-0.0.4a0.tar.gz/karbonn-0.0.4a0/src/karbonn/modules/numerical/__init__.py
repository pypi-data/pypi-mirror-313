r"""Contain module to encode or decode numerical values."""

from __future__ import annotations

__all__ = [
    "AsinhCosSinNumericalEncoder",
    "AsinhNumericalEncoder",
    "CosSinNumericalEncoder",
    "PiecewiseLinearNumericalEncoder",
]

from karbonn.modules.numerical.asinh import AsinhNumericalEncoder
from karbonn.modules.numerical.piecewise import PiecewiseLinearNumericalEncoder
from karbonn.modules.numerical.sine import (
    AsinhCosSinNumericalEncoder,
    CosSinNumericalEncoder,
)
