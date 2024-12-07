r"""Contain some absolute relative error metrics."""

from __future__ import annotations

__all__ = ["AbsoluteRelativeError", "SymmetricAbsoluteRelativeError"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_mapping

from karbonn.functional import (
    absolute_relative_error,
    symmetric_absolute_relative_error,
)
from karbonn.metric.state import BaseState, ErrorState
from karbonn.metric.state_ import BaseStateMetric

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class AbsoluteRelativeError(BaseStateMetric):
    r"""Implement the absolute relative error metric.

    Args:
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the target is zero.
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import AbsoluteRelativeError
    >>> metric = AbsoluteRelativeError()
    >>> metric
    AbsoluteRelativeError(
      (eps): 1e-08
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
    >>> metric.value(prefix="abs_rel_err_")
    {'abs_rel_err_mean': 0.5,
     'abs_rel_err_min': 0.0,
     'abs_rel_err_max': 1.0,
     'abs_rel_err_sum': 2.0,
     'abs_rel_err_count': 4}

    ```
    """

    def __init__(self, eps: float = 1e-8, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())
        if eps <= 0:
            msg = (
                f"Incorrect eps ({eps}). eps has to be an arbitrary small strictly "
                f"positive number to avoid undefined results when the target is zero."
            )
            raise ValueError(msg)
        self._eps = eps

    def extra_repr(self) -> str:
        return repr_mapping({"eps": self._eps, "state": self._state})

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the mean absolute percentage error metric given a
        mini-batch of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import AbsoluteRelativeError
        >>> metric = AbsoluteRelativeError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(absolute_relative_error(prediction, target, eps=self._eps))


class SymmetricAbsoluteRelativeError(BaseStateMetric):
    r"""Implement the symmetric absolute relative error (SARE) metric.

    This metric tracks the mean, maximum and minimum absolute
    relative error values.

    Args:
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the target is zero.
        state: The metric state or its configuration. If ``None``,
            ``ErrorState`` is instantiated.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import SymmetricAbsoluteRelativeError
    >>> metric = SymmetricAbsoluteRelativeError()
    >>> metric
    SymmetricAbsoluteRelativeError(
      (eps): 1e-08
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
    {'mean': 0.3333333333333333,
     'min': 0.0,
     'max': 2.0,
     'sum': 4.0,
     'count': 12}
    >>> metric.reset()
    >>> metric(torch.eye(2), torch.ones(2, 2))
    >>> metric.value("sym_abs_rel_err_")
    {'sym_abs_rel_err_mean': 1.0,
     'sym_abs_rel_err_min': 0.0,
     'sym_abs_rel_err_max': 2.0,
     'sym_abs_rel_err_sum': 4.0,
     'sym_abs_rel_err_count': 4}

    ```
    """

    def __init__(self, eps: float = 1e-8, state: BaseState | dict | None = None) -> None:
        super().__init__(state=state or ErrorState())
        if eps <= 0:
            msg = (
                f"Incorrect eps ({eps}). eps has to be an arbitrary small strictly "
                f"positive number to avoid undefined results when the target is zero."
            )
            raise ValueError(msg)
        self._eps = eps

    def extra_repr(self) -> str:
        return repr_mapping({"eps": self._eps, "state": self._state})

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the mean absolute percentage error metric given a
        mini-batch of examples.

        Args:
            prediction: The predictions as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.
            target: The target tensor as a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn)`` and type float or long.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import SymmetricAbsoluteRelativeError
        >>> metric = SymmetricAbsoluteRelativeError()
        >>> metric(torch.ones(2, 4), torch.ones(2, 4))
        >>> metric.value()
        {'mean': 0.0,
         'min': 0.0,
         'max': 0.0,
         'sum': 0.0,
         'count': 8}

        ```
        """
        self._state.update(symmetric_absolute_relative_error(prediction, target, eps=self._eps))
