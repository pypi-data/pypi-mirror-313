r"""Contain the general robust regression loss a.k.a the Barron robust
loss."""

from __future__ import annotations

__all__ = ["general_robust_regression_loss"]

import math
from typing import TYPE_CHECKING

from karbonn.functional.reduction import reduce_loss

if TYPE_CHECKING:
    import torch


def general_robust_regression_loss(
    prediction: torch.Tensor,
    target: torch.Tensor,
    alpha: float = 2.0,
    scale: float = 1.0,
    max: float | None = None,  # noqa: A002
    reduction: str = "mean",
) -> torch.Tensor:
    r"""Compute the general robust regression loss a.k.a. Barron robust
    loss.

    Based on the paper:

        A General and Adaptive Robust Loss Function
        Jonathan T. Barron
        CVPR 2019 (https://arxiv.org/abs/1701.03077)

    Note:
        The "adaptative" part of the loss is not implemented in this
            function.

    Args:
        prediction: The predictions.
        target: The target values.
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

    Returns:
        The loss. The shape of the tensor depends on the reduction
            strategy.

    Raises:
        ValueError: if the reduction is not valid.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import general_robust_regression_loss
    >>> loss = general_robust_regression_loss(
    ...     torch.randn(2, 4, requires_grad=True), torch.randn(2, 4)
    ... )
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    squared_error = prediction.sub(target).div(scale).pow(2)
    if alpha == 2:
        loss = squared_error
    elif alpha == 0:
        loss = squared_error.mul(0.5).add(1).log()
    else:
        alpha2 = math.fabs(alpha - 2)
        loss = squared_error.div(alpha2).add(1).pow(alpha / 2).sub(1).mul(alpha2 / alpha)
    if max is not None:
        loss = loss.clamp(max=max)
    return reduce_loss(loss, reduction)
