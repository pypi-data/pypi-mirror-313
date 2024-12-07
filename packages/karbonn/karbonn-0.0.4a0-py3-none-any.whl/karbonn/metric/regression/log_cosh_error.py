r"""Contain a metric to compute the logarithm of the hyperbolic cosine
of the prediction error."""

from __future__ import annotations

__all__ = ["LogCoshError"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_mapping

from karbonn.functional import log_cosh_loss
from karbonn.metric.state import BaseState, ErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class LogCoshError(BaseStateMetric):
    r"""Implement a metric to compute the logarithm of the hyperbolic
    cosine of the prediction error.

    Args:
        scale: The scale factor.
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import LogCoshError
    >>> metric = LogCoshError()
    >>> metric
    LogCoshError(
      (scale): 1.0
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
    {'mean': 0.072296...,
     'min': 0.0,
     'max': 0.433780...,
     'sum': 0.867561...,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value("log_cosh_err_")
    {'log_cosh_err_mean': 0.216890...,
     'log_cosh_err_min': 0.0,
     'log_cosh_err_max': 0.433780...,
     'log_cosh_err_sum': 0.867561...,
     'log_cosh_err_count': 4}

    ```
    """

    def __init__(self, scale: float = 1.0, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())
        if scale <= 0.0:
            msg = f"Incorrect scale {scale}. The scale has to be >0"
            raise ValueError(msg)
        self._scale = float(scale)

    def extra_repr(self) -> str:
        return repr_mapping({"scale": self._scale, "state": self._state})

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the metric given a mini-batch of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import LogCoshError
        >>> metric = LogCoshError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(log_cosh_loss(prediction, target, reduction="none", scale=self._scale))
