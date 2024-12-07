r"""Contain the implementation of the Poisson regression loss
function."""

from __future__ import annotations

__all__ = ["poisson_regression_loss"]

from typing import TYPE_CHECKING

from karbonn.functional.reduction import reduce_loss

if TYPE_CHECKING:
    import torch


def poisson_regression_loss(
    prediction: torch.Tensor, target: torch.Tensor, reduction: str = "mean", eps: float = 1e-8
) -> torch.Tensor:
    r"""Compute the Poisson regression loss.

    Loss Functions and Metrics in Deep Learning
    https://arxiv.org/pdf/2307.02694

    Args:
        prediction: The count predictions. The values must be positive.
        target: The count target values. The values must be positive.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the count is zero.

    Returns:
        The Poisson regression loss. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import poisson_regression_loss
    >>> loss = poisson_regression_loss(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    loss = prediction - target.mul(prediction.clamp(min=eps).log())
    return reduce_loss(loss, reduction)
