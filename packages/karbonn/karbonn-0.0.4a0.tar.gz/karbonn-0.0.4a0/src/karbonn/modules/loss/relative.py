r"""Contain relative loss implementations."""

from __future__ import annotations

__all__ = ["RelativeLoss", "RelativeMSELoss", "RelativeSmoothL1Loss"]

from typing import TYPE_CHECKING

import torch
from torch import nn

from karbonn.functional import check_loss_reduction_strategy, relative_loss
from karbonn.modules.loss.indicators import ClassicalRelativeIndicator
from karbonn.utils import setup_module

if TYPE_CHECKING:
    from karbonn.modules.loss import BaseRelativeIndicator


class RelativeLoss(nn.Module):
    r"""Implement a "generic" relative loss that takes as input a
    criterion.

    Args:
        criterion: The criterion or its configuration. This criterion
            should not have reduction to be compatible with the shapes
            of the prediction and targets.
        indicator: The name of the indicator function to use or its
            implementation. If ``None``, ``ClassicalRelativeIndicator``
            is instantiated.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the indicator is zero.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import RelativeLoss
    >>> from karbonn.modules.loss import ClassicalRelativeIndicator
    >>> criterion = RelativeLoss(
    ...     criterion=torch.nn.MSELoss(reduction="none"),
    ...     indicator=ClassicalRelativeIndicator(),
    ... )
    >>> criterion
    RelativeLoss(
      eps=1e-08, reduction=mean
      (criterion): MSELoss()
      (indicator): ClassicalRelativeIndicator()
    )
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> loss = criterion(prediction, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(
        self,
        criterion: nn.Module | dict,
        indicator: BaseRelativeIndicator | dict | None = None,
        reduction: str = "mean",
        eps: float = 1e-8,
    ) -> None:
        super().__init__()
        self.criterion = setup_module(criterion)
        self.indicator = setup_module(indicator or ClassicalRelativeIndicator())

        check_loss_reduction_strategy(reduction)
        self.reduction = reduction
        self._eps = eps

    def extra_repr(self) -> str:
        return f"eps={self._eps}, reduction={self.reduction}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        loss = self.criterion(prediction, target)
        indicator = self.indicator(prediction, target)
        return relative_loss(
            loss=loss,
            indicator=indicator,
            reduction=self.reduction,
            eps=self._eps,
        )


class RelativeMSELoss(RelativeLoss):
    r"""Implement the relative MSE loss.

    Args:
        indicator: The name of the indicator function to use or its
            implementation. If ``None``, ``ClassicalRelativeIndicator``
            is instantiated.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the indicator is zero.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import RelativeMSELoss
    >>> from karbonn.modules.loss import ClassicalRelativeIndicator
    >>> criterion = RelativeMSELoss(indicator=ClassicalRelativeIndicator())
    >>> criterion
    RelativeMSELoss(
      eps=1e-08, reduction=mean
      (criterion): MSELoss()
      (indicator): ClassicalRelativeIndicator()
    )
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> loss = criterion(prediction, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(
        self,
        indicator: BaseRelativeIndicator | dict | None = None,
        reduction: str = "mean",
        eps: float = 1e-8,
    ) -> None:
        super().__init__(
            criterion=nn.MSELoss(reduction="none"),
            indicator=indicator,
            reduction=reduction,
            eps=eps,
        )


class RelativeSmoothL1Loss(RelativeLoss):
    r"""Implement the relative smooth L1 loss.

    Args:
        indicator: The name of the indicator function to use or its
            implementation. If ``None``, ``ClassicalRelativeIndicator``
            is instantiated.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the indicator is zero.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import RelativeSmoothL1Loss
    >>> from karbonn.modules.loss import ClassicalRelativeIndicator
    >>> criterion = RelativeSmoothL1Loss(indicator=ClassicalRelativeIndicator())
    >>> criterion
    RelativeSmoothL1Loss(
      eps=1e-08, reduction=mean
      (criterion): SmoothL1Loss()
      (indicator): ClassicalRelativeIndicator()
    )
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> loss = criterion(prediction, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(
        self,
        indicator: BaseRelativeIndicator | dict | None = None,
        reduction: str = "mean",
        eps: float = 1e-8,
    ) -> None:
        super().__init__(
            criterion=nn.SmoothL1Loss(reduction="none"),
            indicator=indicator,
            reduction=reduction,
            eps=eps,
        )
