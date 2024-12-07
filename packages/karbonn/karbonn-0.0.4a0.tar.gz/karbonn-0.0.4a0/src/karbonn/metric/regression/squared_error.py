r"""Contain the squared error-based metrics."""

from __future__ import annotations

__all__ = ["RootMeanSquaredError", "SquaredError"]

import logging
from typing import TYPE_CHECKING

from torch.nn.functional import mse_loss

from karbonn.metric.state import BaseState, ErrorState, RootMeanErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class SquaredError(BaseStateMetric):
    r"""Implement the squared error metric.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import SquaredError
    >>> metric = SquaredError()
    >>> metric
    SquaredError(
      (state): ErrorState(
          (tracker): ScalableTensorTracker(count=0, total=0.0, min_value=inf, max_value=-inf)
          (track_count): True
        )
    )
    >>> metric(torch.ones(2, 4), torch.ones(2, 4))
    >>> metric.value()
    {'mean': 0.0,
     'min': 0.0,
     'max': 0.0,
     'sum': 0.0,
     'count': 8}
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value()
    {'mean': 0.166666...,
     'min': 0.0,
     'max': 1.0,
     'sum': 2.0,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value("sq_err_")
    {'sq_err_mean': 0.5,
     'sq_err_min': 0.0,
     'sq_err_max': 1.0,
     'sq_err_sum': 2.0,
     'sq_err_count': 4}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the squared logarithmic error metric given a mini-
        batch of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import SquaredError
        >>> metric = SquaredError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(mse_loss(prediction.float(), target.float(), reduction="none"))


class RootMeanSquaredError(SquaredError):
    r"""Implement the squared error metric.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``RootMeanErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import RootMeanSquaredError
    >>> metric = RootMeanSquaredError()
    >>> metric
    RootMeanSquaredError(
      (state): RootMeanErrorState(
          (tracker): MeanTensorTracker(count=0, total=0.0)
          (track_count): True
        )
    )
    >>> metric(torch.ones(2, 4), torch.ones(2, 4))
    >>> metric.value()
    {'mean': 0.0, 'count': 8}
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value()
    {'mean': 0.408248..., 'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value()
    {'mean': 0.707106..., 'count': 4}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(
            state=state or RootMeanErrorState(),
        )
