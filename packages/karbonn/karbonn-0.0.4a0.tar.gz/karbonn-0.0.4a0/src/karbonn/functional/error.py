r"""Contain some functions to compute errors between predictions and
targets."""

from __future__ import annotations

__all__ = ["absolute_error", "absolute_relative_error", "symmetric_absolute_relative_error"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


def absolute_error(prediction: Tensor, target: Tensor) -> Tensor:
    r"""Compute the element-wise absolute error between the predictions
    and targets.

    Args:
        prediction: The tensor of predictions.
        target: The target tensor, which must have the same shape and
            data type as ``prediction``.

    Returns:
        The absolute error tensor, which has the same shape and data
            type as the inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import absolute_error
    >>> absolute_error(torch.eye(2), torch.ones(2, 2))
    tensor([[0., 1.],
            [1., 0.]])

    ```
    """
    return target.sub(prediction).abs()


def absolute_relative_error(prediction: Tensor, target: Tensor, eps: float = 1e-8) -> Tensor:
    r"""Compute the element-wise absolute relative error between the
    predictions and targets.

    Args:
        prediction: The tensor of predictions.
        target: The target tensor, which must have the same shape and
            data type as ``prediction``.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the target is zero.

    Returns:
        The absolute relative error tensor, which has the same shape
            and data type as the inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import absolute_relative_error
    >>> absolute_relative_error(torch.eye(2), torch.ones(2, 2))
    tensor([[0., 1.],
            [1., 0.]])

    ```
    """
    return target.sub(prediction).div(target.abs().clamp(min=eps)).abs()


def symmetric_absolute_relative_error(
    prediction: Tensor, target: Tensor, eps: float = 1e-8
) -> Tensor:
    r"""Compute the element-wise symmetric absolute relative error
    between the predictions and targets.

    Args:
        prediction: The tensor of predictions.
        target: The target tensor, which must have the same shape and
            data type as ``prediction``.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the target is zero.

    Returns:
        The symmetric absolute relative error tensor, which has the
            same shape and data type as the inputs.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import symmetric_absolute_relative_error
    >>> symmetric_absolute_relative_error(torch.eye(2), torch.ones(2, 2))
    tensor([[0., 2.],
            [2., 0.]])

    ```
    """
    return (
        target.sub(prediction).div(target.abs().add(prediction.abs()).mul(0.5).clamp(min=eps)).abs()
    )
