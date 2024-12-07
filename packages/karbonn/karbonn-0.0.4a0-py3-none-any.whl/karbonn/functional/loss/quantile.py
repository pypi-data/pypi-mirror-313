r"""Contain the implementation of the quantile regression loss
function."""

from __future__ import annotations

__all__ = ["quantile_regression_loss"]

from typing import TYPE_CHECKING

from karbonn.functional.reduction import reduce_loss

if TYPE_CHECKING:
    import torch


def quantile_regression_loss(
    prediction: torch.Tensor, target: torch.Tensor, q: float = 0.5, reduction: str = "mean"
) -> torch.Tensor:
    r"""Compute the quantile regression loss.

    Loss Functions and Metrics in Deep Learning
    https://arxiv.org/pdf/2307.02694

    Args:
        prediction: The predictions.
        target: The target values.
        q: The quantile value. ``q=0.5`` is equivalent to the Mean
            Absolute Error (MAE).
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The quantile regression loss. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import quantile_regression_loss
    >>> loss = quantile_regression_loss(
    ...     torch.randn(2, 4, requires_grad=True), torch.randn(2, 4)
    ... )
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    diff = target - prediction
    loss = q * diff.clamp_min(0.0) + (1.0 - q) * (diff.neg().clamp_min(0.0))
    return reduce_loss(loss, reduction)
