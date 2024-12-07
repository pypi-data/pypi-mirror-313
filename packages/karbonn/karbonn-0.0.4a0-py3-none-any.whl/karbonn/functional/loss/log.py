r"""Contain the loss functions that use the logarithmic function to
transform the predictions or targets."""

from __future__ import annotations

__all__ = ["log_cosh_loss", "msle_loss"]

from typing import TYPE_CHECKING

from torch.nn.functional import mse_loss

from karbonn.functional.reduction import reduce_loss

if TYPE_CHECKING:
    import torch


def log_cosh_loss(
    prediction: torch.Tensor,
    target: torch.Tensor,
    reduction: str = "mean",
    scale: float = 1.0,
) -> torch.Tensor:
    r"""Compute the logarithm of the hyperbolic cosine of the prediction
    error.

    Args:
        prediction: The predictions.
        target: The target values.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        scale: The scale factor.

    Returns:
        The logarithm of the hyperbolic cosine of the prediction error.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import log_cosh_loss
    >>> loss = log_cosh_loss(torch.randn(3, 5, requires_grad=True), torch.randn(3, 5))
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    return reduce_loss(
        target.sub(prediction).div(scale).cosh().log(),
        reduction=reduction,
    )


def msle_loss(
    prediction: torch.Tensor, target: torch.Tensor, reduction: str = "mean"
) -> torch.Tensor:
    r"""Compute the mean squared error (MSE) on the logarithmic
    transformed predictions and targets.

    This loss is best to use when targets having exponential growth,
    such as population counts, average sales of a commodity over a
    span of years etc. Note that this loss penalizes an
    under-predicted estimate greater than an over-predicted estimate.

    Note: this loss only works with positive values (0 included).

    Args:
        prediction: The predictions.
        target: The target values.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The mean squared logarithmic error. The shape of
            the tensor depends on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import msle_loss
    >>> loss = msle_loss(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<MseLossBackward0>)
    >>> loss.backward()

    ```
    """
    return mse_loss(prediction.log1p(), target.log1p(), reduction=reduction)
