r"""Contain loss functions."""

from __future__ import annotations

__all__ = [
    "ArithmeticalMeanIndicator",
    "AsinhMSELoss",
    "AsinhSmoothL1Loss",
    "BaseRelativeIndicator",
    "BinaryFocalLoss",
    "BinaryFocalLossWithLogits",
    "BinaryPoly1Loss",
    "BinaryPoly1LossWithLogits",
    "ClassicalRelativeIndicator",
    "GeneralRobustRegressionLoss",
    "GeometricMeanIndicator",
    "MaximumMeanIndicator",
    "MinimumMeanIndicator",
    "MomentMeanIndicator",
    "PoissonRegressionLoss",
    "QuantileRegressionLoss",
    "RelativeLoss",
    "RelativeMSELoss",
    "RelativeSmoothL1Loss",
    "ReversedRelativeIndicator",
    "TransformedLoss",
]

from karbonn.modules.loss.asinh import AsinhMSELoss, AsinhSmoothL1Loss
from karbonn.modules.loss.focal import BinaryFocalLoss, BinaryFocalLossWithLogits
from karbonn.modules.loss.general_robust import GeneralRobustRegressionLoss
from karbonn.modules.loss.indicators import (
    ArithmeticalMeanIndicator,
    BaseRelativeIndicator,
    ClassicalRelativeIndicator,
    GeometricMeanIndicator,
    MaximumMeanIndicator,
    MinimumMeanIndicator,
    MomentMeanIndicator,
    ReversedRelativeIndicator,
)
from karbonn.modules.loss.poisson import PoissonRegressionLoss
from karbonn.modules.loss.poly import BinaryPoly1Loss, BinaryPoly1LossWithLogits
from karbonn.modules.loss.quantile import QuantileRegressionLoss
from karbonn.modules.loss.relative import (
    RelativeLoss,
    RelativeMSELoss,
    RelativeSmoothL1Loss,
)
from karbonn.modules.loss.transform import TransformedLoss
