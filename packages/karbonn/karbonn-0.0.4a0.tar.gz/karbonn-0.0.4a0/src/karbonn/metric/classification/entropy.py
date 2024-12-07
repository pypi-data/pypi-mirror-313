r"""Contain a metric to compute the categorical cross-entropy."""

from __future__ import annotations

__all__ = ["CategoricalCrossEntropy"]

import logging
from typing import TYPE_CHECKING

from torch.nn.functional import cross_entropy

from karbonn.metric.state import BaseState, MeanErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class CategoricalCrossEntropy(BaseStateMetric):
    r"""Implement a metric to compute the categorical cross-entropy.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``MeanErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import CategoricalCrossEntropy
    >>> metric = CategoricalCrossEntropy()
    >>> metric
    CategoricalCrossEntropy(
      (state): MeanErrorState(
          (tracker): MeanTensorTracker(count=0, total=0.0)
          (track_count): True
        )
    )
    >>> metric(torch.eye(4), torch.arange(4))
    >>> metric.value()
    {'mean': 0.743668..., 'count': 4}
    >>> metric(torch.ones(2, 3), torch.ones(2))
    >>> metric.value()
    {'mean': 0.861983..., 'count': 6}
    >>> metric.reset()
    >>> metric(torch.ones(2, 3), torch.ones(2))
    >>> metric.value()
    {'mean': 1.098612..., 'count': 2}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or MeanErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the metric given a mini-batch of examples.

        Args:
            prediction: The predicted labels as a ``torch.Tensor`` of
                shape ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, num_classes)``
                and type float.
            target: The categorical targets. The values have to be in
                ``{0, 1, ..., num_classes-1}``. This input must be a
                ``torch.Tensor`` of shape ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, 1)`` and type long or float.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import CategoricalCrossEntropy
        >>> metric = CategoricalCrossEntropy()
        >>> metric(torch.eye(4), torch.arange(4))
        >>> metric.value()
        {'mean': 0.743668..., 'count': 4}

        ```
        """
        self._state.update(
            cross_entropy(
                prediction.flatten(start_dim=0, end_dim=-2),
                target.flatten().long(),
                reduction="none",
            )
        )
