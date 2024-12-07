r"""Contain the loss functions that use the inverse hyperbolic sine
(asinh) to transform the predictions or targets."""

from __future__ import annotations

__all__ = ["AsinhMSELoss", "AsinhSmoothL1Loss"]

import torch
from torch import nn

from karbonn.functional import check_loss_reduction_strategy
from karbonn.functional.loss.asinh import asinh_mse_loss, asinh_smooth_l1_loss


class AsinhMSELoss(nn.Module):
    r"""Implement a loss module that computes the mean squared error
    (MSE) on the inverse hyperbolic sine (asinh) transformed predictions
    and targets.

    It is a generalization of mean squared logarithmic error (MSLE)
    that works for real values. The ``asinh`` transformation is used
    instead of ``log1p`` because ``asinh`` works on negative values.

    Args:
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import AsinhMSELoss
    >>> criterion = AsinhMSELoss()
    >>> criterion
    AsinhMSELoss(reduction=mean)
    >>> loss = criterion(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<MseLossBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, reduction: str = "mean") -> None:
        super().__init__()
        check_loss_reduction_strategy(reduction)
        self.reduction = str(reduction)

    def extra_repr(self) -> str:
        return f"reduction={self.reduction}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return asinh_mse_loss(prediction, target, reduction=self.reduction)


class AsinhSmoothL1Loss(nn.Module):
    r"""Implement a loss module that computes the smooth L1 loss on the
    inverse hyperbolic sine (asinh) transformed predictions and targets.

    It is a generalization of mean squared logarithmic error (MSLE)
    that works for real values. The ``asinh`` transformation is used
    instead of ``log1p`` because ``asinh`` works on negative values.

    Args:
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        beta: The threshold at which to change between L1 and L2 loss.
            The value must be non-negative.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import AsinhSmoothL1Loss
    >>> criterion = AsinhSmoothL1Loss()
    >>> criterion
    AsinhSmoothL1Loss(reduction=mean, beta=1.0)
    >>> loss = criterion(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<SmoothL1LossBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, reduction: str = "mean", beta: float = 1.0) -> None:
        super().__init__()
        check_loss_reduction_strategy(reduction)
        self.reduction = str(reduction)
        self._beta = float(beta)

    def extra_repr(self) -> str:
        return f"reduction={self.reduction}, beta={self._beta}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return asinh_smooth_l1_loss(prediction, target, reduction=self.reduction, beta=self._beta)
