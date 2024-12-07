r"""Contain the normalized mean squared error metric."""

from __future__ import annotations

__all__ = ["NormalizedMeanSquaredError"]

import logging
from typing import TYPE_CHECKING

from karbonn.functional import absolute_error
from karbonn.metric.state import BaseState, NormalizedMeanSquaredErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class NormalizedMeanSquaredError(BaseStateMetric):
    r"""Implement the normalized mean squared error (NMSE) metric.

    Note: this metric does not work if all the targets are zero.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``NormalizedMeanSquaredErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import NormalizedMeanSquaredError
    >>> metric = NormalizedMeanSquaredError()
    >>> metric
    NormalizedMeanSquaredError(
      (state): NormalizedMeanSquaredErrorState(
          (squared_errors): MeanTensorTracker(count=0, total=0.0)
          (squared_targets): MeanTensorTracker(count=0, total=0.0)
          (track_count): True
        )
    )
    >>> metric(torch.ones(2, 4), torch.ones(2, 4))
    >>> metric.value()
    {'mean': 0.0, 'count': 8}
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value()
    {'mean': 0.166666..., 'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value()
    {'mean': 0.5, 'count': 4}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or NormalizedMeanSquaredErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the normalized mean squared error metric given a mini-
        batch of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import NormalizedMeanSquaredError
        >>> metric = NormalizedMeanSquaredError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0, 'count': 8}

        ```
        """
        self._state.update(absolute_error(prediction, target), target)
