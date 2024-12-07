r"""Contain the implementation of the quantile regression loss
function."""

from __future__ import annotations

__all__ = ["QuantileRegressionLoss"]

import torch
from torch import nn

from karbonn.functional.loss import quantile_regression_loss
from karbonn.functional.reduction import check_loss_reduction_strategy


class QuantileRegressionLoss(nn.Module):
    r"""Implement a loss module that computes the quantile regression
    loss.

    Loss Functions and Metrics in Deep Learning
    https://arxiv.org/pdf/2307.02694

    Args:
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        q: The quantile value. ``q=0.5`` is equivalent to the Mean
            Absolute Error (MAE).

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import QuantileRegressionLoss
    >>> criterion = QuantileRegressionLoss()
    >>> criterion
    QuantileRegressionLoss(reduction=mean, q=0.5)
    >>> loss = criterion(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, reduction: str = "mean", q: float = 0.5) -> None:
        super().__init__()
        check_loss_reduction_strategy(reduction)
        self.reduction = str(reduction)
        self._q = float(q)

    def extra_repr(self) -> str:
        return f"reduction={self.reduction}, q={self._q}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return quantile_regression_loss(prediction, target, reduction=self.reduction, q=self._q)
