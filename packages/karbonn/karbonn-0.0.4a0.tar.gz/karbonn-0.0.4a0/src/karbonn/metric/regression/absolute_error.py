r"""Contain the absolute error metric."""

from __future__ import annotations

__all__ = ["AbsoluteError"]

import logging
from typing import TYPE_CHECKING

from karbonn.functional import absolute_error
from karbonn.metric.state import BaseState, ErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class AbsoluteError(BaseStateMetric):
    r"""Implement the absolute error metric.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import AbsoluteError
    >>> metric = AbsoluteError()
    >>> metric
    AbsoluteError(
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
    {'mean': 0.16666666666666666,
     'min': 0.0,
     'max': 1.0,
     'sum': 2.0,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value(prefix="abs_err_")
    {'abs_err_mean': 0.5,
     'abs_err_min': 0.0,
     'abs_err_max': 1.0,
     'abs_err_sum': 2.0,
     'abs_err_count': 4}

    ```
    """

    def __init__(self, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the mean absolute error metric given a mini-batch of
        examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import AbsoluteError
        >>> metric = AbsoluteError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(absolute_error(prediction, target))
