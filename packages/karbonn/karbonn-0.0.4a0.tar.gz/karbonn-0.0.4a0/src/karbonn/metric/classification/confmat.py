r"""Contain confusion tracker metrics for binary and categorical
labels."""

from __future__ import annotations

__all__ = ["BinaryConfusionMatrix", "CategoricalConfusionMatrix"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_mapping

from karbonn.metric.base import BaseMetric, EmptyMetricError
from karbonn.utils.tracker import (
    BinaryConfusionMatrixTracker,
    MulticlassConfusionMatrixTracker,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from minrecord import BaseRecord
    from torch import Tensor


logger = logging.getLogger(__name__)


class BinaryConfusionMatrix(BaseMetric):
    r"""Implement a confusion tracker metric for binary labels.

    Args:
        betas: The betas used to compute the f-beta scores.
        tracker: The value tracker. If ``None``,
            a ``BinaryConfusionMatrixTracker`` object is initialized.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import BinaryConfusionMatrix
    >>> metric = BinaryConfusionMatrix()
    >>> metric
    BinaryConfusionMatrix(
      (betas): (1,)
      (tracker): BinaryConfusionMatrixTracker(num_classes=2, count=0)
      (track_count): True
    )
    >>> metric(torch.tensor([0, 1, 0, 1]), torch.tensor([0, 1, 0, 1]))
    >>> metric.value()
    {'accuracy': 1.0,
     'balanced_accuracy': 1.0,
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'jaccard_index': 1.0,
     'count': 4,
     'precision': 1.0,
     'recall': 1.0,
     'true_negative_rate': 1.0,
     'true_negative': 2,
     'true_positive_rate': 1.0,
     'true_positive': 2,
     'f1_score': 1.0}
    >>> metric(torch.tensor([1, 0]), torch.tensor([1, 0]))
    >>> metric.value()
    {'accuracy': 1.0,
     'balanced_accuracy': 1.0,
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'jaccard_index': 1.0,
     'count': 6,
     'precision': 1.0,
     'recall': 1.0,
     'true_negative_rate': 1.0,
     'true_negative': 3,
     'true_positive_rate': 1.0,
     'true_positive': 3,
     'f1_score': 1.0}
    >>> metric.reset()
    >>> metric(torch.tensor([1, 0]), torch.tensor([1, 0]))
    >>> metric.value()
    {'accuracy': 1.0,
     'balanced_accuracy': 1.0,
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'jaccard_index': 1.0,
     'count': 2,
     'precision': 1.0,
     'recall': 1.0,
     'true_negative_rate': 1.0,
     'true_negative': 1,
     'true_positive_rate': 1.0,
     'true_positive': 1,
     'f1_score': 1.0}

    ```
    """

    def __init__(
        self,
        betas: Sequence[int | float] = (1,),
        tracker: BinaryConfusionMatrixTracker | None = None,
        track_count: bool = True,
    ) -> None:
        super().__init__()
        self._betas = tuple(betas)
        self._tracker = tracker or BinaryConfusionMatrixTracker()
        self._track_count = bool(track_count)

    def extra_repr(self) -> str:
        return repr_mapping(
            {
                "betas": self._betas,
                "tracker": str(self._tracker),
                "track_count": self._track_count,
            }
        )

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the confusion tracker metric given a mini-batch of
        examples.

        Args:
            prediction: The predicted labels where the values are ``0`` or
                ``1``. This input must be a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` or ``(d0, d1, ..., dn, 1)``
                and type long or float.
            target: The binary targets where the values are ``0`` or
                ``1``. This input must be a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` or  ``(d0, d1, ..., dn, 1)``
                and type bool or long or float.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import BinaryConfusionMatrix
        >>> metric = BinaryConfusionMatrix()
        >>> metric(torch.tensor([0, 1, 0, 1]), torch.tensor([0, 1, 0, 1]))
        >>> metric.value()
        {'accuracy': 1.0,
         'balanced_accuracy': 1.0,
         'false_negative_rate': 0.0,
         'false_negative': 0,
         'false_positive_rate': 0.0,
         'false_positive': 0,
         'jaccard_index': 1.0,
         'count': 4,
         'precision': 1.0,
         'recall': 1.0,
         'true_negative_rate': 1.0,
         'true_negative': 2,
         'true_positive_rate': 1.0,
         'true_positive': 2,
         'f1_score': 1.0}

        ```
        """
        self._tracker.update(prediction.flatten(), target.flatten())

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return self._tracker.get_records(betas=self._betas, prefix=prefix, suffix=suffix)

    def reset(self) -> None:
        self._tracker.reset()

    def value(self, prefix: str = "", suffix: str = "") -> dict:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = tracker.compute_metrics(betas=self._betas, prefix=prefix, suffix=suffix)
        if not self._track_count:
            del results[f"{prefix}count{suffix}"]
        return results


class CategoricalConfusionMatrix(BaseMetric):
    r"""Implement a confusion tracker metric for multi-class labels.

    Args:
        num_classes: The number of classes.
        betas: The betas used to compute the f-beta scores.
        tracker: The value tracker. If ``None``,
            a ``BinaryConfusionMatrixTracker`` object is initialized.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import CategoricalConfusionMatrix
    >>> metric = CategoricalConfusionMatrix(num_classes=3)
    >>> metric
    CategoricalConfusionMatrix(
      (betas): (1,)
      (tracker): MulticlassConfusionMatrixTracker(num_classes=3, count=0)
      (track_count): True
    )
    >>> metric(
    ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
    ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
    ... )
    >>> metric.value()
    {'accuracy': 0.5,
     'balanced_accuracy': 0.333333...,
     'count': 6,
     'macro_precision': 0.555555...,
     'macro_recall': 0.333333...,
     'macro_f1_score': 0.388888...,
     'micro_precision': 0.5,
     'micro_recall': 0.5,
     'micro_f1_score': 0.5,
     'weighted_precision': 0.833333...,
     'weighted_recall': 0.5,
     'weighted_f1_score': 0.583333...,
     'precision': tensor([0.6667, 0.0000, 1.0000]),
     'recall': tensor([0.6667, 0.0000, 0.3333]),
     'f1_score': tensor([0.6667, 0.0000, 0.5000])}
    >>> metric(prediction=torch.tensor([1, 0]), target=torch.tensor([1, 0]))
    >>> metric.value()
    {'accuracy': 0.625,
     'balanced_accuracy': 0.694444...,
     'count': 8,
     'macro_precision': 0.694444...,
     'macro_recall': 0.694444...,
     'macro_f1_score': 0.583333...,
     'micro_precision': 0.625,
     'micro_recall': 0.625,
     'micro_f1_score': 0.625,
     'weighted_precision': 0.791666...,
     'weighted_recall': 0.625,
     'weighted_f1_score': 0.625,
     'precision': tensor([0.7500, 0.3333, 1.0000]),
     'recall': tensor([0.7500, 1.0000, 0.3333]),
     'f1_score': tensor([0.7500, 0.5000, 0.5000])}
    >>> metric.reset()
    >>> metric(prediction=torch.tensor([1, 0, 2]), target=torch.tensor([1, 0, 2]))
    >>> metric.value()
    {'accuracy': 1.0,
     'balanced_accuracy': 1.0,
     'count': 3,
     'macro_precision': 1.0,
     'macro_recall': 1.0,
     'macro_f1_score': 1.0,
     'micro_precision': 1.0,
     'micro_recall': 1.0,
     'micro_f1_score': 1.0,
     'weighted_precision': 1.0,
     'weighted_recall': 1.0,
     'weighted_f1_score': 1.0,
     'precision': tensor([1., 1., 1.]),
     'recall': tensor([1., 1., 1.]),
     'f1_score': tensor([1., 1., 1.])}

    ```
    """

    def __init__(
        self,
        num_classes: int,
        betas: Sequence[int | float] = (1,),
        tracker: MulticlassConfusionMatrixTracker | None = None,
        track_count: bool = True,
    ) -> None:
        super().__init__()
        self._betas = tuple(betas)
        self._tracker = tracker or MulticlassConfusionMatrixTracker.from_num_classes(num_classes)
        self._tracker.resize(num_classes)
        self._track_count = bool(track_count)

    def extra_repr(self) -> str:
        return repr_mapping(
            {
                "betas": self._betas,
                "tracker": str(self._tracker),
                "track_count": self._track_count,
            }
        )

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the confusion tracker metric given a mini-batch of
        examples.

        Args:
            prediction: The predicted labels where the values are ``0`` or
                ``1``. This input must be a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` or ``(d0, d1, ..., dn, 1)``
                and type long or float.
            target: The binary targets where the values are ``0`` or
                ``1``. This input must be a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` or  ``(d0, d1, ..., dn, 1)``
                and type bool or long or float.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import CategoricalConfusionMatrix
        >>> metric = CategoricalConfusionMatrix(num_classes=3)
        >>> metric(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> metric.value()
        {'accuracy': 0.5,
         'balanced_accuracy': 0.333333...,
         'count': 6,
         'macro_precision': 0.555555...,
         'macro_recall': 0.333333...,
         'macro_f1_score': 0.388888...,
         'micro_precision': 0.5,
         'micro_recall': 0.5,
         'micro_f1_score': 0.5,
         'weighted_precision': 0.833333...,
         'weighted_recall': 0.5,
         'weighted_f1_score': 0.583333...,
         'precision': tensor([0.6667, 0.0000, 1.0000]),
         'recall': tensor([0.6667, 0.0000, 0.3333]),
         'f1_score': tensor([0.6667, 0.0000, 0.5000])}

        ```
        """
        self._tracker.update(prediction.flatten(), target.flatten())

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return self._tracker.get_records(betas=self._betas, prefix=prefix, suffix=suffix)

    def reset(self) -> None:
        self._tracker.reset()

    def value(self, prefix: str = "", suffix: str = "") -> dict:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = tracker.compute_metrics(betas=self._betas, prefix=prefix, suffix=suffix)
        if not self._track_count:
            del results[f"{prefix}count{suffix}"]
        return results
