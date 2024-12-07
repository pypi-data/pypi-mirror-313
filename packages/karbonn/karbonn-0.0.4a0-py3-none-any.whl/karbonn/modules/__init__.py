r"""Contain some modules."""

from __future__ import annotations

__all__ = [
    "Asinh",
    "AsinhCosSinNumericalEncoder",
    "AsinhMSELoss",
    "AsinhNumericalEncoder",
    "AsinhSmoothL1Loss",
    "AverageFusion",
    "BinaryFocalLoss",
    "BinaryFocalLossWithLogits",
    "BinaryPoly1Loss",
    "BinaryPoly1LossWithLogits",
    "Clamp",
    "ConcatFusion",
    "CosSinNumericalEncoder",
    "ExU",
    "Exp",
    "ExpSin",
    "Expm1",
    "Gaussian",
    "GeneralRobustRegressionLoss",
    "Laplacian",
    "Log",
    "Log1p",
    "MultiQuadratic",
    "MulticlassFlatten",
    "MultiplicationFusion",
    "NLinear",
    "PiecewiseLinearNumericalEncoder",
    "PoissonRegressionLoss",
    "Quadratic",
    "QuantileRegressionLoss",
    "ReLUn",
    "RelativeLoss",
    "RelativeMSELoss",
    "RelativeSmoothL1Loss",
    "ResidualBlock",
    "SafeExp",
    "SafeLog",
    "Sin",
    "Sinh",
    "Snake",
    "SquaredReLU",
    "Squeeze",
    "SumFusion",
    "ToBinaryLabel",
    "ToCategoricalLabel",
    "ToFloat",
    "ToLong",
    "TransformedLoss",
    "View",
]

from karbonn.modules.activations import (
    Asinh,
    Exp,
    Expm1,
    ExpSin,
    Gaussian,
    Laplacian,
    Log,
    Log1p,
    MultiQuadratic,
    Quadratic,
    ReLUn,
    SafeExp,
    SafeLog,
    Sin,
    Sinh,
    Snake,
    SquaredReLU,
)
from karbonn.modules.clamp import Clamp
from karbonn.modules.classification import ToBinaryLabel, ToCategoricalLabel
from karbonn.modules.dtype import ToFloat, ToLong
from karbonn.modules.exu import ExU
from karbonn.modules.fusion import (
    AverageFusion,
    ConcatFusion,
    MultiplicationFusion,
    SumFusion,
)
from karbonn.modules.loss import (
    AsinhMSELoss,
    AsinhSmoothL1Loss,
    BinaryFocalLoss,
    BinaryFocalLossWithLogits,
    BinaryPoly1Loss,
    BinaryPoly1LossWithLogits,
    GeneralRobustRegressionLoss,
    PoissonRegressionLoss,
    QuantileRegressionLoss,
    RelativeLoss,
    RelativeMSELoss,
    RelativeSmoothL1Loss,
    TransformedLoss,
)
from karbonn.modules.nlinear import NLinear
from karbonn.modules.numerical import (
    AsinhCosSinNumericalEncoder,
    AsinhNumericalEncoder,
    CosSinNumericalEncoder,
    PiecewiseLinearNumericalEncoder,
)
from karbonn.modules.residual import ResidualBlock
from karbonn.modules.shape import MulticlassFlatten, Squeeze, View
