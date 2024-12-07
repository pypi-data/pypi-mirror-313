r"""Contain the general robust regression loss a.k.a the Barron robust
loss."""

from __future__ import annotations

__all__ = ["GeneralRobustRegressionLoss"]


import torch
from torch import nn

from karbonn.functional import (
    check_loss_reduction_strategy,
    general_robust_regression_loss,
)


class GeneralRobustRegressionLoss(nn.Module):
    r"""Implement the general robust regression loss a.k.a. Barron robust
    loss.

    Based on the paper:

        A General and Adaptive Robust Loss Function
        Jonathan T. Barron
        CVPR 2019 (https://arxiv.org/abs/1701.03077)

    Note:
        The "adaptative" part of the loss is not implemented in this
            function.

    Args:
        alpha: The shape parameter that controls the robustness of the
            loss.
        scale: The scale parameter that controls the size of the loss's
            quadratic bowl near 0.
        max: The max value to clip the loss before to compute the
            reduction. ``None`` means no clipping is used.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Target: ``(*)``, same shape as the input.
        - Output: scalar. If ``reduction`` is ``'none'``, then ``(*)``, same
          shape as input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import GeneralRobustRegressionLoss
    >>> criterion = GeneralRobustRegressionLoss()
    >>> criterion
    GeneralRobustRegressionLoss(alpha=2.0, scale=1.0, max=None, reduction=mean)
    >>> input = torch.randn(3, 2, requires_grad=True)
    >>> target = torch.rand(3, 2, requires_grad=False)
    >>> loss = criterion(input, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(
        self,
        alpha: float = 2.0,
        scale: float = 1.0,
        max: float | None = None,  # noqa: A002
        reduction: str = "mean",
    ) -> None:
        super().__init__()
        self._alpha = float(alpha)
        if scale <= 0:
            msg = f"scale has to be greater than 0 but received {scale}"
            raise ValueError(msg)
        self._scale = float(scale)
        self._max = max

        check_loss_reduction_strategy(reduction)
        self.reduction = reduction

    def extra_repr(self) -> str:
        return (
            f"alpha={self._alpha}, scale={self._scale}, max={self._max}, "
            f"reduction={self.reduction}"
        )

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return general_robust_regression_loss(
            prediction=prediction,
            target=target,
            alpha=self._alpha,
            scale=self._scale,
            max=self._max,
            reduction=self.reduction,
        )
