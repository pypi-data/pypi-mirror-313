r"""Contain tracker implementations for metrics."""

from __future__ import annotations

__all__ = [
    "Average",
    "AverageTracker",
    "BaseConfusionMatrixTracker",
    "BaseTracker",
    "BinaryConfusionMatrix",
    "BinaryConfusionMatrixTracker",
    "EmptyTrackerError",
    "ExponentialMovingAverage",
    "ExtremaTensorTracker",
    "MeanTensorTracker",
    "MovingAverage",
    "MulticlassConfusionMatrix",
    "MulticlassConfusionMatrixTracker",
    "ScalableTensorTracker",
    "ScalarTracker",
    "TensorTracker",
]

from karbonn.utils.tracker.average import AverageTracker
from karbonn.utils.tracker.average import AverageTracker as Average
from karbonn.utils.tracker.base import BaseTracker
from karbonn.utils.tracker.confmat import BaseConfusionMatrixTracker
from karbonn.utils.tracker.confmat import BinaryConfusionMatrixTracker
from karbonn.utils.tracker.confmat import (
    BinaryConfusionMatrixTracker as BinaryConfusionMatrix,
)
from karbonn.utils.tracker.confmat import MulticlassConfusionMatrixTracker
from karbonn.utils.tracker.confmat import (
    MulticlassConfusionMatrixTracker as MulticlassConfusionMatrix,
)
from karbonn.utils.tracker.exception import EmptyTrackerError
from karbonn.utils.tracker.moving import ExponentialMovingAverage, MovingAverage
from karbonn.utils.tracker.scalar import ScalarTracker
from karbonn.utils.tracker.tensor import (
    ExtremaTensorTracker,
    MeanTensorTracker,
    ScalableTensorTracker,
    TensorTracker,
)
