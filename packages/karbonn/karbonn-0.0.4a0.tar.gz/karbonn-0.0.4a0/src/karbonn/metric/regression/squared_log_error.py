r"""Contain the squared logarithmic error-based metrics."""

from __future__ import annotations

__all__ = ["SquaredAsinhError", "SquaredLogError"]

import logging
from typing import TYPE_CHECKING

from karbonn.functional import asinh_mse_loss, msle_loss
from karbonn.metric.state import ErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

    from karbonn.metric.state import BaseState

logger = logging.getLogger(__name__)


class SquaredAsinhError(BaseStateMetric):
    r"""Implement a metric to compute the squared error on the inverse
    hyperbolic sine (arcsinh) transformed predictions and targets.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import SquaredAsinhError
    >>> metric = SquaredAsinhError()
    >>> metric
    SquaredAsinhError(
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
    {'mean': 0.129469...,
     'min': 0.0,
     'max': 0.776819...,
     'sum': 1.553638...,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value("sq_asinh_err_")
    {'sq_asinh_err_mean': 0.388409...,
     'sq_asinh_err_min': 0.0,
     'sq_asinh_err_max': 0.776819...,
     'sq_asinh_err_sum': 1.553638...,
     'sq_asinh_err_count': 4}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the squared error on the inverse hyperbolic sine
        (arcsinh) transformed predictions and targets given a mini-batch
        of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import SquaredAsinhError
        >>> metric = SquaredAsinhError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(asinh_mse_loss(prediction, target, reduction="none"))


class SquaredLogError(BaseStateMetric):
    r"""Implement the squared logarithmic error (SLE) metric.

    This metric is best to use when targets having exponential growth,
    such as population counts, average sales of a commodity over a
    span of years etc. Note that this metric penalizes an
    under-predicted estimate greater than an over-predicted estimate.

    Note: this metric only works with positive value (0 included).

    Args:
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import SquaredLogError
    >>> metric = SquaredLogError()
    >>> metric
    SquaredLogError(
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
    {'mean': 0.080075...,
     'min': 0.0,
     'max': 0.480453...,
     'sum': 0.960906...,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value("sq_log_err_")
    {'sq_log_err_mean': 0.240226...,
     'sq_log_err_min': 0.0,
     'sq_log_err_max': 0.480453...,
     'sq_log_err_sum': 0.960906...,
     'sq_log_err_count': 4}

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
        >>> from karbonn.metric import SquaredLogError
        >>> metric = SquaredLogError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(msle_loss(prediction, target, reduction="none"))
