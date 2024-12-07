r"""Contain the implementation of the poisson regression loss
function."""

from __future__ import annotations

__all__ = ["PoissonRegressionLoss"]

import torch
from torch import nn

from karbonn.functional.loss import poisson_regression_loss
from karbonn.functional.reduction import check_loss_reduction_strategy


class PoissonRegressionLoss(nn.Module):
    r"""Implement a loss module that computes the Poisson regression
    loss.

    Loss Functions and Metrics in Deep Learning
    https://arxiv.org/pdf/2307.02694

    Args:
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the count is zero.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import PoissonRegressionLoss
    >>> criterion = PoissonRegressionLoss()
    >>> criterion
    PoissonRegressionLoss(reduction=mean, eps=1e-08)
    >>> loss = criterion(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, reduction: str = "mean", eps: float = 1e-8) -> None:
        super().__init__()
        check_loss_reduction_strategy(reduction)
        self.reduction = str(reduction)
        self._eps = float(eps)

    def extra_repr(self) -> str:
        return f"reduction={self.reduction}, eps={self._eps}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return poisson_regression_loss(prediction, target, reduction=self.reduction, eps=self._eps)
